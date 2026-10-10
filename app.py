"""
================================================================
KachraGrid v2 — AI Waste Complaint & Logistics System
Ward 142 — Jayanagar, Bangalore Municipal Prototype
================================================================
"""

import os
import random
from datetime import datetime
from PIL import Image
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

import config
import database
import ai_models
from fuel_tracker import FuelTracker
import simulation

# ----------------- Page Configuration ----------------- #
st.set_page_config(
    page_title="KachraGrid v2 | Bangalore Ward 142",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- Custom Styling ----------------- #
st.markdown("""
<style>
    /* Modern Civic Dashboard Aesthetics */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        color: #F8FAFC;
    }
    .main-header h1 {
        color: #38BDF8;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .main-header p {
        color: #94A3B8;
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-critical { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; }
    .badge-high { background: rgba(245, 158, 11, 0.2); color: #F59E0B; border: 1px solid #F59E0B; }
    .badge-medium { background: rgba(59, 130, 246, 0.2); color: #3B82F6; border: 1px solid #3B82F6; }
    .badge-low { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid #10B981; }

    .card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .timeline-item {
        border-left: 2px solid #38BDF8;
        padding-left: 1.2rem;
        margin-left: 0.5rem;
        margin-bottom: 1.2rem;
        position: relative;
    }
    .timeline-item::before {
        content: "";
        position: absolute;
        left: -6px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #38BDF8;
    }
    .stat-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38BDF8;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

fuel_tracker = FuelTracker()

# ----------------- Sidebar Navigation & Controls ----------------- #
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=300&auto=format&fit=crop&q=80", use_container_width=True)
    st.title("♻️ KachraGrid v2")
    st.caption("Govt. of Karnataka | BBMP Ward 142 (Jayanagar)")

    page = st.radio(
        "Navigation",
        [
            "📝 1. Citizen Complaint Form",
            "🔍 2. Application Status Tracker",
            "🏛️ 3. Municipal Officer Dashboard",
            "🚚 4. Live Truck Tracking & Map",
            "⛽ 5. Fuel & Diesel Dashboard",
        ],
        index=0
    )

    st.markdown("---")
    st.subheader("⚙️ AI & Prototype Controls")

    ai_mode_choice = st.toggle("Fast AI Mode (No VRAM lag)", value=True, help="Toggle between instant computer vision heuristics and heavy Hugging Face transformers pipeline.")
    ai_models.set_ai_mode(ai_mode_choice)
    st.caption(f"Engine: {'⚡ Smart Neural CV (Instant)' if ai_mode_choice else '🤖 HuggingFace Local Pipeline'}")

    # Simulation Trigger
    st.markdown("---")
    st.write("**Simulation Engine**")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        if st.button("⏩ Advance Step", use_container_width=True, help="Moves simulated trucks 2 mins along route"):
            res = simulation.advance_simulation_tick()
            st.toast("Simulation step advanced!", icon="🚚")
            st.rerun()
    with col_sim2:
        if st.button("⏱️ Auto-SLA", use_container_width=True, help="Simulate 30-min auto-approval sweep"):
            approved = simulation.run_auto_approval_check(minutes_threshold=0)
            if approved:
                st.toast(f"Auto-approved {len(approved)} pending grievances!", icon="✅")
                st.rerun()
            else:
                st.toast("No pending complaints awaiting SLA action.", icon="ℹ️")

    # Quick Ward Metrics
    st.markdown("---")
    st.markdown("**Ward 142 Quick Stats**")
    bins_data = database.get_all_bins()
    full_bins = sum(1 for b in bins_data if b["current_fill_pct"] >= 80)
    st.markdown(f"- **Total Bins:** 25 units")
    st.markdown(f"- **Critical (>80%):** :red[{full_bins} bins]")
    st.markdown(f"- **Diesel Benchmark:** ₹{config.DIESEL_RATE_PER_LITER}/L")
    st.markdown(f"- **Active Fleet:** 3 Compactors")

    # Citizen Multilingual Assistant in Sidebar
    st.markdown("---")
    with st.expander("💬 Sahaya AI Citizen Chat"):
        lang = st.selectbox("Language / ಭಾಷೆ", ["English", "Kannada", "Hindi"], index=0)
        user_msg = st.text_input("Ask a question about bins or segregation:")
        if user_msg:
            reply = ai_models.citizen_chat_assistant(user_msg, language=lang)
            st.info(reply)


# Header Banner
st.markdown("""
<div class="main-header">
    <h1>♻️ KachraGrid v2 <span style="font-size: 1rem; color: #10B981; background: rgba(16, 185, 129, 0.15); padding: 2px 10px; border-radius: 999px; border: 1px solid #10B981;">Ward 142 • Bangalore</span></h1>
    <p>Open-Source Civic AI Waste Redressal & Intelligent Municipal Logistics System</p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: CITIZEN COMPLAINT FORM
# ==============================================================================
if "Citizen Complaint" in page:
    st.subheader("📝 Citizen Waste Grievance Registration")
    st.markdown(
        "Report an overflowing bin, illegal dumping, or unattended municipal waste in **Ward 142 (Jayanagar)**. "
        "Upload a photo to get **instant AI waste analysis** and a verifiable **Application ID**."
    )

    bins_list = database.get_all_bins()
    bin_options = {f"{b['bin_id']} — {b['landmark']} ({b['zone_type'].title()}, Current Fill: {b['current_fill_pct']}%)": b['bin_id'] for b in bins_list}

    col_form, col_preview = st.columns([1.1, 0.9], gap="large")

    with col_form:
        with st.form("citizen_complaint_form", clear_on_submit=False):
            st.markdown("##### 1. Citizen & Location Details")
            c_name = st.text_input("Your Full Name *", placeholder="e.g. Priya Sharma")
            c_phone = st.text_input("Mobile Number (10 digits) *", placeholder="e.g. 9876543210")

            selected_bin_str = st.selectbox("Select Nearest Ward 142 Bin *", list(bin_options.keys()))
            selected_bin_id = bin_options[selected_bin_str]

            c_loc_desc = st.text_area("Specific Landmark / Spot Details", placeholder="e.g. Near 4th Block Vegetable market corner, spilling onto walkway")

            st.markdown("##### 2. Grievance Nature")
            prob_type = st.selectbox(
                "Problem Type *",
                [
                    "Overflow (>90% full)",
                    "Not collected for >24 hours",
                    "Foul Odor / Pest Breeding",
                    "Hazardous / Biomedical waste mixed",
                    "Animal Menace / Stray Dogs",
                    "Illegal Commercial Dumping"
                ]
            )

            st.markdown("##### 3. Bin Photo Evidence (REAL AI Analysis)")
            uploaded_file = st.file_uploader("Upload Bin Photo (JPG/PNG)", type=["jpg", "jpeg", "png"])

            submit_btn = st.form_submit_button("🚀 Submit Complaint to Municipal Office", use_container_width=True)

    with col_preview:
        st.markdown("##### 🤖 Live AI Vision Inspection")

        ai_results = None
        saved_photo_path = None

        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Grievance Photo", use_container_width=True)

            with st.spinner("AI evaluating fill level, waste composition & sanitary urgency..."):
                ai_results = ai_models.analyze_bin_photo(img)

                # Save file locally
                filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
                saved_photo_path = os.path.join(config.UPLOAD_DIR, filename)
                img.save(saved_photo_path)
        else:
            st.info("💡 Upload an image to trigger Hugging Face Qwen2.5-VL / Local Neural CV analysis.")
            st.image("https://images.unsplash.com/photo-1605600659908-0ef719419d41?w=500&auto=format&fit=crop&q=80", caption="Sample Municipal Waste Stream", use_container_width=True)

        if ai_results:
            st.markdown("---")
            urgency_class = f"badge-{ai_results['urgency'].lower()}"
            st.markdown(f"**Urgency Assessment:** <span class='badge-pill {urgency_class}'>{ai_results['urgency']}</span>", unsafe_allow_html=True)

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Estimated Fill", f"{ai_results['fill_pct']}%", delta="Critical Overflow" if ai_results['overflow_detected'] else "Within Bounds")
            with col_m2:
                st.metric("Est. Payload", f"{ai_results['est_weight_kg']} kg")

            st.write(f"**Detected Category:** `{ai_results['waste_type']}`")
            st.caption(f"**Diagnostic Notes:** {ai_results['reasoning']}")

    # Form Submission Handler
    if submit_btn:
        if not c_name or not c_phone:
            st.error("Please provide both citizen name and contact number.")
        else:
            # Generate official ID
            app_id = f"KG-2025-{random.randint(100000, 999999)}"

            # If no photo uploaded, use text metadata predictor
            if not ai_results:
                bin_meta = database.get_bin_by_id(selected_bin_id)
                fill_p = ai_models.predict_fill_level_from_metadata(
                    bin_meta["capacity_kg"], prob_type, bin_meta["zone_type"]
                )
                ai_results = {
                    "fill_pct": fill_p,
                    "waste_type": "Reported via Citizen Description",
                    "urgency": "HIGH" if fill_p >= 85 else "MEDIUM",
                    "reasoning": f"Synthesized from citizen grievance: {prob_type}"
                }

            database.create_application(
                app_id=app_id,
                name=c_name,
                phone=c_phone,
                ward_no="142",
                bin_id=selected_bin_id,
                location_desc=c_loc_desc,
                problem_type=prob_type,
                photo_path=saved_photo_path,
                ai_fill_pct=ai_results["fill_pct"],
                ai_waste_type=ai_results["waste_type"],
                ai_urgency=ai_results["urgency"],
                ai_notes=ai_results["reasoning"]
            )

            st.success(f"🎉 Grievance registered successfully! Application ID: **{app_id}**")
            st.balloons()
            st.info(f"Your application has been routed to the BBMP Jayanagar Municipal Sub-Division. You can track progress on the **Status Tracker** tab using ID `{app_id}`.")


# ==============================================================================
# PAGE 2: APPLICATION STATUS TRACKER
# ==============================================================================
elif "Status Tracker" in page:
    st.subheader("🔍 Application Status & Live Redressal Timeline")
    st.markdown("Track the status of citizen complaints through the municipal verification and truck dispatch pipeline.")

    all_apps = database.get_all_applications()
    app_id_list = [a["application_id"] for a in all_apps]

    c_search1, c_search2 = st.columns([1, 2])
    with c_search1:
        search_query = st.text_input("Enter Application ID", placeholder="e.g. APP-001 or KG-2025-XXXXXX")
    with c_search2:
        selected_from_list = st.selectbox("Or Pick From Recent Applications", [""] + app_id_list)

    lookup_id = search_query.strip().upper() if search_query else selected_from_list

    if not lookup_id and app_id_list:
        lookup_id = app_id_list[0]  # Default to latest

    if lookup_id:
        app_data = database.get_application_by_id(lookup_id)
        if not app_data:
            st.warning(f"No grievance record found for Application ID: {lookup_id}")
        else:
            # Display Application Banner
            status = app_data["status"]
            status_colors = {
                "PENDING": "rgba(245, 158, 11, 0.2)",
                "APPROVED": "rgba(59, 130, 246, 0.2)",
                "REJECTED": "rgba(239, 68, 68, 0.2)",
                "COMPLETED": "rgba(16, 185, 129, 0.2)",
                "HOLD": "rgba(148, 163, 184, 0.2)"
            }
            border_colors = {
                "PENDING": "#F59E0B", "APPROVED": "#3B82F6", "REJECTED": "#EF4444", "COMPLETED": "#10B981", "HOLD": "#94A3B8"
            }

            st.markdown(f"""
            <div style="background: {status_colors.get(status, '#334155')}; border: 1px solid {border_colors.get(status, '#FFF')}; border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #FFF;">Grievance Application: {app_data['application_id']}</h3>
                        <p style="margin: 4px 0 0 0; color: #CBD5E1;">Citizen: <strong>{app_data['citizen_name']}</strong> ({app_data['citizen_phone']}) | Ward 142 — {app_data['bin_id']}</p>
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: {border_colors.get(status, '#FFF')}; border: 1px solid {border_colors.get(status, '#FFF')}; padding: 4px 14px; border-radius: 20px;">
                        STATUS: {status}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_details, col_timeline = st.columns([1, 1.2], gap="large")

            with col_details:
                st.markdown("#### 📋 Grievance Dossier")
                st.markdown(f"- **Bin Landmark:** `{app_data['landmark']}`")
                st.markdown(f"- **Specific Spot:** {app_data['location_desc'] or 'N/A'}")
                st.markdown(f"- **Issue Category:** `{app_data['problem_type']}`")
                st.markdown(f"- **Reported On:** {app_data['created_at']}")

                if app_data["work_order_id"]:
                    st.markdown(f"- **Work Order Issued:** :blue-background[{app_data['work_order_id']}]")
                if app_data["assigned_truck_id"]:
                    truck_obj = next((t for t in database.get_all_trucks() if t["truck_id"] == app_data["assigned_truck_id"]), None)
                    driver_text = f"Driver: {truck_obj['driver_name']}" if truck_obj else ""
                    st.markdown(f"- **Allocated Fleet:** :green-background[Truck {app_data['assigned_truck_id']} ({driver_text})]")

                st.markdown("---")
                st.markdown("#### 🤖 AI Vision Findings")
                st.markdown(f"- **Assessed Fill Level:** {app_data['ai_fill_pct']}%")
                st.markdown(f"- **Waste Composition:** `{app_data['ai_waste_type']}`")
                urgency = app_data["ai_urgency"] or "MEDIUM"
                st.markdown(f"- **Civic Priority:** <span class='badge-pill badge-{urgency.lower()}'>{urgency}</span>", unsafe_allow_html=True)
                st.caption(f"Reasoning: {app_data['ai_notes']}")

                if app_data["photo_path"] and os.path.exists(app_data["photo_path"]):
                    st.image(app_data["photo_path"], caption="Citizen Uploaded Evidence", use_container_width=True)
                else:
                    st.caption("No photo evidence attached or sample mock reference.")

            with col_timeline:
                st.markdown("#### ⏱️ Real-Time Redressal Timeline")
                timeline_logs = database.get_status_timeline(lookup_id)

                if not timeline_logs:
                    st.info("No audit logs recorded yet.")
                else:
                    for log in timeline_logs:
                        st.markdown(f"""
                        <div class="timeline-item">
                            <strong style="color: #38BDF8;">{log['stage']}</strong>
                            <span style="font-size: 0.8rem; color: #94A3B8; margin-left: 8px;">{log['timestamp']}</span>
                            <div style="color: #F1F5F9; font-size: 0.95rem; margin-top: 2px;">{log['status_text']}</div>
                            <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 2px;">{log['details'] or ''}</div>
                        </div>
                        """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 3: MUNICIPAL OFFICER DASHBOARD
# ==============================================================================
elif "Officer Dashboard" in page:
    st.subheader("🏛️ Municipal Executive Dashboard — Ward 142")
    st.markdown("Review citizen applications, verify AI photo analysis, issue Work Orders, and dispatch compactors.")

    all_apps = database.get_all_applications()
    pending = [a for a in all_apps if a["status"] == "PENDING"]
    approved = [a for a in all_apps if a["status"] == "APPROVED"]
    rejected = [a for a in all_apps if a["status"] == "REJECTED"]
    completed = [a for a in all_apps if a["status"] == "COMPLETED"]

    # Top KPI Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #F59E0B;">{len(pending)}</div>
            <div class="stat-label">Pending Review</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #3B82F6;">{len(approved)}</div>
            <div class="stat-label">Active Work Orders</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #10B981;">{len(completed)}</div>
            <div class="stat-label">Resolved / Cleared</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #EF4444;">{len(rejected)}</div>
            <div class="stat-label">Rejected / Low Priority</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_filter = st.radio("Filter Applications", ["PENDING", "APPROVED", "COMPLETED", "REJECTED", "ALL"], horizontal=True)
    displayed_apps = database.get_all_applications(filter_status=tab_filter)

    if not displayed_apps:
        st.info(f"No applications currently in '{tab_filter}' status.")
    else:
        for app in displayed_apps:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-weight: 700; font-size: 1.1rem; color: #38BDF8;">{app['application_id']}</span>
                            <span style="margin-left: 10px; color: #94A3B8;">Citizen: <strong>{app['citizen_name']}</strong> ({app['citizen_phone']})</span>
                            <span style="margin-left: 10px;" class="badge-pill badge-{(app['ai_urgency'] or 'MEDIUM').lower()}">{app['ai_urgency'] or 'MEDIUM'}</span>
                            <div style="color: #CBD5E1; margin-top: 4px;">📍 {app['landmark']} (Bin ID: {app['bin_id']})</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 0.85rem; color: #94A3B8;">Reported: {app['created_at']}</span>
                            <div style="font-weight: 700; color: #F8FAFC; margin-top: 2px;">Status: {app['status']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_img, col_info, col_actions = st.columns([1, 1.2, 1.2])

                with col_img:
                    if app["photo_path"] and os.path.exists(app["photo_path"]):
                        st.image(app["photo_path"], caption="Grievance Evidence", use_container_width=True)
                    else:
                        st.caption("No photo attached")

                with col_info:
                    st.write(f"**Grievance:** {app['problem_type']}")
                    st.write(f"**Details:** {app['location_desc'] or 'None provided'}")
                    st.write(f"**AI Fill Level:** `{app['ai_fill_pct']}%`")
                    st.write(f"**AI Classification:** `{app['ai_waste_type']}`")
                    st.caption(f"AI Notes: {app['ai_notes']}")

                with col_actions:
                    if app["status"] == "PENDING":
                        st.markdown("**Officer Action Required:**")
                        trucks = database.get_all_trucks()
                        truck_opts = {f"{t['truck_id']} - {t['driver_name']} ({t['status']})": t['truck_id'] for t in trucks}
                        chosen_truck = st.selectbox(f"Assign Truck for {app['application_id']}", list(truck_opts.keys()), key=f"truck_{app['application_id']}")
                        officer_note_input = st.text_input("Officer Remarks", value="Approved for municipal compactor dispatch.", key=f"note_{app['application_id']}")

                        col_act1, col_act2, col_act3 = st.columns(3)
                        with col_act1:
                            if st.button("✅ Approve", key=f"appr_{app['application_id']}", use_container_width=True):
                                wo_id = f"WO-2025-{random.randint(1000, 9999)}"
                                database.update_application_status(
                                    app_id=app["application_id"],
                                    new_status="APPROVED",
                                    officer_notes=officer_note_input,
                                    work_order_id=wo_id,
                                    assigned_truck_id=truck_opts[chosen_truck]
                                )
                                st.success(f"Approved! Issued {wo_id}")
                                st.rerun()
                        with col_act2:
                            if st.button("⏸️ Hold", key=f"hold_{app['application_id']}", use_container_width=True):
                                database.update_application_status(
                                    app_id=app["application_id"],
                                    new_status="HOLD",
                                    officer_notes="Placed on administrative hold for ward supervisor check."
                                )
                                st.rerun()
                        with col_act3:
                            if st.button("❌ Reject", key=f"rej_{app['application_id']}", use_container_width=True):
                                database.update_application_status(
                                    app_id=app["application_id"],
                                    new_status="REJECTED",
                                    officer_notes="Grievance rejected: Fill volume below municipal threshold."
                                )
                                st.rerun()
                    else:
                        st.markdown(f"**Resolved Notes:**")
                        st.caption(f"{app['officer_notes'] or 'No officer remarks recorded.'}")
                        if app["work_order_id"]:
                            st.write(f"Work Order: `{app['work_order_id']}`")
                        if app["assigned_truck_id"]:
                            st.write(f"Assigned Truck: `{app['assigned_truck_id']}`")

                st.markdown("---")


# ==============================================================================
# PAGE 4: LIVE TRUCK TRACKING & MAP
# ==============================================================================
elif "Truck Tracking" in page:
    st.subheader("🚚 Live Truck Tracking & Bin Telemetry Map")
    st.markdown("Interactive OpenStreetMap of **Ward 142 (Jayanagar)** showing real-time compactor movements, bin capacities, and depot dispatch vectors.")

    bins = database.get_all_bins()
    trucks = database.get_all_trucks()

    col_map, col_fleet = st.columns([2, 1], gap="medium")

    with col_map:
        # Build Folium Map
        m = folium.Map(
            location=[config.WARD_CENTER_LAT, config.WARD_CENTER_LON],
            zoom_start=15,
            tiles="CartoDB positron"
        )

        # Mark BBMP Ward Headquarters
        folium.Marker(
            location=[simulation.DEPOT_LAT, simulation.DEPOT_LON],
            popup="<b>BBMP Ward 142 Depot HQ</b><br>Truck Staging & Maintenance",
            tooltip="BBMP Depot HQ",
            icon=folium.Icon(color="black", icon="home", prefix="fa")
        ).add_to(m)

        # Mark all 25 Bins
        for b in bins:
            fill = b["current_fill_pct"]
            if fill >= 85:
                marker_color = "red"
            elif fill >= 50:
                marker_color = "orange"
            else:
                marker_color = "green"

            popup_html = f"""
            <b>Bin {b['bin_id']}</b><br>
            {b['landmark']}<br>
            Zone: {b['zone_type'].title()}<br>
            <b>Fill: {fill}%</b> ({b['capacity_kg']} kg capacity)<br>
            Last Cleaned: {b['last_cleaned_at'] or 'Recent'}
            """
            folium.CircleMarker(
                location=[b["latitude"], b["longitude"]],
                radius=7 + (fill / 20.0),
                popup=popup_html,
                tooltip=f"{b['bin_id']}: {fill}% Full",
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.75
            ).add_to(m)

        # Mark Trucks
        for t in trucks:
            t_color = "blue" if t["status"] in ("En Route", "Cleaning") else "gray"
            folium.Marker(
                location=[t["current_lat"], t["current_lon"]],
                popup=f"<b>Truck {t['truck_id']}</b><br>Driver: {t['driver_name']}<br>Status: <b>{t['status']}</b><br>Target: {t['target_bin_id'] or 'None'}",
                tooltip=f"Truck {t['truck_id']} ({t['status']})",
                icon=folium.Icon(color=t_color, icon="truck", prefix="fa")
            ).add_to(m)

            # Draw Route Line if truck has target bin
            if t["target_bin_id"]:
                tb = next((x for x in bins if x["bin_id"] == t["target_bin_id"]), None)
                if tb:
                    folium.PolyLine(
                        locations=[[t["current_lat"], t["current_lon"]], [tb["latitude"], tb["longitude"]]],
                        color="#38BDF8",
                        weight=3,
                        dash_array="5, 10"
                    ).add_to(m)

        folium_static(m, width=780, height=540)

    with col_fleet:
        st.markdown("##### 🚛 Fleet Status")
        for t in trucks:
            st.markdown(f"""
            <div class="card">
                <div style="font-weight: 700; color: #38BDF8;">{t['truck_id']} • {t['driver_name']}</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Capacity: {t['capacity_kg']} kg | Mileage: {t['mileage_km_l']} km/L</div>
                <div style="margin-top: 4px;">Status: <strong>{t['status']}</strong></div>
                <div style="font-size: 0.85rem; color: #CBD5E1;">Target Bin: <code>{t['target_bin_id'] or 'Depot Standby'}</code></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("##### 📍 Legend")
        st.markdown("- 🔴 **Red:** Critical Fill (>85%)")
        st.markdown("- 🟠 **Orange:** Moderate Fill (50-84%)")
        st.markdown("- 🟢 **Green:** Cleared (<50%)")
        st.markdown("- 🚛 **Blue Truck:** En Route / Active")
        st.markdown("- 🏠 **Black Icon:** Ward Depot HQ")


# ==============================================================================
# PAGE 5: FUEL & DIESEL DASHBOARD
# ==============================================================================
elif "Fuel" in page:
    st.subheader("⛽ Fuel Consumption & Logistics Economics")
    st.markdown(
        f"Track diesel expenditures, mileage performance, and algorithmic route savings in **Ward 142**. "
        f"Bangalore Diesel Benchmark: **₹{config.DIESEL_RATE_PER_LITER}/Liter**."
    )

    summary = fuel_tracker.get_summary_metrics()

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{summary['total_distance_km']} km</div>
            <div class="stat-label">Total Distance Logged</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{summary['total_fuel_liters']} L</div>
            <div class="stat-label">Diesel Consumed</div>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #F87171;">₹{summary['total_cost_inr']:,.2f}</div>
            <div class="stat-label">Total Diesel Cost (₹89/L)</div>
        </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color: #34D399;">₹{summary['total_savings_inr']:,.2f}</div>
            <div class="stat-label">Savings vs Fixed Routes</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_chart1, col_chart2 = st.columns(2)
    daily_df = fuel_tracker.get_daily_trend()

    with col_chart1:
        st.markdown("##### 📈 Daily Fuel Cost vs Algorithm Savings (₹)")
        if not daily_df.empty:
            chart_df = daily_df.set_index("trip_date")[["fuel_cost_inr", "savings_inr"]]
            chart_df.columns = ["Fuel Cost (₹)", "Civic Savings (₹)"]
            st.bar_chart(chart_df)
        else:
            st.info("No trip logs recorded yet.")

    with col_chart2:
        st.markdown("##### 🚛 Truck Performance & Efficiency Breakdown")
        monthly_df = fuel_tracker.generate_monthly_report()
        if not monthly_df.empty:
            st.dataframe(
                monthly_df[["truck_id", "driver", "mileage_km_l", "total_km", "total_fuel_liters", "total_cost_inr", "total_savings_inr"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No truck reports generated.")

    # Real-Time Fuel Trip Calculator Widget
    st.markdown("---")
    st.markdown("##### 🧮 Interactive Per-Trip Fuel Cost Calculator")
    calc_c1, calc_c2, calc_c3 = st.columns(3)
    with calc_c1:
        calc_truck = st.selectbox("Select Compactor Truck", ["T01", "T02", "T03"], index=0)
    with calc_c2:
        calc_dist = st.number_input("Trip Distance (km)", min_value=1.0, max_value=80.0, value=12.4, step=0.5)
    with calc_c3:
        calc_res = fuel_tracker.calculate_trip(calc_truck, calc_dist)
        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; padding: 0.8rem; border-radius: 8px;">
            <div>Driver: <strong>{calc_res['driver_name']}</strong> (Mileage: {calc_res['mileage_km_l']} km/L)</div>
            <div>Fuel Used: <strong>{calc_res['fuel_liters']} L</strong></div>
            <div style="color: #38BDF8; font-size: 1.1rem; font-weight: 700;">Cost: ₹{calc_res['cost_inr']}</div>
            <div style="color: #34D399; font-size: 0.9rem;">Saved vs Legacy Route: ₹{calc_res['savings_inr']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Trip Logs Table
    st.markdown("---")
    st.markdown("##### 📄 Audit Log: All Recorded Trips")
    logs = database.get_all_fuel_logs()
    if logs:
        log_df = pd.DataFrame(logs)
        st.dataframe(
            log_df[["trip_date", "truck_id", "driver_name", "distance_km", "fuel_liters", "fuel_cost_inr", "savings_inr", "notes"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("No trip entries.")
