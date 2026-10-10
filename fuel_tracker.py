"""
KachraGrid v2 - Fuel Tracking Module
Calculates fuel consumption, diesel expenditures (₹89/L in Bangalore),
emissions metrics, and savings compared to conventional legacy static routes.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime
from config import DIESEL_RATE_PER_LITER, TRUCK_SPECS, TRADITIONAL_FIXED_ROUTE_KM
import database


class FuelTracker:
    def __init__(self, diesel_rate: float = DIESEL_RATE_PER_LITER):
        self.diesel_rate = diesel_rate
        self.truck_specs = TRUCK_SPECS
        self.traditional_fixed_route_km = TRADITIONAL_FIXED_ROUTE_KM

    def calculate_trip(self, truck_id: str, distance_km: float) -> Dict[str, Any]:
        """
        Calculates fuel used and cost for a specific trip.
        Formulas:
          - fuel_used (L) = distance (km) / mileage (km/L)
          - cost (₹) = fuel_used × diesel_rate (₹89)
          - baseline_cost (₹) = (legacy_km / mileage) × diesel_rate
          - savings (₹) = max(0, baseline_cost - cost)
        """
        truck_info = self.truck_specs.get(truck_id, {"mileage": 6.0, "driver": "Driver", "plate": "KA-01"})
        mileage = float(truck_info["mileage"])

        fuel_used_liters = round(distance_km / mileage, 2)
        cost_inr = round(fuel_used_liters * self.diesel_rate, 2)

        # Baseline: Old fixed route cost for that single shift/pickup cycle
        # Traditional route would have covered fixed 32.5km / 3 trucks = ~10.8 km per truck run
        legacy_baseline_km = max(distance_km, 10.8)
        legacy_fuel_liters = legacy_baseline_km / mileage
        legacy_cost_inr = legacy_fuel_liters * self.diesel_rate
        savings_inr = round(max(0.0, legacy_cost_inr - cost_inr), 2)

        # CO2 emissions: approx 2.68 kg CO2 per liter of diesel
        co2_kg = round(fuel_used_liters * 2.68, 2)
        co2_saved_kg = round((legacy_fuel_liters - fuel_used_liters) * 2.68, 2) if legacy_fuel_liters > fuel_used_liters else 0.0

        return {
            "truck_id": truck_id,
            "driver_name": truck_info["driver"],
            "mileage_km_l": mileage,
            "distance_km": round(distance_km, 2),
            "fuel_liters": fuel_used_liters,
            "fuel_rate_inr": self.diesel_rate,
            "cost_inr": cost_inr,
            "savings_inr": savings_inr,
            "co2_emitted_kg": co2_kg,
            "co2_saved_kg": co2_saved_kg
        }

    def record_completed_trip(
        self,
        truck_id: str,
        distance_km: float,
        application_id: Optional[str] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Calculates and logs completed trip directly into SQLite database."""
        trip_metrics = self.calculate_trip(truck_id, distance_km)
        today_str = datetime.now().strftime("%Y-%m-%d")

        database.add_fuel_log_entry(
            truck_id=truck_id,
            trip_date=today_str,
            distance_km=trip_metrics["distance_km"],
            fuel_liters=trip_metrics["fuel_liters"],
            fuel_cost_inr=trip_metrics["cost_inr"],
            savings_inr=trip_metrics["savings_inr"],
            app_id=application_id,
            notes=notes or f"Dynamic grievance response trip: {distance_km} km"
        )
        return trip_metrics

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Aggregates lifetime and month-to-date fuel statistics."""
        logs = database.get_all_fuel_logs()
        if not logs:
            return {
                "total_distance_km": 0.0,
                "total_fuel_liters": 0.0,
                "total_cost_inr": 0.0,
                "total_savings_inr": 0.0,
                "avg_cost_per_km": 0.0,
                "total_trips": 0
            }

        df = pd.DataFrame(logs)
        total_dist = df["distance_km"].sum()
        total_liters = df["fuel_liters"].sum()
        total_cost = df["fuel_cost_inr"].sum()
        total_savings = df["savings_inr"].sum()
        avg_cost_km = round(total_cost / total_dist, 2) if total_dist > 0 else 0.0

        return {
            "total_distance_km": round(total_dist, 1),
            "total_fuel_liters": round(total_liters, 2),
            "total_cost_inr": round(total_cost, 2),
            "total_savings_inr": round(total_savings, 2),
            "avg_cost_per_km": avg_cost_km,
            "total_trips": len(df)
        }

    def generate_monthly_report(self) -> pd.DataFrame:
        """Returns aggregated breakdown by Truck ID with driver and efficiency."""
        logs = database.get_all_fuel_logs()
        if not logs:
            return pd.DataFrame()

        df = pd.DataFrame(logs)
        # Group by truck
        grouped = df.groupby("truck_id").agg(
            trips=("log_id", "count"),
            total_km=("distance_km", "sum"),
            total_fuel_liters=("fuel_liters", "sum"),
            total_cost_inr=("fuel_cost_inr", "sum"),
            total_savings_inr=("savings_inr", "sum")
        ).reset_index()

        # Add driver & mileage info
        grouped["driver"] = grouped["truck_id"].apply(lambda tid: self.truck_specs.get(tid, {}).get("driver", "N/A"))
        grouped["mileage_km_l"] = grouped["truck_id"].apply(lambda tid: self.truck_specs.get(tid, {}).get("mileage", 6.0))
        grouped["cost_per_km"] = (grouped["total_cost_inr"] / grouped["total_km"]).round(2)

        return grouped

    def get_daily_trend(self) -> pd.DataFrame:
        """Returns daily aggregated fuel consumption and costs."""
        logs = database.get_all_fuel_logs()
        if not logs:
            return pd.DataFrame()

        df = pd.DataFrame(logs)
        daily = df.groupby("trip_date").agg(
            distance_km=("distance_km", "sum"),
            fuel_cost_inr=("fuel_cost_inr", "sum"),
            savings_inr=("savings_inr", "sum")
        ).reset_index().sort_values("trip_date")
        return daily
