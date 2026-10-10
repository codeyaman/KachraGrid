"""
KachraGrid v2 - Simulation Engine
Simulates Indian Municipal Office Workflows:
  1. Auto-approval logic for grievances pending > 30 mins
  2. Truck lifecycle dispatch: DISPATCHED -> EN ROUTE -> ARRIVED -> CLEANING -> COMPLETED
  3. Dynamic GPS stepping and trajectory interpolation
  4. Automatic Fuel logging on job completion
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import database
from fuel_tracker import FuelTracker

fuel_tracker = FuelTracker()

# Simulated depot coordinates (Jayanagar BBMP Sub-Division Office)
DEPOT_LAT = 12.9290
DEPOT_LON = 77.5835

# Route milestones
STAGE_SEQUENCE = ["PENDING", "APPROVED", "DISPATCHED", "EN_ROUTE", "ARRIVED", "CLEANING", "COMPLETED"]


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def run_auto_approval_check(minutes_threshold: int = 30) -> List[str]:
    """
    Checks for pending grievances older than `minutes_threshold` minutes.
    In the prototype demo, auto-approves them and assigns the nearest available truck.
    """
    now = datetime.now()
    pending_apps = database.get_all_applications(filter_status="PENDING")
    approved_ids = []

    trucks = database.get_all_trucks()
    available_trucks = [t for t in trucks if t["status"] in ("Available", "Idle")]
    if not available_trucks:
        available_trucks = trucks  # Assign round-robin if all busy

    for idx, app in enumerate(pending_apps):
        try:
            created_dt = datetime.strptime(app["created_at"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            created_dt = now - timedelta(minutes=45)

        age_minutes = (now - created_dt).total_seconds() / 60.0

        if age_minutes >= minutes_threshold or app.get("ai_urgency") == "CRITICAL":
            assigned_truck = available_trucks[idx % len(available_trucks)]
            wo_id = f"WO-AUTO-{random.randint(1000, 9999)}"
            officer_note = (
                f"Automated Civic SLA Threshold Exceeded ({int(age_minutes)} mins). "
                f"Auto-approved by BBMP Autonomous Dispatch Engine."
            )

            database.update_application_status(
                app_id=app["application_id"],
                new_status="APPROVED",
                officer_notes=officer_note,
                work_order_id=wo_id,
                assigned_truck_id=assigned_truck["truck_id"]
            )
            approved_ids.append(app["application_id"])

    return approved_ids


def advance_simulation_tick() -> Dict[str, Any]:
    """
    Advances the prototype world by one simulation step:
    - Moves active trucks closer to their target bin
    - Updates application lifecycle stages
    - If a truck reaches cleaning completion, marks application RESOLVED,
      cleans the bin (resets fill to 10%), and logs fuel consumption.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trucks = database.get_all_trucks()
    events = []

    for t in trucks:
        tid = t["truck_id"]
        status = t["status"]
        target_bin_id = t["target_bin_id"]
        app_id = t["assigned_app_id"]

        if not target_bin_id or status == "Available":
            continue

        target_bin = database.get_bin_by_id(target_bin_id)
        if not target_bin:
            continue

        dest_lat = target_bin["latitude"]
        dest_lon = target_bin["longitude"]
        curr_lat = t["current_lat"]
        curr_lon = t["current_lon"]

        dist_to_bin = haversine_distance(curr_lat, curr_lon, dest_lat, dest_lon)

        # 1. State: En Route -> advancing position
        if status in ("En Route", "Dispatched"):
            if dist_to_bin <= 0.15:
                # Arrived
                database.update_truck_position(tid, dest_lat, dest_lon, "Cleaning", target_bin_id)
                events.append(f"Truck {tid} reached bin {target_bin_id} and began compactor cleaning.")
                if app_id:
                    _log_app_stage(app_id, "ARRIVED", f"Truck {tid} arrived on-site at {target_bin['landmark']}.")
            else:
                # Move 35% closer
                new_lat = curr_lat + 0.35 * (dest_lat - curr_lat)
                new_lon = curr_lon + 0.35 * (dest_lon - curr_lon)
                database.update_truck_position(tid, new_lat, new_lon, "En Route", target_bin_id)
                events.append(f"Truck {tid} en route to {target_bin_id} (Distance left: {round(dist_to_bin, 2)} km).")
                if app_id:
                    _log_app_stage(app_id, "EN_ROUTE", f"GPS Telemetry: Truck {tid} moving along Ward 142 transit route.")

        # 2. State: Cleaning -> Complete
        elif status == "Cleaning":
            # Bin is cleaned
            database.update_bin_fill(target_bin_id, new_pct=10, cleaned=True)

            # Calculate trip distance from depot to bin + return
            trip_km = round(haversine_distance(DEPOT_LAT, DEPOT_LON, dest_lat, dest_lon) * 2.2 + random.uniform(1.0, 3.5), 1)

            # Record fuel
            fuel_res = fuel_tracker.record_completed_trip(
                truck_id=tid,
                distance_km=trip_km,
                application_id=app_id,
                notes=f"Completed pickup at {target_bin['landmark']}."
            )

            # Release truck back to available
            database.update_truck_position(tid, DEPOT_LAT, DEPOT_LON, "Available", None)
            conn = database.get_db_connection()
            conn.execute("UPDATE trucks SET assigned_app_id = NULL WHERE truck_id = ?", (tid,))
            conn.commit()
            conn.close()

            # Mark Application COMPLETED
            if app_id:
                database.update_application_status(
                    app_id=app_id,
                    new_status="COMPLETED",
                    officer_notes=f"Waste successfully cleared by {tid} ({t['driver_name']}). Trip fuel: {fuel_res['fuel_liters']}L (Cost ₹{fuel_res['cost_inr']})."
                )
                _log_app_stage(app_id, "COMPLETED", f"Bin {target_bin_id} emptied. 100% grievance resolved.")

            events.append(f"Truck {tid} completed cleaning at {target_bin_id}! Logged {trip_km} km (Fuel: {fuel_res['fuel_liters']}L, Cost: ₹{fuel_res['cost_inr']}).")

    return {"timestamp": now_str, "events": events}


def _log_app_stage(app_id: str, stage: str, details: str):
    conn = database.get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
    INSERT INTO status_log (application_id, stage, status_text, timestamp, details)
    VALUES (?, ?, ?, ?, ?)
    """, (app_id, stage, f"Live Operation: {stage}", now_str, details))
    conn.commit()
    conn.close()


def generate_simulated_timeline(app_id: str) -> List[Dict[str, Any]]:
    """Fetches real status logs and produces human-friendly visual stage badges."""
    logs = database.get_status_timeline(app_id)
    app = database.get_application_by_id(app_id)
    if not app:
        return []

    return logs
