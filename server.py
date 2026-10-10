"""
KachraGrid v2 — Flask REST API Server
Serves all backend logic (database, AI, fuel, simulation) to the Vite frontend.
"""

import os
import base64
import io
import json
import random
import urllib.request
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image

import config
import database
import ai_models
from fuel_tracker import FuelTracker
import simulation

app = Flask(__name__)
CORS(app)

database.init_database()
fuel_tracker = FuelTracker()


# ───── Health & System Config ─────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "ward": "142", "city": "Bangalore"})


@app.route("/api/config")
def api_config():
    return jsonify({
        "mapbox_token": config.MAPBOX_ACCESS_TOKEN,
        "mapbox_configured": bool(config.MAPBOX_ACCESS_TOKEN),
        "openrouter_configured": bool(config.OPENROUTER_API_KEY),
        "hf_configured": bool(config.HF_TOKEN),
        "carto_key": config.CARTO_API_KEY,
        "ward_number": config.WARD_NUMBER,
        "ward_name": config.WARD_NAME,
        "city": config.CITY_NAME,
        "center_lat": config.WARD_CENTER_LAT,
        "center_lon": config.WARD_CENTER_LON
    })


@app.route("/api/route/directions", methods=["GET"])
def api_route_directions():
    start = request.args.get("start", "77.5835,12.9290")
    end = request.args.get("end", "77.5938,12.9252")
    token = config.MAPBOX_ACCESS_TOKEN
    if not token:
        return jsonify({"error": "Mapbox access token not configured"}), 400
    try:
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start};{end}?geometries=geojson&overview=full&access_token={token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ai_models._SSL_CONTEXT, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───── Bins ─────
@app.route("/api/bins")
def api_bins():
    return jsonify(database.get_all_bins())


@app.route("/api/bins/<bin_id>")
def api_bin_detail(bin_id):
    b = database.get_bin_by_id(bin_id)
    return jsonify(b) if b else (jsonify({"error": "Bin not found"}), 404)


# ───── Trucks ─────
@app.route("/api/trucks")
def api_trucks():
    return jsonify(database.get_all_trucks())


# ───── Applications ─────
@app.route("/api/applications")
def api_applications():
    status_filter = request.args.get("status", "ALL")
    return jsonify(database.get_all_applications(filter_status=status_filter))


@app.route("/api/applications/<app_id>")
def api_application_detail(app_id):
    a = database.get_application_by_id(app_id)
    return jsonify(a) if a else (jsonify({"error": "Application not found"}), 404)


@app.route("/api/applications/<app_id>/timeline")
def api_application_timeline(app_id):
    return jsonify(database.get_status_timeline(app_id))


@app.route("/api/applications", methods=["POST"])
def api_create_application():
    data = request.json
    app_id = f"KG-2025-{random.randint(100000, 999999)}"

    # Handle base64 photo if present
    photo_path = None
    ai_results = None
    if data.get("photo_base64"):
        try:
            img_bytes = base64.b64decode(data["photo_base64"].split(",")[-1])
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{app_id}.jpg"
            photo_path = os.path.join(str(config.UPLOAD_DIR), filename)
            img.save(photo_path)
            ai_results = ai_models.analyze_bin_photo(img)
        except Exception as e:
            ai_results = None

    if not ai_results:
        bin_meta = database.get_bin_by_id(data.get("bin_id", "B001"))
        fill_p = ai_models.predict_fill_level_from_metadata(
            bin_meta["capacity_kg"] if bin_meta else 1000,
            data.get("problem_type", ""),
            bin_meta["zone_type"] if bin_meta else "residential"
        )
        ai_results = {
            "fill_pct": fill_p,
            "waste_type": "Citizen Reported (No Photo)",
            "urgency": "HIGH" if fill_p >= 85 else "MEDIUM",
            "reasoning": f"Synthesized from citizen description: {data.get('problem_type', 'General')}"
        }

    database.create_application(
        app_id=app_id,
        name=data.get("citizen_name", ""),
        phone=data.get("citizen_phone", ""),
        ward_no="142",
        bin_id=data.get("bin_id", "B001"),
        location_desc=data.get("location_desc", ""),
        problem_type=data.get("problem_type", ""),
        photo_path=photo_path,
        ai_fill_pct=ai_results["fill_pct"],
        ai_waste_type=ai_results["waste_type"],
        ai_urgency=ai_results["urgency"],
        ai_notes=ai_results["reasoning"]
    )

    return jsonify({
        "application_id": app_id,
        "status": "PENDING",
        "ai": ai_results
    }), 201


# ───── Officer Actions ─────
@app.route("/api/applications/<app_id>/approve", methods=["POST"])
def api_approve(app_id):
    data = request.json or {}
    truck_id = data.get("truck_id", "T01")
    notes = data.get("officer_notes", "Approved for compactor dispatch.")
    wo_id = f"WO-2025-{random.randint(1000, 9999)}"
    database.update_application_status(
        app_id=app_id,
        new_status="APPROVED",
        officer_notes=notes,
        work_order_id=wo_id,
        assigned_truck_id=truck_id
    )
    return jsonify({"status": "APPROVED", "work_order_id": wo_id, "truck_id": truck_id})


@app.route("/api/applications/<app_id>/reject", methods=["POST"])
def api_reject(app_id):
    data = request.json or {}
    notes = data.get("officer_notes", "Rejected: Below municipal threshold.")
    database.update_application_status(app_id=app_id, new_status="REJECTED", officer_notes=notes)
    return jsonify({"status": "REJECTED"})


@app.route("/api/applications/<app_id>/hold", methods=["POST"])
def api_hold(app_id):
    data = request.json or {}
    notes = data.get("officer_notes", "Placed on administrative hold.")
    database.update_application_status(app_id=app_id, new_status="HOLD", officer_notes=notes)
    return jsonify({"status": "HOLD"})


# ───── Simulation ─────
@app.route("/api/simulation/advance", methods=["POST"])
def api_sim_advance():
    result = simulation.advance_simulation_tick()
    return jsonify(result)


@app.route("/api/simulation/auto-approve", methods=["POST"])
def api_sim_auto_approve():
    approved = simulation.run_auto_approval_check(minutes_threshold=0)
    return jsonify({"approved": approved, "count": len(approved)})


# ───── Fuel ─────
@app.route("/api/fuel/summary")
def api_fuel_summary():
    return jsonify(fuel_tracker.get_summary_metrics())


@app.route("/api/fuel/logs")
def api_fuel_logs():
    return jsonify(database.get_all_fuel_logs())


@app.route("/api/fuel/daily")
def api_fuel_daily():
    df = fuel_tracker.get_daily_trend()
    return jsonify(df.to_dict(orient="records") if not df.empty else [])


@app.route("/api/fuel/trucks")
def api_fuel_trucks():
    df = fuel_tracker.generate_monthly_report()
    return jsonify(df.to_dict(orient="records") if not df.empty else [])


@app.route("/api/fuel/calculate", methods=["POST"])
def api_fuel_calculate():
    data = request.json
    result = fuel_tracker.calculate_trip(data.get("truck_id", "T01"), float(data.get("distance_km", 10)))
    return jsonify(result)


# ───── AI Chat ─────
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    reply = ai_models.citizen_chat_assistant(
        data.get("message", ""),
        language=data.get("language", "English")
    )
    return jsonify({"reply": reply})


# ───── AI Photo Analysis ─────
@app.route("/api/analyze-photo", methods=["POST"])
def api_analyze_photo():
    data = request.json
    if not data.get("photo_base64"):
        return jsonify({"error": "No photo provided"}), 400
    try:
        img_bytes = base64.b64decode(data["photo_base64"].split(",")[-1])
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        result = ai_models.analyze_bin_photo(img)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───── Dashboard Stats ─────
@app.route("/api/dashboard/stats")
def api_dashboard_stats():
    all_apps = database.get_all_applications()
    bins = database.get_all_bins()
    trucks = database.get_all_trucks()
    fuel_sum = fuel_tracker.get_summary_metrics()

    return jsonify({
        "total_bins": len(bins),
        "critical_bins": sum(1 for b in bins if b["current_fill_pct"] >= 80),
        "moderate_bins": sum(1 for b in bins if 50 <= b["current_fill_pct"] < 80),
        "clear_bins": sum(1 for b in bins if b["current_fill_pct"] < 50),
        "total_applications": len(all_apps),
        "pending": sum(1 for a in all_apps if a["status"] == "PENDING"),
        "approved": sum(1 for a in all_apps if a["status"] == "APPROVED"),
        "completed": sum(1 for a in all_apps if a["status"] == "COMPLETED"),
        "rejected": sum(1 for a in all_apps if a["status"] == "REJECTED"),
        "trucks_active": sum(1 for t in trucks if t["status"] not in ("Available", "Idle")),
        "trucks_total": len(trucks),
        "fuel": fuel_sum,
        "diesel_rate": config.DIESEL_RATE_PER_LITER
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
