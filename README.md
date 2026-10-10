<div align="center">

# 🗑️ KachraGrid

### AI-Powered Municipal Waste Complaint & Logistics System

*Photograph the garbage. Let AI file the complaint. Send the truck that is actually needed.*

![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Models](https://img.shields.io/badge/Models-Hugging_Face-yellow.svg)
![Cost](https://img.shields.io/badge/Cost-%E2%82%B90_Forever-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)
![Built at](https://img.shields.io/badge/Built_at-%5BHackathon_Name%5D-purple.svg)
![Open Source](https://img.shields.io/badge/Open_Source-Yes-green.svg)
![Build](https://img.shields.io/badge/build-CI_not_configured-lightgrey.svg)

```text
  _  __          _          _                _     _
 | |/ /__ _  ___| |__  _ __(_) __ _ _ __(_) __| |
 | ' // _` |/ __| '_ \| '__| |/ _` | '__| |/ _` |
 | . \ (_| | (__| | | | |  | | (_| | |  | | (_| |
 |_|\_\__,_|\___|_| |_|_|  |_|\__, |_|  |_|\__,_|
                              |___/
      Citizen photo  ->  AI analysis  ->  Complaint  ->  Truck
```

[Problem](#-the-problem) · [Solution](#-the-solution) · [Demo](#-live-demo-walkthrough) · [Quick Start](#-quick-start) · [Fuel Tracking](#-fuel-tracking) · [Roadmap](#-roadmap)

</div>

---

## 🚨 The Problem

> India produces roughly **1.5 lakh tonnes of municipal solid waste every day**. A large share of it is never collected.

| Figure | Value | Note |
|---|---|---|
| Daily municipal solid waste | ~1.5 lakh tonnes | Order of magnitude from CPCB / MoHUA reporting |
| Waste not collected | ~30% (estimates vary by city) | Left on streets, drains and vacant plots |
| Route design | Fixed routes, often decades old | Trucks follow a schedule, not demand |
| Complaint resolution | Days (commonly 3 to 7) | No tracking, no acknowledgement |

> **Honesty note:** the figures above are widely quoted ballpark numbers. Before publishing or presenting, replace them with citations from the latest CPCB annual report, MoHUA Swachh Survekshan data, and your target city's BBMP/BMC records.

### Why existing systems fail

- **Fixed routes ignore reality.** Trucks visit bins that are 20% full and drive past bins that are 110% full.
- **Fuel is burned on stops that collect nothing.** Every unnecessary stop costs diesel, time and wear.
- **No feedback loop.** A citizen files a complaint and hears nothing. There is no status, no ID, no accountability.
- **No data.** Without fill levels and pickup history, nobody can plan, audit or improve.
- **Complaints are unstructured.** Photos, voice notes and mixed-language messages cannot be triaged by hand at city scale.

### The human cost

- 🦟 **Disease.** Uncollected waste breeds mosquitoes, rats and flies. Dengue, cholera and leptospirosis follow.
- 🤢 **Daily indignity.** Families live beside rotting waste, stray dogs and smoke from burning piles.
- 💉 **Hidden hazards.** Medical waste, needles and chemicals end up in ordinary bins, endangering waste pickers and children.
- 🏘️ **Neighbourhood decline.** Chronic dumping lowers quality of life and erodes trust in civic institutions.

---

## 💡 The Solution

**KachraGrid** turns a smartphone photo into a tracked municipal work order.

A citizen uploads a photo of an overflowing bin. A **local open-weight vision model** reads the image, estimates how full the bin is, identifies the waste type and flags hazards. The system files a numbered application, routes it to the municipal office for review, assigns the nearest suitable truck, tracks the trip, and calculates the diesel cost and savings versus the old fixed route.

### Three phases

| Phase | What happens | Status |
|---|---|---|
| **1. Citizen Complaint** | Form, photo upload, AI image analysis, application ID, live status tracking | ✅ **REAL and functional** |
| **2. Municipal Office Review** | Officer dashboard, approve / reject / hold, work order generation | 🧪 **PROTOTYPE** (simulated; demo auto-approves after 30 s) |
| **3. Truck Dispatch & Fuel Tracking** | Truck assignment, simulated live tracking, fuel cost and savings | 🧪 **PROTOTYPE** (simulated trips, real fuel math) |

> **What is real:** photo upload, AI image analysis, complaint filing, tracking, and the fuel and savings arithmetic.
> **What is simulated:** the officer's decision, the truck's movement, and the trip completion. No real municipal system or vehicle is connected.

### Elevator pitch

Municipal waste collection is run on schedules, not signals. KachraGrid replaces the schedule with citizen photos analysed by open-weight AI running on your own hardware. Photos, phone numbers and locations never leave the municipality's machine. Every component is free, so a ward can adopt it at **₹0**.

---

## 🔄 How It Works

```text
 ┌────────────────────────────── PHASE 1: CITIZEN  [ REAL ] ──────────────────────────────┐
 │                                                                                         │
 │  ┌──────────────┐    ┌──────────────────┐    ┌────────────────┐    ┌────────────────┐  │
 │  │ Citizen      │───▶│ Complaint form   │───▶│ AI photo       │───▶│ Application    │  │
 │  │ opens app    │    │ + bin photo      │    │ analysis       │    │ KG-2025-XXXX   │  │
 │  └──────────────┘    └──────────────────┘    │ Qwen2.5-VL     │    │ created        │  │
 │                                              │ fill %, type,  │    └───────┬────────┘  │
 │                                              │ hazards,       │            │           │
 │                                              │ priority       │            ▼           │
 │                                              └────────────────┘    Status tracking     │
 └──────────────────────────────────────────────────────────────────────┬──────────────────┘
                                                                         │
 ┌──────────────────────── PHASE 2: MUNICIPAL OFFICE  [ PROTOTYPE ] ─────▼──────────────────┐
 │                                                                                           │
 │  ┌─────────────────┐    ┌───────────────────────────────┐    ┌───────────────────────┐   │
 │  │ Officer         │───▶│ Review: photo + AI analysis   │───▶│ Approve / Reject /    │   │
 │  │ dashboard       │    │ + urgency + citizen info      │    │ Hold                  │   │
 │  └─────────────────┘    └───────────────────────────────┘    └──────────┬────────────┘   │
 │                                                  (demo: auto-approve 30s) │ Approved      │
 │                                                                           ▼               │
 │                                                                  Work Order generated     │
 └───────────────────────────────────────────────────────────────────────┬───────────────────┘
                                                                          │
 ┌──────────────────── PHASE 3: DISPATCH & FUEL  [ PROTOTYPE / CALCULATED ]▼─────────────────┐
 │                                                                                            │
 │  ┌──────────────┐   ┌─────────────────────────────────────────────┐   ┌────────────────┐  │
 │  │ Truck        │──▶│ Dispatched ▶ En Route ▶ Arrived ▶ Cleaning  │──▶│ Completed      │  │
 │  │ assignment   │   │ ▶ Completed        (simulated tracking)     │   └───────┬────────┘  │
 │  │ nearest +    │   └─────────────────────────────────────────────┘           │           │
 │  │ capacity     │                                                             ▼           │
 │  └──────────────┘            Fuel tracking:  km ÷ mileage × ₹89/L  =  trip cost + savings  │
 └────────────────────────────────────────────────────────────────────────────────────────────┘

   Legend:  REAL = runs real AI on real uploads     PROTOTYPE = simulated for demonstration
```

---

## 🎬 Live Demo Walkthrough

> Screenshots live in `docs/screenshots/`. Replace the placeholders after your first run.

### Step 1: File a complaint

![Complaint form](docs/screenshots/01_complaint_form.png)

The citizen enters name, phone, ward, location, problem type and description, then uploads a photo. Location can be typed, picked on the map, or read from the photo's EXIF GPS when present.

### Step 2: AI analyses the photo

![AI analysis](docs/screenshots/02_ai_analysis.png)

Sample output for a medical-waste complaint (sample report R003, near a hospital):

```json
{
  "application_id": "KG-2025-0003",
  "model": "Qwen/Qwen2.5-VL-7B-Instruct",
  "fill_level_pct": 85,
  "overflowing": false,
  "waste_type": "mixed",
  "hazards": [
    {"type": "medical_waste", "evidence": "syringes and needles visible at top of bin", "severity": "high"},
    {"type": "sharps", "evidence": "exposed needles within reach of the public", "severity": "high"}
  ],
  "bin_condition": "intact",
  "priority": "emergency",
  "recommended_action": "Dispatch trained crew with sharps protocol and biomedical waste container. Do not mix with general collection.",
  "confidence": 0.88
}
```

### Step 3: Application is created and tracked

![Status timeline](docs/screenshots/03_status_timeline.png)

```text
Application KG-2025-0003                                Priority: EMERGENCY
Ward 142 (Jayanagar)  |  Near Sagar Hospital  |  Filed 2025-01-13 11:00

  ●  Submitted          2025-01-13 11:00:04
  ●  Analyzed           2025-01-13 11:00:19   AI: medical waste, sharps
  ●  Sent to Office     2025-01-13 11:00:20
  ●  Under Review       2025-01-13 11:00:21
  ●  Approved           2025-01-13 11:00:51   (auto-approved, prototype)
  ●  Dispatched         2025-01-13 11:00:52   Truck T01 / Rajesh Kumar
  ◐  En Route           ETA 6 min
  ○  Arrived
  ○  Cleaning
  ○  Completed
```

### Step 4: Officer reviews (prototype)

![Officer dashboard](docs/screenshots/04_officer_dashboard.png)

The officer sees the photo, the AI JSON, urgency and citizen contact, with **Approve / Reject / Hold** buttons. In demo mode the app approves automatically after 30 seconds.

### Step 5: Truck tracking (simulated)

![Truck tracking](docs/screenshots/05_truck_tracking.png)

A Folium map on OpenStreetMap shows the depot, the truck marker advancing along the route, and the target bin.

### Step 6: Fuel report

![Fuel report](docs/screenshots/06_fuel_report.png)

Sample per-trip result for Truck T01 (11.2 km optimized vs 18.5 km fixed route):

```text
TRIP FUEL REPORT                         Truck T01  |  Mileage 6.0 km/L  |  Diesel ₹89.00/L

                     Optimized (KachraGrid)      Old fixed route        Saved
 Distance                      11.2 km                18.5 km             7.3 km  (39%)
 Diesel used                   1.87 L                 3.08 L              1.22 L
 Cost                          ₹166                   ₹274                ₹108
```

---

## ✨ Features

| Feature | Description | Status | AI Model Used |
|---|---|---|---|
| 📸 Photo Analysis | Fill level (0 to 120%), waste type, condition from a bin photo | ✅ Real | Qwen2.5-VL-7B-Instruct |
| ⚠️ Hazard Detection | Flags medical waste, sharps, fire, smoke, chemicals, rubble | ✅ Real | Qwen2.5-VL-7B-Instruct |
| 📝 Complaint Form | Name, phone, ward, location, problem type, description | ✅ Real | None |
| 🔎 Application Tracking | Unique ID `KG-YYYY-XXXX`, live status timeline | ✅ Real | None |
| 🧠 Fill Prediction | Estimates when a bin will be full from history, area type and weather | ✅ Real (on sample data) | Llama-3.1-8B-Instruct |
| 🎙️ Voice Complaints | Speak the complaint instead of typing | ✅ Real | Whisper-small |
| 🌐 Multilingual Support | Hindi, Kannada, English and Hinglish in; English for officers | ✅ Real | NLLB-200 distilled 600M |
| 🏛️ Office Review | Approve / reject / hold, work-order generation | 🧪 Prototype | Llama-3.1-8B (summaries) |
| 🚛 Truck Dispatch | Assign nearest truck with enough capacity | 🧪 Prototype | None (rules) |
| 📍 Live Tracking | Dispatched, En Route, Arrived, Cleaning, Completed | 🧪 Prototype | None (simulation) |
| ⛽ Fuel Calculation | Distance ÷ mileage × ₹/L, savings vs fixed route | ✅ Real math, simulated trips | None |
| 📊 Monthly Reports | Per-truck totals, savings, projections | ✅ Real math, simulated trips | None |
| 📲 Telegram Alerts | Optional status notifications | ✅ Real (optional) | None |

---

## 🧰 Tech Stack

Every component is free. AI models are downloaded straight from the **Hugging Face Hub** and run locally.

| Component | Technology | Cost | Why Open-Source |
|---|---|---|---|
| Frontend | Streamlit | ₹0 | Fast Python UI, no JS build chain |
| Vision AI | `Qwen/Qwen2.5-VL-7B-Instruct` | ₹0 | Photos of medical waste and homes stay on-premises |
| Text AI | `meta-llama/Llama-3.1-8B-Instruct` | ₹0 | Municipal data stays under municipal control |
| Speech-to-text | `openai/whisper-small` | ₹0 | Voice notes contain personal information |
| Translation | `facebook/nllb-200-distilled-600M` | ₹0 | Works offline in flood or outage conditions |
| AI library | `transformers` + `torch` + `bitsandbytes` | ₹0 | Standard, inspectable, swappable |
| Database | SQLite (prototype) / PostgreSQL (production) | ₹0 | Zero-setup now, scalable later |
| Maps | Folium + OpenStreetMap | ₹0 | No API key, no billing |
| Charts | Streamlit native charts + Plotly | ₹0 | Interactive without a BI licence |
| Messaging | Telegram Bot API (optional) | ₹0 | Free, works on low-end phones |
| Fuel tracking | Custom Python module | ₹0 | Transparent, auditable formula |
| Packaging | Docker Compose (optional) | ₹0 | Reproducible deployment |

### ⚖️ Licences of the models (read before deploying)

| Model | Licence | Implication |
|---|---|---|
| Qwen2.5-VL-7B-Instruct | Apache 2.0 | Permissive, commercial use allowed |
| whisper-small | MIT | Permissive |
| Llama-3.1-8B-Instruct | Llama 3.1 Community Licence | **Open-weight, not OSI open-source.** Gated: accept Meta's terms on Hugging Face. Usage restrictions apply |
| nllb-200-distilled-600M | CC-BY-NC 4.0 | **Non-commercial.** Confirm your deployment qualifies, or substitute another translation model |

The KachraGrid **source code** is Apache 2.0. Model weights keep their own licences.

---

## 🏗️ Architecture

```text
                          ┌─────────────────────────────┐
                          │          CITIZEN            │
                          │   browser / phone / voice   │
                          └──────────────┬──────────────┘
                                         │
 ════════════ REAL ══════════════════════▼══════════════════════════════════════════
                          ┌─────────────────────────────┐
                          │       STREAMLIT APP         │
                          │  complaint form · tracking  │
                          │  officer view · dashboards  │
                          └───┬──────────┬───────────┬──┘
                              │          │           │
          ┌───────────────────▼──┐  ┌────▼─────┐  ┌──▼────────────────────┐
          │   AI LAYER (local)   │  │ MAPS     │  │ DATABASE              │
          │   Hugging Face       │  │ Folium + │  │ SQLite  (prototype)   │
          │                      │  │ OSM      │  │ PostgreSQL (prod)     │
          │ Qwen2.5-VL  photo    │  └──────────┘  │                       │
          │ Llama-3.1   text     │                │ applications          │
          │ Whisper     voice    │◀──────────────▶│ analyses              │
          │ NLLB-200    translate│                │ bins · trucks         │
          └──────────────────────┘                │ trips · fuel_logs     │
                                                  └──────────┬────────────┘
 ═════════ PROTOTYPE / SIMULATED ═════════════════════════════│═══════════════════
                                                              │
   ┌──────────────────────┐   ┌──────────────────────┐   ┌────▼─────────────────┐
   │ OFFICE SIMULATOR     │──▶│ DISPATCH SIMULATOR   │──▶│ FUEL TRACKING MODULE │
   │ approve / reject /   │   │ truck choice + state │   │ km ÷ mileage × ₹/L   │
   │ hold · auto 30 s     │   │ machine + movement   │   │ savings · monthly    │
   └──────────────────────┘   └──────────────────────┘   └────┬─────────────────┘
                                                              │
                                                  ┌───────────▼────────────┐
                                                  │ DASHBOARD (Plotly)     │
                                                  │ trips · km · ₹ · saved │
                                                  └────────────────────────┘

   Optional: Telegram Bot API for status notifications to citizen and officer.
```

### Design principles

- **Local inference.** No image or text is sent to a third-party AI API.
- **One database, thin layers.** Streamlit pages call plain Python modules; modules call the DB.
- **Honest simulation.** Simulated parts are isolated in `simulation/` and clearly labelled in the UI.
- **Swappable models.** Model IDs and quantisation live in `config.yaml`.

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Detail |
|---|---|
| Python | 3.10 or newer |
| RAM | 16 GB minimum |
| Disk | **40 GB free** (about 35 GB of model downloads plus cache) |
| GPU | NVIDIA with 6 GB+ VRAM strongly recommended |
| Accounts | Hugging Face account (free) with access to Llama 3.1 granted |

> **Llama 3.1 is gated.** Open the model page on Hugging Face, accept Meta's licence, create a read token, then run `huggingface-cli login`.

### Install

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/kachragrid.git
cd kachragrid

# 2. Create an isolated environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Authenticate with Hugging Face (needed once for the gated Llama model)
huggingface-cli login

# 5. Download all models (one time, about 35 GB)
python scripts/download_models.py

# 6. Seed the Ward 142 sample data
python scripts/seed_database.py

# 7. Run the app
streamlit run app.py
```

Open `http://localhost:8501`.

![Running app](docs/screenshots/00_running_app.png)

### First-run time

| Phase | Time |
|---|---|
| Install dependencies | 3 to 5 min |
| Model download (about 35 GB) | 15 to 60+ min, depends on bandwidth |
| First model load | 1 to 3 min |
| Later launches | under 1 min |

After the first download, the system runs **fully offline**.

### Optional: Docker Compose

```bash
docker compose up --build
```

Mount your Hugging Face cache (`~/.cache/huggingface`) into the container to avoid re-downloading.

### Optional: Telegram notifications

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC..."     # from @BotFather
export TELEGRAM_OFFICER_CHAT_ID="..."
```

### Hardware tiers

| Tier | RAM | GPU | Disk | Expected latency |
|---|---|---|---|---|
| Minimum | 16 GB | none | 40 GB | slow, 30 s or more per response |
| Recommended | 16 GB | NVIDIA 6 GB+ | 40 GB | about 5 s |
| Best | 24 GB | NVIDIA 8 GB+ | 50 GB | about 2 s |
| Free cloud | 24 GB (Oracle Always Free, 4 ARM cores) | none | 50 GB | CPU speed |

> **Caveats.** `bitsandbytes` 4-bit loading targets NVIDIA CUDA. On CPU-only or ARM machines, use `quantization: none` with smaller or alternative models, or expect long response times and higher RAM use. The latency figures are targets; benchmark on your hardware with `python -m eval.latency`.

---

## 🤖 Model Details

| Model | Hugging Face ID | Download size | Purpose | Memory at 4-bit |
|---|---|---|---|---|
| Vision | `Qwen/Qwen2.5-VL-7B-Instruct` | about 16 GB | Photo analysis | about 6 GB VRAM |
| Text | `meta-llama/Llama-3.1-8B-Instruct` | about 16 GB | Summaries, prediction reasoning, replies | about 5.5 GB VRAM |
| Voice | `openai/whisper-small` | about 1 GB | Voice complaints | about 1 GB |
| Translation | `facebook/nllb-200-distilled-600M` | about 2.5 GB | Hindi / Kannada to English and back | about 1.5 GB |
| **Total** | | **about 35 GB** | | |

### Low-memory loading

Weights are downloaded in 16-bit and **quantised to 4-bit as they load**, which shrinks memory use. It does not shrink the download.

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit NF4 quantisation: roughly a quarter of the 16-bit memory footprint
quant_cfg = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

llm = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=quant_cfg,
    device_map="auto",
)
```

### Automatic download

Models are fetched from the Hugging Face Hub the first time they are needed (or ahead of time with `scripts/download_models.py`) and cached locally.

### Memory strategy on small GPUs

On a 6 GB GPU the app loads **one large model at a time**: the vision model for photo analysis, then it unloads and the text model loads for summaries. This is why a request touching both takes longer on small hardware.

---

## ⛽ Fuel Tracking

Fuel tracking is **real arithmetic applied to simulated trips**.

### Formula

```text
Diesel used (L)  =  Distance (km)  ÷  Truck mileage (km/L)
Trip cost (₹)    =  Diesel used (L)  ×  Diesel rate (₹/L)

Savings          =  Old fixed-route value  −  Optimized value     (km, L and ₹)
```

```python
def trip_fuel(distance_km: float, mileage_km_per_l: float, diesel_rate: float = 89.0) -> dict:
    """Return diesel litres and rupee cost for one trip."""
    litres = distance_km / mileage_km_per_l          # diesel consumed
    return {"litres": litres, "cost_inr": litres * diesel_rate}
```

### Fleet and rates

| Truck | Capacity | Mileage | Driver |
|---|---|---|---|
| T01 | 8 tonne | 6.0 km/L | Rajesh Kumar |
| T02 | 8 tonne | 5.5 km/L | Suresh Reddy |
| T03 | 5 tonne | 7.0 km/L | Manjunath |

Diesel rate: **₹89 per litre** (configurable in `config.yaml`).

### Sample monthly report: Truck T01, January

| Metric | Optimized (KachraGrid) | Old fixed route | Savings |
|---|---|---|---|
| Trips | 22 | 22 | none |
| Distance | 246 km | 407 km | **161 km (39.6%)** |
| Diesel | 41.0 L | 67.8 L | **26.8 L** |
| Cost | ₹3,649 | ₹6,034 | **₹2,385 / month** |
| Average per trip | ₹166 | ₹274 | ₹108 |
| Average per km | ₹14.83 | ₹14.83 | none |

> Cost per km is identical because the same truck burns the same fuel per km. **The saving comes from driving fewer kilometres**, which is exactly what demand-based routing changes.

### Projections (simple linear extrapolation)

| Scope | Assumption | Projected saving |
|---|---|---|
| One truck, one year | T01 result repeated for 12 months | about ₹28,600, 322 L, 1,932 km |
| City fleet of 50 trucks | All trucks save like T01 | about ₹14.3 lakh per year, 16,100 L of diesel |

> **Caveats.** The 50-truck figure ignores differences in mileage, route length and load, and assumes the T01 saving generalises. Treat it as an order-of-magnitude estimate, then replace it with measured data from a real pilot.

### Why it matters

Fuel is a recurring, line-item cost in municipal budgets. Less diesel burned also means lower emissions and less wear on vehicles. A transparent per-trip ledger gives officers an auditable number instead of an estimate.

---

## 📋 Application Workflow

```text
 Citizen submits form + photo
          │
          ▼
   ┌─────────────┐
   │  Submitted  │  application ID KG-YYYY-XXXX issued
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  Analyzed   │  AI result stored (fill %, type, hazards, priority)
   └──────┬──────┘
          ▼
   ┌──────────────────┐
   │  Sent to Office  │
   └──────┬───────────┘
          ▼
   ┌──────────────┐        ┌────────────┐
   │ Under Review │───────▶│  Rejected  │  reason shown to citizen
   └──────┬───────┘        └────────────┘
          │ ⏸ Hold: stays here until an officer acts
          ▼
   ┌──────────────┐
   │   Approved   │  work order generated
   └──────┬───────┘
          ▼
   Dispatched ▶ En Route ▶ Arrived ▶ Cleaning ▶ Completed
```

### Status codes

| Code | Meaning | Set by | Real or simulated |
|---|---|---|---|
| `SUBMITTED` | Complaint received, ID issued | System | Real |
| `ANALYZED` | AI analysis stored | System | Real |
| `SENT_TO_OFFICE` | Queued for review | System | Real |
| `UNDER_REVIEW` | Officer is looking at it | Officer / simulator | Simulated |
| `APPROVED` | Work order issued | Officer / simulator | Simulated |
| `REJECTED` | Not actionable, reason recorded | Officer / simulator | Simulated |
| `DISPATCHED` | Truck assigned | Dispatcher | Simulated |
| `EN_ROUTE` | Truck travelling | Simulator | Simulated |
| `ARRIVED` | Truck at the bin | Simulator | Simulated |
| `CLEANING` | Crew working | Simulator | Simulated |
| `COMPLETED` | Bin cleared, fuel logged | Simulator | Simulated |

### Priority rules

| Priority | Triggers | Target response (design goal) |
|---|---|---|
| Emergency | Fire, sharps, medical waste, chemical hazard | Immediate |
| High | Fill above 100%, near hospital / school / market | Same day |
| Medium | Fill 70 to 100% | Within 24 h |
| Low | Fill below 70% | Next scheduled pass |

### Prototype simulation

`DEMO_MODE=true` (default) auto-approves after **30 seconds** and advances truck states on a short timer so the full flow can be shown in minutes. Set `DEMO_MODE=false` to require manual officer action.

<details>
<summary><b>Application data model (click to expand)</b></summary>

```sql
-- One row per citizen complaint
CREATE TABLE applications (
    application_id   TEXT PRIMARY KEY,          -- KG-2025-0001
    citizen_name     TEXT NOT NULL,
    phone_masked     TEXT NOT NULL,             -- stored masked, e.g. +9198765XXXX
    ward             INTEGER NOT NULL,
    lat              REAL, lng REAL,
    problem_type     TEXT NOT NULL,
    description      TEXT,
    photo_path       TEXT,
    status           TEXT NOT NULL DEFAULT 'SUBMITTED',
    priority         TEXT,
    created_at       TEXT NOT NULL
);

-- AI output for each application
CREATE TABLE analyses (
    application_id   TEXT REFERENCES applications(application_id),
    fill_level_pct   REAL, waste_type TEXT,
    hazards_json     TEXT, confidence REAL,
    raw_json         TEXT, model TEXT, analyzed_at TEXT
);

-- Fuel ledger per completed trip
CREATE TABLE fuel_logs (
    trip_id TEXT PRIMARY KEY, truck_id TEXT, trip_date TEXT,
    distance_km REAL, mileage_kmpl REAL, litres REAL, cost_inr REAL,
    old_distance_km REAL, old_litres REAL, old_cost_inr REAL
);
```

</details>

---

## 🗂️ Sample Data

Included under `data/sample/`. Everything is synthetic or approximate.

| Dataset | Content |
|---|---|
| Bins | **25 bins** around Jayanagar, Bangalore (**Ward 142**) with GPS coordinates, area type and capacity |
| Trucks | **3 trucks**: T01 (8 T, 6 km/L), T02 (8 T, 5.5 km/L), T03 (5 T, 7 km/L) |
| Drivers | Rajesh Kumar, Suresh Reddy, Manjunath |
| Complaints | **5 sample reports** in Hinglish and English with photos (overflow, fire, medical waste, missed pickup, construction debris) |
| Collection history | **7 days** of pickups for 5 sample bins, including missed pickups |
| Fuel logs | Trip records with savings against the fixed route |

Area types: market, residential, commercial, hospital, slum, school.

> Coordinates approximate Jayanagar and are **not** official BBMP bin locations.

### Replace with your city's data

1. Export your bins to `data/sample/bins.csv` (`bin_id, lat, lng, area_type, capacity_kg, ward`).
2. Update `data/sample/trucks.csv` with your fleet, capacities and mileage.
3. Set the ward, city centre and diesel rate in `config.yaml`.
4. Run `python scripts/seed_database.py --reset`.

---

## 📁 Project Structure

```text
kachragrid/
├── app.py                        # ⭐ Streamlit entry point
├── config.yaml                   # Model IDs, diesel rate, mileage, DEMO_MODE
├── requirements.txt
├── docker-compose.yml            # Optional container setup
├── LICENSE                       # Apache 2.0
├── README.md
│
├── pages/                        # Streamlit multipage UI
│   ├── 1_File_Complaint.py       # Citizen form + photo upload
│   ├── 2_Track_Application.py    # Status timeline
│   ├── 3_Officer_Dashboard.py    # Review queue (prototype)
│   ├── 4_Truck_Tracking.py       # Folium live map (simulated)
│   └── 5_Fuel_Reports.py         # Trip and monthly reports
│
├── kachragrid/                   # Core Python package
│   ├── ai/
│   │   ├── vision.py             # ⭐ Qwen2.5-VL bin photo analysis
│   │   ├── text.py               # Llama-3.1 summaries and reasoning
│   │   ├── voice.py              # Whisper-small transcription
│   │   ├── translate.py          # NLLB-200 translation
│   │   ├── model_loader.py       # 4-bit loading, load/unload management
│   │   └── prompts/              # System and user prompt templates
│   ├── db.py                     # SQLite / PostgreSQL access
│   ├── applications.py           # Create, update, status transitions
│   ├── fuel.py                   # ⭐ Fuel and savings calculations
│   └── notify.py                 # Optional Telegram notifications
│
├── simulation/                   # Everything PROTOTYPE lives here
│   ├── office.py                 # Auto-approve after 30 s
│   ├── dispatch.py               # Nearest-truck assignment
│   └── tracker.py                # Truck state machine and movement
│
├── skills/
│   └── waste-bin-analyzer/       # Agent Skill
│       ├── skill.json
│       └── examples/
│
├── eval/                         # Evaluation harness
│   ├── fill_prediction.py        # ⭐ Fill prediction benchmark
│   ├── photo_analysis.py
│   ├── route_savings.py
│   ├── cases/                    # Test cases
│   └── results/
│
├── data/
│   ├── sample/                   # Ward 142 dataset + sample photos
│   └── uploads/                  # Citizen uploads (git-ignored)
│
├── scripts/
│   ├── download_models.py        # Pull all models from Hugging Face
│   └── seed_database.py          # Load sample data
│
├── tests/
└── docs/
    └── screenshots/
```

---

## 🏆 Hackathon Requirements Compliance

| Requirement | Status | Detail |
|---|---|---|
| Open-source AI | ✅ | Llama 3.1 and Qwen2.5-VL from Hugging Face (open-weight; see licence table) |
| Public GitHub repository | ✅ | Apache 2.0 licensed |
| Agent Skill | ✅ | `waste-bin-analyzer` in `skills/waste-bin-analyzer/skill.json` |
| Original evaluation harness | ✅ | Fill-prediction benchmark, photo-analysis accuracy, route-savings checks in `eval/` |
| Open-weight models are essential | ✅ | See below |

### Agent Skill: `waste-bin-analyzer`

```json
{
  "name": "waste-bin-analyzer",
  "description": "Analyzes a photo of a waste bin and returns fill level, waste type, hazards and priority.",
  "input": {"image": "bytes", "location": "optional lat,lng", "text": "optional citizen description"},
  "output": {"fill_level_pct": "number", "waste_type": "string", "hazards": "array", "priority": "string"}
}
```

### Evaluation harness

| Suite | Metric |
|---|---|
| Fill prediction | Mean absolute error in percentage points; share within 10 points |
| Photo analysis | Waste-type accuracy; hazard recall (missing a needle is the costly error) |
| Route savings | Distance and fuel saved versus the fixed route |
| Model comparison | Llama vs Phi vs Qwen on identical cases |

```bash
python -m eval.fill_prediction      # benchmark results written to eval/results/
```

### Why open-weight models are essential here

| Reason | Why it matters |
|---|---|
| 🏥 **Medical and hazardous waste photos** | Images can show patient materials, hospital premises and people. Sending them to an external API is a privacy risk |
| 📱 **Citizen data** | Phone numbers, names and home locations are personal data under India's data-protection regime |
| 🏛️ **Government sovereignty** | Municipal records should remain under municipal control, not a foreign vendor's cloud |
| 💰 **Cost at scale** | Per-call API pricing across a population of hundreds of millions of citizens is unaffordable for municipal budgets. Local inference has no per-call cost |
| 🌧️ **Resilience** | Floods and network outages are exactly when waste problems spike. Local models keep working offline |

---

## 📈 Impact Metrics

> These are **design targets and hypotheses**, not measured results. KachraGrid is a prototype. The pilot phase exists to replace each target with a measurement.

| Metric | Before (typical today) | After KachraGrid (target) | How it will be measured |
|---|---|---|---|
| Complaint response time | Days, often untracked | Same day for high / emergency priority | Timestamps in `applications` |
| Fuel cost per truck | Fixed-route baseline | Reduction from fewer kilometres (demo route: 39%) | `fuel_logs` before vs after |
| Overflowing bins at end of shift | Unknown | Zero bins above 100% in pilot ward | Fill estimates and photos |
| Citizen feedback | None | Status visible for every complaint | Share of complaints with a tracked ID |
| Citizen satisfaction | Not measured | Survey in pilot ward | Post-resolution rating |
| Disease incidence | Not linked to waste data | Track alongside ward health data | Partner with ward health office |
| Swachh Survekshan ranking | Current city rank | Improved citizen-feedback and processing indicators | Official survey results |

Only the fuel row is currently backed by (simulated) calculations. Every other row requires pilot data.

---

## 🛣️ Roadmap

| Phase | Scope | Status |
|---|---|---|
| **1. Hackathon prototype** | Real citizen flow and AI analysis; simulated office, dispatch and tracking; fuel math | 🟢 Current |
| **2. Ward pilot** | One ward (Ward 142 candidate) with real bin locations, real officers, manual review, measured results | ⚪ Planned |
| **3. Municipal integration** | Connect to BBMP / BMC complaint and work-order systems and APIs | ⚪ Planned |
| **4. IoT and real GPS** | Bin fill sensors, truck GPS telemetry, replace simulated tracking | ⚪ Planned |
| **5. City-wide deployment** | Multi-ward rollout, PostgreSQL, role-based access, audit logs | ⚪ Planned |

Also planned: stronger Kannada support, WhatsApp channel, model-licence review for production, CI pipeline.

---

## 🤝 Contributing

Contributions are welcome, especially from civic-tech practitioners, sanitation engineers and municipal staff.

```bash
git checkout -b feature/your-feature
# make changes, add tests
pytest
git commit -m "Describe your change"
git push origin feature/your-feature     # then open a pull request
```

- Read `CODE_OF_CONDUCT.md` (Contributor Covenant) before participating.
- Use the issue templates in `.github/ISSUE_TEMPLATE/`: **Bug report**, **Feature request**, **New city dataset**.
- Keep every dependency free. No paid or proprietary APIs.
- Document new configuration in `config.yaml` and this README.

Good first issues: additional languages, new ward datasets, photo-analysis test cases, UI accessibility.

---

## 👥 Team

| Name | Role | Links |
|---|---|---|
| [Name] | [Role] | [GitHub / LinkedIn] |
| [Name] | [Role] | [GitHub / LinkedIn] |

---

## 📄 License

Source code is released under the **Apache License 2.0**.

- ✅ Use, modify and distribute freely, including commercially
- ✅ Includes an explicit patent grant
- ⚠️ Keep the licence and notice files, and state significant changes
- ⚠️ **Model weights carry their own licences** (Llama 3.1 Community Licence, CC-BY-NC for NLLB). See the [model licence table](#️-licences-of-the-models-read-before-deploying)

See [`LICENSE`](LICENSE) for the full text.

---

## 🙏 Acknowledgments

- **[Hugging Face](https://huggingface.co)** for the model hub and `transformers`
- **[Meta AI](https://ai.meta.com)** for Llama 3.1 and NLLB-200
- **[Qwen team, Alibaba Cloud](https://github.com/QwenLM)** for Qwen2.5-VL
- **[OpenAI](https://github.com/openai/whisper)** for the open Whisper weights
- **[OpenStreetMap](https://www.openstreetmap.org)** contributors and **[Folium](https://python-visualization.github.io/folium/)**
- **[Streamlit](https://streamlit.io)** for the rapid UI framework
- **BBMP open data** and the sanitation workers who keep Indian cities running

---

<div align="center">

**KachraGrid** · every bin emptied when it needs to be · every citizen heard

*Prototype built at [Hackathon Name]*

</div>
