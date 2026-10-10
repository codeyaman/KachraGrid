"""
KachraGrid v2 - Database Module
SQLite Schema, Seed Data, and Query Functions for Bangalore Ward 142
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from config import DB_PATH, DIESEL_RATE_PER_LITER


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initializes tables and seeds initial data if not already populated."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Bins table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bins (
        bin_id TEXT PRIMARY KEY,
        landmark TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        zone_type TEXT NOT NULL,
        capacity_kg INTEGER NOT NULL,
        current_fill_pct INTEGER NOT NULL DEFAULT 50,
        status TEXT NOT NULL DEFAULT 'Active',
        last_cleaned_at TEXT
    )
    """)

    # 2. Trucks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trucks (
        truck_id TEXT PRIMARY KEY,
        driver_name TEXT NOT NULL,
        mileage_km_l REAL NOT NULL,
        capacity_kg INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Available',
        current_lat REAL NOT NULL,
        current_lon REAL NOT NULL,
        target_bin_id TEXT,
        assigned_app_id TEXT
    )
    """)

    # 3. Applications table (Citizen Complaints)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        application_id TEXT PRIMARY KEY,
        citizen_name TEXT NOT NULL,
        citizen_phone TEXT NOT NULL,
        ward_no TEXT NOT NULL DEFAULT '142',
        bin_id TEXT NOT NULL,
        location_desc TEXT,
        problem_type TEXT NOT NULL,
        photo_path TEXT,
        ai_fill_pct INTEGER,
        ai_waste_type TEXT,
        ai_urgency TEXT,
        ai_notes TEXT,
        status TEXT NOT NULL DEFAULT 'PENDING',
        officer_notes TEXT,
        work_order_id TEXT,
        assigned_truck_id TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (bin_id) REFERENCES bins (bin_id)
    )
    """)

    # 4. Fuel Log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuel_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        truck_id TEXT NOT NULL,
        trip_date TEXT NOT NULL,
        distance_km REAL NOT NULL,
        fuel_liters REAL NOT NULL,
        fuel_cost_inr REAL NOT NULL,
        savings_inr REAL NOT NULL,
        application_id TEXT,
        notes TEXT,
        FOREIGN KEY (truck_id) REFERENCES trucks (truck_id)
    )
    """)

    # 5. Status Log table (Audit & Timeline Tracker)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT NOT NULL,
        stage TEXT NOT NULL,
        status_text TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        details TEXT,
        FOREIGN KEY (application_id) REFERENCES applications (application_id)
    )
    """)

    conn.commit()

    # Seed initial data if empty
    cursor.execute("SELECT COUNT(*) FROM bins")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()

    conn.close()


