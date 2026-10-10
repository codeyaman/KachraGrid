# KachraGrid v2 — 3-Minute Live Walkthrough Demo Script

**City & Ward:** Bangalore, Ward 142 — Jayanagar  
**Audience:** Municipal Commissioners, Smart City Evaluators, Civic Hackathon Jury  
**Duration:** 3 Minutes  

---

### [0:00 - 0:35] Scene 1: The Problem & The Citizen Experience (Page 1)
**Presenter:**
> *"Welcome to KachraGrid v2. In traditional Indian cities, citizen complaints get lost in bureaucracy, and garbage trucks follow rigid fixed routes that waste diesel and ignore overflowing bins. KachraGrid v2 bridges this gap with an open-source, civic AI workflow."*

**Action:**
1. Open **Page 1: Citizen Complaint Form**.
2. Point out Ward 142 Jayanagar (Bangalore) context.
3. Enter citizen details: `Priya Sharma`, Mobile `9876543210`.
4. Select bin: `B001 — Jayanagar 4th Block Shopping Complex Market`.
5. Upload a photo (`sample_b001.jpg`).
6. **Highlight AI Inspection:** Show that the local Hugging Face / Neural Computer Vision engine instantly detects **95% fill level**, flags it as **Critical Overflow**, detects mixed plastic/organic waste, and calculates an estimated payload of **684 kg**.
7. Click **Submit Complaint to Municipal Office**. Note the generated Application ID (e.g., `KG-2025-XXXXXX`).

---

### [0:35 - 1:15] Scene 2: Municipal Office Review & Approval (Page 3)
**Presenter:**
> *"Unlike naive dispatch systems that bypass municipal authority, KachraGrid v2 simulates the real Indian government administrative flow. Every grievance lands on the Municipal Executive Engineer's dashboard before any public funds or fuel are spent."*

**Action:**
1. Switch to **Page 3: Municipal Officer Dashboard**.
2. Highlight top KPI tiles: Pending Grievances, Active Work Orders, Cleared Bins, and Rejections.
3. Scroll to the newly submitted grievance or `APP-004` (Ramesh, B012).
4. Review the AI diagnostic findings side-by-side with the uploaded photo.
5. Select compactor truck `T01 (Rajesh Kumar)`.
6. Click **Approve**. Show that it immediately generates a verifiable **Work Order ID** (e.g., `WO-2025-XXXX`) and transitions the grievance to approved status.
7. Optional: Click the **⏱️ Auto-SLA** button in the sidebar to demonstrate how neglected complaints older than 30 minutes are automatically escalated and approved according to citizen charter SLAs.

---

### [1:15 - 2:05] Scene 3: Dynamic Truck Dispatch & Live Map (Page 4)
**Presenter:**
> *"Now let's look at the logistics engine. Once approved, compactor trucks are dynamically routed instead of following fixed routes."*

**Action:**
1. Switch to **Page 4: Live Truck Tracking & Map**.
2. Observe the interactive OpenStreetMap centered on Jayanagar Ward 142.
3. Show the **25 Bins**:
   - 🔴 Red circle markers: Overfilled bins (>85%)
   - 🟠 Orange circle markers: Moderate bins
   - 🟢 Green circle markers: Cleaned bins
4. Point to the **BBMP Ward Depot Headquarters** and active trucks:
   - `T01` (Rajesh Kumar)
   - `T02` (Suresh Reddy)
   - `T03` (Manjunath)
5. Point out the dynamic blue route vector leading from Truck T01 directly to its target bin.
6. Click **Advance Step (2 min)** in the sidebar:
   - Watch the trucks advance on the map towards their assigned bins.
   - Show how bin statuses transition from `Dispatched` → `En Route` → `Cleaning` → `Completed`.

---

### [2:05 - 2:40] Scene 4: Fuel Economics & Savings (Page 5)
**Presenter:**
> *"Every municipal trip incurs real public fuel costs. Bangalore's diesel rate is ₹89/liter. KachraGrid v2 tracks fuel consumption per trip and proves civic savings versus outdated fixed sweeps."*

**Action:**
1. Navigate to **Page 5: Fuel & Diesel Dashboard**.
2. Review top financial cards:
   - Total Distance Logged (km)
   - Total Diesel Consumed (Liters)
   - Total Diesel Expenditure at ₹89/L
   - Total Fiscal Savings versus traditional 32.5 km fixed route
3. Demonstrate the **Interactive Fuel Trip Calculator**:
   - Select Truck `T01` (Mileage: 6.0 km/L).
   - Enter `12.4 km`.
   - Show calculation: 2.07 Liters used, ₹184.23 cost, **₹112 saved** compared to running the entire fixed route.
4. Show the Truck Efficiency breakdown table and daily cost bar charts.

---

### [2:40 - 3:00] Scene 5: Citizen Closure & Multilingual AI (Page 2 & Sidebar)
**Presenter:**
> *"Finally, transparency is closed back to the citizen."*

**Action:**
1. Go to **Page 2: Application Status Tracker**.
2. Select `APP-001` or search the newly created ID.
3. Display the **Audit Timeline**:
   - `SUBMITTED` → `AI_ANALYSIS` → `OFFICE_REVIEW` → `APPROVED` → `DISPATCHED` → `COMPLETED`.
4. Open the **Sahaya AI Citizen Chat** in the sidebar:
   - Switch language to **Kannada** or **Hindi**.
   - Show instant civic assistance explaining segregation rules and collection schedules.

**Presenter Closing:**
> *"100% Free, 100% Open Source, running completely locally without paid APIs. Thank you!"*