def seed_data(cursor: sqlite3.Cursor):
    now = datetime.now()

    # 25 Bins in Bangalore Ward 142 (Jayanagar 3rd/4th/5th Block)
    bins_data = [
        ("B001", "Jayanagar 4th Block Shopping Complex Market", 12.9250, 77.5830, "market", 1000, 95),
        ("B002", "33rd Cross Residential Avenue", 12.9265, 77.5845, "residential", 500, 40),
        ("B003", "11th Main Park Side Road", 12.9278, 77.5812, "residential", 500, 60),
        ("B004", "Cosmopolitan Club Commercial Zone", 12.9290, 77.5860, "commercial", 1000, 85),
        ("B005", "Vegetable & Flower Wholesale Market", 12.9305, 77.5825, "market", 2000, 100),
        ("B006", "36th Cross Residential Colony", 12.9235, 77.5870, "residential", 500, 30),
        ("B007", "Apollo Cradle & Specialty Hospital", 12.9242, 77.5890, "hospital", 1000, 75),
        ("B008", "9th Main South End Circle Residences", 12.9218, 77.5855, "residential", 500, 45),
        ("B009", "Cool Joint Commercial Plaza", 12.9260, 77.5800, "commercial", 1000, 70),
        ("B010", "Janatha Bazaar Food Street Market", 12.9275, 77.5875, "market", 2000, 90),
        ("B011", "Madhavan Park Bus Stop", 12.9320, 77.5850, "commercial", 1000, 50),
        ("B012", "Pattabhirama Nagar Temple Entrance", 12.9210, 77.5820, "residential", 500, 110),
        ("B013", "Sagar Hospitals Medical Wing", 12.9200, 77.5910, "hospital", 1500, 65),
        ("B014", "Nanda Talkies Circle", 12.9285, 77.5790, "commercial", 1000, 55),
        ("B015", "Shalimar Ground Recreation Area", 12.9335, 77.5815, "residential", 500, 25),
        ("B016", "Jayanagar Metro Station Gate 2", 12.9298, 77.5802, "commercial", 1500, 80),
        ("B017", "Byrasandra Lake Perimeter", 12.9265, 77.5920, "residential", 500, 35),
        ("B018", "Ashoka Pillar Road Crossing", 12.9350, 77.5865, "commercial", 1000, 30),
        ("B019", "Tilak Nagar Vegetable Mandi", 12.9280, 77.5950, "market", 2000, 85),
        ("B020", "Southend Circle Flower Stalls", 12.9205, 77.5800, "market", 1000, 60),
        ("B021", "RV Dental College Enclave", 12.9185, 77.5835, "hospital", 1000, 40),
        ("B022", "8th Block Post Office Lane", 12.9170, 77.5850, "residential", 500, 20),
        ("B023", "Rose Garden Children's Park", 12.9240, 77.5780, "residential", 500, 50),
        ("B024", "Maiyas Restaurant Lane Commercial", 12.9255, 77.5838, "commercial", 1200, 92),
        ("B025", "Swagath Garuda Mall Back Gate", 12.9230, 77.5930, "commercial", 1500, 68),
    ]

    for b in bins_data:
        cleaned_time = (now - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            """INSERT INTO bins (bin_id, landmark, latitude, longitude, zone_type, capacity_kg, current_fill_pct, status, last_cleaned_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'Active', ?)""",
            (b[0], b[1], b[2], b[3], b[4], b[5], b[6], cleaned_time)
        )

    # 3 Trucks
    trucks_data = [
        ("T01", "Rajesh Kumar", 6.0, 5000, "En Route", 12.9260, 77.5835, "B001", "APP-001"),
        ("T02", "Suresh Reddy", 5.5, 4500, "Cleaning", 12.9304, 77.5826, "B005", "APP-002"),
        ("T03", "Manjunath", 7.0, 4000, "Available", 12.9220, 77.5850, None, None),
    ]

    for t in trucks_data:
        cursor.execute(
            """INSERT INTO trucks (truck_id, driver_name, mileage_km_l, capacity_kg, status, current_lat, current_lon, target_bin_id, assigned_app_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            t
        )

    # Sample Applications
    apps = [
        (
            "APP-001", "Priya Sharma", "9876543210", "142", "B001",
            "Near 4th Block Vegetable stalls, plastic & wet waste spilled on road",
            "Overflow", "uploads/sample_b001.jpg", 95, "Mixed Organic & Plastic", "CRITICAL",
            "AI detected 95% full bin with street spillage and pedestrian blockage.",
            "APPROVED", "Approved for immediate clearance by AEE Jayanagar Sub-division.",
            "WO-2025-0101", "T01",
            (now - timedelta(hours=3, minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
            (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "APP-002", "Ahmed Khan", "9845112233", "142", "B005",
            "Near Wholesale flower shop, foul odor and flies",
            "Overflow", "uploads/sample_b005.jpg", 100, "Organic Rotten Waste", "CRITICAL",
            "AI verified 100% capacity exceeded. Heavy rotting wet waste.",
            "APPROVED", "High odor complaint. Truck T02 diverted.",
            "WO-2025-0102", "T02",
            (now - timedelta(hours=2, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
            (now - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "APP-003", "Dr. Meena", "9900223344", "142", "B007",
            "Near clinic rear exit, bio-hazard bags mixed in municipal bin",
            "Hazardous", "uploads/sample_b007.jpg", 75, "Biomedical / Hazardous", "HIGH",
            "AI identified clinical waste bags mixed with municipal refuse.",
            "APPROVED", "Sanitary Inspector alerted. Dispatched with protective gear protocol.",
            "WO-2025-0103", "T03",
            (now - timedelta(hours=1, minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
            (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "APP-004", "Ramesh", "9741009988", "142", "B012",
            "Temple entrance bin not collected for 2 days",
            "Not collected", None, 110, "Domestic Waste", "HIGH",
            "Simulated fill rate 110% overflow. Temple festival debris.",
            "PENDING", None, None, None,
            (now - timedelta(minutes=22)).strftime("%Y-%m-%d %H:%M:%S"),
            (now - timedelta(minutes=22)).strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "APP-005", "Sunita", "9611883322", "142", "B018",
            "Slight smell when passing Ashoka pillar intersection",
            "Smell", None, 30, "Dry Leaves", "LOW",
            "AI assessed 30% fill level. Normal ventilation odor.",
            "REJECTED", "Low priority: Bin below 35% capacity. Scheduled for regular morning sweep.",
            None, None,
            (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            (now - timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        ),
    ]

    for a in apps:
        cursor.execute("""
        INSERT INTO applications (
            application_id, citizen_name, citizen_phone, ward_no, bin_id,
            location_desc, problem_type, photo_path, ai_fill_pct, ai_waste_type,
            ai_urgency, ai_notes, status, officer_notes, work_order_id,
            assigned_truck_id, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, a)

    # Status logs for APP-001
    app1_logs = [
        ("APP-001", "SUBMITTED", "Citizen complaint registered via KachraGrid portal", (now - timedelta(hours=3, minutes=15)).strftime("%Y-%m-%d %H:%M:%S"), "Application ID KG-2025-001 issued"),
        ("APP-001", "AI_ANALYSIS", "Computer Vision AI evaluated image: 95% full", (now - timedelta(hours=3, minutes=14)).strftime("%Y-%m-%d %H:%M:%S"), "Classification: Mixed Organic & Plastic | Severity: CRITICAL"),
        ("APP-001", "OFFICE_REVIEW", "Application reviewed by Municipal Executive Engineer", (now - timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M:%S"), "Urgency verified against Ward 142 heat-map"),
        ("APP-001", "APPROVED", "Approved for clearance. Work Order WO-2025-0101 created", (now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"), "Assigned to Compactor Truck T01 (Driver: Rajesh Kumar)"),
        ("APP-001", "DISPATCHED", "Truck T01 departed depot", (now - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"), "Distance to bin: 3.2 km | Estimated ETA: 12 mins"),
        ("APP-001", "EN_ROUTE", "Truck T01 en route near 4th Block Main Road", (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"), "Simulated GPS tracker ping: 12.9260, 77.5835")
    ]
    for sl in app1_logs:
        cursor.execute("INSERT INTO status_log (application_id, stage, status_text, timestamp, details) VALUES (?, ?, ?, ?, ?)", sl)

    # Sample Fuel Data
    fuel_records = [
        ("T01", "2025-01-13", 12.4, 2.07, 184.23, 112.00, "APP-001", "Optimized route via 4th Block"),
        ("T02", "2025-01-13", 8.1, 1.47, 130.83, 78.00, "APP-002", "Direct pickup at Wholesale market"),
        ("T03", "2025-01-13", 5.6, 0.80, 71.20, 45.00, "APP-003", "Hospital bio-waste specialized run"),
        ("T01", "2025-01-14", 14.2, 2.37, 210.93, 125.00, None, "Morning routine + 2 complaints cleared"),
        ("T02", "2025-01-14", 10.5, 1.91, 169.99, 95.00, None, "Commercial corridor sweeps"),
        ("T03", "2025-01-14", 7.8, 1.11, 98.79, 62.00, None, "Southern ring road pickups"),
        ("T01", "2025-01-15", 11.0, 1.83, 162.87, 104.00, None, "AI dynamic dispatched route"),
        ("T02", "2025-01-15", 9.2, 1.67, 148.63, 88.00, None, "Afternoon responsive collection"),
        ("T03", "2025-01-15", 6.5, 0.93, 82.77, 54.00, None, "Emergency clearance run")
    ]
    for fr in fuel_records:
        cursor.execute("""
        INSERT INTO fuel_log (truck_id, trip_date, distance_km, fuel_liters, fuel_cost_inr, savings_inr, application_id, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, fr)


# ------------------- Query Functions ------------------- #

def get_all_bins() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM bins ORDER BY bin_id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_bin_by_id(bin_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM bins WHERE bin_id = ?", (bin_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_bin_fill(bin_id: str, new_pct: int, cleaned: bool = False):
    conn = get_db_connection()
    if cleaned:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn.execute("UPDATE bins SET current_fill_pct = ?, last_cleaned_at = ? WHERE bin_id = ?", (new_pct, now_str, bin_id))
    else:
        conn.execute("UPDATE bins SET current_fill_pct = ? WHERE bin_id = ?", (new_pct, bin_id))
    conn.commit()
    conn.close()


def get_all_trucks() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM trucks ORDER BY truck_id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_truck_position(truck_id: str, lat: REAL, lon: REAL, status: str, target_bin_id: Optional[str] = None):
    conn = get_db_connection()
    conn.execute(
        "UPDATE trucks SET current_lat = ?, current_lon = ?, status = ?, target_bin_id = ? WHERE truck_id = ?",
        (lat, lon, status, target_bin_id, truck_id)
    )
    conn.commit()
    conn.close()


def create_application(
    app_id: str,
    name: str,
    phone: str,
    ward_no: str,
    bin_id: str,
    location_desc: str,
    problem_type: str,
    photo_path: Optional[str],
    ai_fill_pct: int,
    ai_waste_type: str,
    ai_urgency: str,
    ai_notes: str
) -> str:
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
    INSERT INTO applications (
        application_id, citizen_name, citizen_phone, ward_no, bin_id,
        location_desc, problem_type, photo_path, ai_fill_pct, ai_waste_type,
        ai_urgency, ai_notes, status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
    """, (app_id, name, phone, ward_no, bin_id, location_desc, problem_type,
          photo_path, ai_fill_pct, ai_waste_type, ai_urgency, ai_notes, now_str, now_str))

    # Add initial status logs
    conn.execute("""
    INSERT INTO status_log (application_id, stage, status_text, timestamp, details)
    VALUES (?, 'SUBMITTED', 'Grievance submitted by citizen', ?, ?)
    """, (app_id, now_str, f"Registered under Ward {ward_no} - {bin_id}"))

    conn.execute("""
    INSERT INTO status_log (application_id, stage, status_text, timestamp, details)
    VALUES (?, 'AI_ANALYSIS', 'Hugging Face AI Vision & Urgency Analyzed', ?, ?)
    """, (app_id, now_str, f"Detected {ai_fill_pct}% fill level | Category: {ai_waste_type} | Priority: {ai_urgency}"))

    # Also reflect fill level on bin if higher
    bin_info = conn.execute("SELECT current_fill_pct FROM bins WHERE bin_id = ?", (bin_id,)).fetchone()
    if bin_info and ai_fill_pct > bin_info["current_fill_pct"]:
        conn.execute("UPDATE bins SET current_fill_pct = ? WHERE bin_id = ?", (ai_fill_pct, bin_id))

    conn.commit()
    conn.close()
    return app_id


def get_all_applications(filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if filter_status and filter_status != "ALL":
        rows = conn.execute("""
        SELECT a.*, b.landmark, b.latitude, b.longitude 
        FROM applications a 
        LEFT JOIN bins b ON a.bin_id = b.bin_id
        WHERE a.status = ?
        ORDER BY a.created_at DESC
        """, (filter_status,)).fetchall()
    else:
        rows = conn.execute("""
        SELECT a.*, b.landmark, b.latitude, b.longitude 
        FROM applications a 
        LEFT JOIN bins b ON a.bin_id = b.bin_id
        ORDER BY a.created_at DESC
        """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_application_by_id(app_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("""
    SELECT a.*, b.landmark, b.latitude, b.longitude, b.capacity_kg
    FROM applications a 
    LEFT JOIN bins b ON a.bin_id = b.bin_id
    WHERE a.application_id = ?
    """, (app_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_application_status(
    app_id: str,
    new_status: str,
    officer_notes: str = "",
    work_order_id: Optional[str] = None,
    assigned_truck_id: Optional[str] = None
):
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("""
    UPDATE applications
    SET status = ?, officer_notes = ?, work_order_id = COALESCE(?, work_order_id),
        assigned_truck_id = COALESCE(?, assigned_truck_id), updated_at = ?
    WHERE application_id = ?
    """, (new_status, officer_notes, work_order_id, assigned_truck_id, now_str, app_id))

    # Log to status audit
    stage_name = new_status
    status_desc = f"Application marked as {new_status} by BBMP Ward 142 Office."
    if new_status == "APPROVED":
        status_desc = f"Work Order {work_order_id} issued. Truck {assigned_truck_id} allocated."
    elif new_status == "REJECTED":
        status_desc = f"Application rejected. Reason: {officer_notes}"
    elif new_status == "HOLD":
        status_desc = f"Placed on administrative hold: {officer_notes}"

    conn.execute("""
    INSERT INTO status_log (application_id, stage, status_text, timestamp, details)
    VALUES (?, ?, ?, ?, ?)
    """, (app_id, stage_name, status_desc, now_str, officer_notes))

    if assigned_truck_id and new_status == "APPROVED":
        app = conn.execute("SELECT bin_id FROM applications WHERE application_id = ?", (app_id,)).fetchone()
        if app:
            conn.execute(
                "UPDATE trucks SET status = 'En Route', target_bin_id = ?, assigned_app_id = ? WHERE truck_id = ?",
                (app["bin_id"], app_id, assigned_truck_id)
            )

    conn.commit()
    conn.close()


def get_status_timeline(app_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT * FROM status_log 
    WHERE application_id = ? 
    ORDER BY log_id ASC
    """, (app_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_fuel_log_entry(
    truck_id: str,
    trip_date: str,
    distance_km: float,
    fuel_liters: float,
    fuel_cost_inr: float,
    savings_inr: float,
    app_id: Optional[str] = None,
    notes: str = ""
):
    conn = get_db_connection()
    conn.execute("""
    INSERT INTO fuel_log (truck_id, trip_date, distance_km, fuel_liters, fuel_cost_inr, savings_inr, application_id, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (truck_id, trip_date, distance_km, fuel_liters, fuel_cost_inr, savings_inr, app_id, notes))
    conn.commit()
    conn.close()


def get_all_fuel_logs() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT f.*, t.driver_name, t.mileage_km_l 
    FROM fuel_log f
    LEFT JOIN trucks t ON f.truck_id = t.truck_id
    ORDER BY f.trip_date DESC, f.log_id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize on import
init_database()
