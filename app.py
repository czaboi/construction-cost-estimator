import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Construction Cost Estimator",
    page_icon="🏗️",
    layout="wide"
)

# ---------------------------
# Load model
# ---------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------------------
# Session state
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "estimate_data" not in st.session_state:
    st.session_state.estimate_data = None

if "error_projects" not in st.session_state:
    st.session_state.error_projects = [
        {
            "Project Name": "Residential Tower A",
            "Category": "Residential",
            "Area (sq ft)": 50000,
            "Predicted Cost": 15000000,
            "Actual Cost": 16200000
        },
        {
            "Project Name": "Office Complex B",
            "Category": "Commercial",
            "Area (sq ft)": 85000,
            "Predicted Cost": 28000000,
            "Actual Cost": 26500000
        },
        {
            "Project Name": "Shopping Mall C",
            "Category": "Retail",
            "Area (sq ft)": 120000,
            "Predicted Cost": 42000000,
            "Actual Cost": 45100000
        },
        {
            "Project Name": "Apartment Building D",
            "Category": "Residential",
            "Area (sq ft)": 42000,
            "Predicted Cost": 12500000,
            "Actual Cost": 13000000
        },
        {
            "Project Name": "Industrial Warehouse E",
            "Category": "Industrial",
            "Area (sq ft)": 65000,
            "Predicted Cost": 8200000,
            "Actual Cost": 7800000
        }
    ]

# ---------------------------
# Theme CSS
# ---------------------------
st.markdown("""
<style>
    .stApp {
        background: #f3f4f6;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .topbar {
        background: #ffffff;
        border-bottom: 2px solid #f3c48d;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        padding: 18px 24px;
        border-radius: 0 0 14px 14px;
        margin-bottom: 28px;
    }

    .brand {
        font-size: 26px;
        font-weight: 800;
        color: #111827;
        line-height: 1.15;
    }

    .brand-orange {
        color: #f97316;
    }

    .page-card {
        background: #f7f7f8;
        border: 1px solid #e5e7eb;
        border-radius: 28px;
        padding: 34px 38px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .section-card {
        background: #f3f4f6;
        border: 1px solid #d9dde3;
        border-radius: 22px;
        padding: 24px 28px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    .soft-orange-card {
        background: linear-gradient(135deg, #fff7ed, #fef3e8);
        border: 2px solid #f3b36c;
        border-radius: 22px;
        padding: 24px 28px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        margin-bottom: 22px;
    }

    .feature-card {
        background: #fbf4eb;
        border: 1.5px solid #f0c790;
        border-radius: 18px;
        padding: 16px 18px;
        min-height: 94px;
        font-size: 17px;
        color: #1f2937;
        display: flex;
        align-items: center;
    }

    .big-title {
        font-size: 56px;
        font-weight: 800;
        color: #111827;
        line-height: 1.08;
        text-align: center;
        margin-bottom: 8px;
    }

    .big-title .orange {
        color: #f97316;
    }

    .subtitle-center {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 34px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 16px;
    }

    .muted {
        color: #6b7280;
        font-size: 15px;
        line-height: 1.8;
    }

    .result-amount-label {
        color: #374151;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .result-amount {
        color: #f97316;
        font-size: 60px;
        font-weight: 800;
        line-height: 1;
    }

    .mini-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }

    .badge-orange {
        background: #ffedd5;
        color: #c2410c;
    }

    .badge-green {
        background: #dcfce7;
        color: #15803d;
    }

    .badge-red {
        background: #fee2e2;
        color: #b91c1c;
    }

    .summary-card {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        padding: 18px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.05);
    }

    .summary-label {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .summary-value {
        font-size: 44px;
        font-weight: 800;
        color: #111827;
        line-height: 1;
    }

    .summary-value-orange {
        font-size: 44px;
        font-weight: 800;
        color: #f97316;
        line-height: 1;
    }

    .summary-value-green {
        font-size: 44px;
        font-weight: 800;
        color: #16a34a;
        line-height: 1;
    }

    .summary-value-red {
        font-size: 44px;
        font-weight: 800;
        color: #dc2626;
        line-height: 1;
    }

    .scenario-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 22px;
        border: 3px solid #e5e7eb;
        box-shadow: 0 8px 18px rgba(0,0,0,0.05);
        min-height: 360px;
    }

    .scenario-green {
        border-color: #22c55e;
    }

    .scenario-orange {
        border-color: #f59e0b;
    }

    .scenario-red {
        border-color: #fb7185;
    }

    .scenario-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 10px;
    }

    .scenario-total {
        font-size: 32px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 14px;
    }

    .cost-row {
        margin-bottom: 14px;
    }

    .cost-header {
        display: flex;
        justify-content: space-between;
        font-size: 18px;
        color: #374151;
        margin-bottom: 6px;
    }

    .cost-track {
        width: 100%;
        height: 12px;
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
    }

    .cost-fill {
        height: 100%;
        background: #ff6a00;
        border-radius: 999px;
    }

    .hr-line {
        height: 1px;
        background: #d1d5db;
        margin: 24px 0;
    }

    .step-row {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 18px;
    }

    .step-circle {
        width: 46px;
        height: 46px;
        border-radius: 999px;
        background: #ff5a00;
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 24px;
    }

    .step-text {
        font-size: 18px;
        color: #1f2937;
        line-height: 1.5;
    }

    .center-button-wrap {
        text-align: center;
        padding-top: 8px;
    }

    div.stButton > button {
        border-radius: 16px;
        height: 56px;
        border: none;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6a00, #f97316);
        color: white;
        box-shadow: 0 8px 18px rgba(249,115,22,0.28);
    }

    div.stButton > button:hover {
        filter: brightness(1.03);
    }

    .footer-btn {
        width: 100%;
    }

    .big-primary-btn button {
        width: 340px !important;
    }

    .navhint {
        color: #6b7280;
        font-size: 13px;
        margin-top: -10px;
        margin-bottom: 8px;
    }

    .table-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 10px;
        box-shadow: 0 5px 16px rgba(0,0,0,0.04);
    }

    .small-note {
        color: #6b7280;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Helpers
# ---------------------------
def format_currency(x):
    return f"฿{x:,.2f}"

def material_multiplier_label(material_grade):
    mapping = {
        "Basic": "Basic (×0.8)",
        "Standard": "Standard (×1)",
        "Premium": "Luxury (×1.6)"
    }
    return mapping.get(material_grade, material_grade)

def compute_estimate(area, floors, material_grade, location_factor):
    material_map = {
        "Basic": 1,
        "Standard": 2,
        "Premium": 3
    }

    material_value = material_map[material_grade]
    input_data = np.array([[area, floors, material_value]])
    predicted_cost = model.predict(input_data)[0]
    predicted_cost = float(predicted_cost)

    adjusted_cost = predicted_cost * location_factor

    structure = adjusted_cost * 0.45
    finishing = adjusted_cost * 0.35
    mep = adjusted_cost * 0.20

    return {
        "base_cost": predicted_cost,
        "total_cost": adjusted_cost,
        "structure": structure,
        "finishing": finishing,
        "mep": mep
    }

def scenario_costs(base_total):
    low = base_total * 0.80
    medium = base_total
    high = base_total * 1.60
    return low, medium, high

def make_breakdown(total):
    return {
        "Structure": total * 0.45,
        "Finishing": total * 0.35,
        "MEP": total * 0.20
    }

def go_page(page_name):
    st.session_state.page = page_name

# ---------------------------
# Top bar / navigation
# ---------------------------
st.markdown("""
<div class="topbar">
    <div class="brand">
        🏗️ <span class="brand-orange">Construction</span><br>Estimator
    </div>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5 = st.columns([1, 1, 1, 1, 1])
with nav1:
    if st.button("Home", use_container_width=True):
        go_page("Home")
with nav2:
    if st.button("Estimator", use_container_width=True):
        go_page("Estimator")
with nav3:
    if st.button("Result", use_container_width=True):
        go_page("Result")
with nav4:
    if st.button("Comparison", use_container_width=True):
        go_page("Comparison")
with nav5:
    if st.button("Error Analysis", use_container_width=True):
        go_page("Error Analysis")

st.markdown('<div class="navhint">Use the buttons above to navigate between pages.</div>', unsafe_allow_html=True)

page = st.session_state.page

# ---------------------------
# Home page
# ---------------------------
if page == "Home":
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="big-title">
        ยินดีต้อนรับสู่ <span class="orange">Construction Cost<br>Estimator</span>
    </div>
    <div class="subtitle-center">
        Your trusted partner in accurate construction cost estimation
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏗️ เกี่ยวกับโปรเจค</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="muted">
        ระบบประเมินราคาค่าก่อสร้างที่ช่วยให้คุณคำนวณต้นทุนการก่อสร้างอาคารได้อย่างรวดเร็วและแม่นยำ
        โดยคำนึงถึงปัจจัยสำคัญต่างๆ เช่น พื้นที่ใช้สอย จำนวนชั้น คุณภาพวัสดุ และตำแหน่งที่ตั้ง
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ คุณสมบัติหลัก</div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown('<div class="feature-card">📊 คำนวณต้นทุนตามพื้นที่และจำนวนชั้นอาคาร</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">📍 ปรับค่าสัมประสิทธิ์ตามทำเลที่ตั้ง</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">🔄 เปรียบเทียบ Scenario ต่างๆ</div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="feature-card">🎨 เลือกระดับคุณภาพวัสดุได้ 4 ระดับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">📈 แสดงผลรายละเอียดค่าใช้จ่ายแยกตามหมวดหมู่</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">🎯 วิเคราะห์ความแม่นยำของการประเมิน</div>', unsafe_allow_html=True)

    st.markdown('<div class="soft-orange-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 วิธีใช้งาน</div>', unsafe_allow_html=True)

    steps = [
        'ไปที่หน้า <b>Estimator</b> เพื่อกรอกข้อมูลโครงการ',
        'ระบุพื้นที่ จำนวนชั้น เกรดวัสดุ และ Location Factor',
        'กดปุ่ม "Calculate Estimate" เพื่อคำนวณ',
        'ดูผลลัพธ์ในหน้า <b>Result</b> พร้อมรายละเอียดค่าใช้จ่ายแต่ละหมวด'
    ]
    for idx, step in enumerate(steps, start=1):
        st.markdown(f"""
        <div class="step-row">
            <div class="step-circle">{idx}</div>
            <div class="step-text">{step}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1.2, 1.2, 1.2])
    with b2:
        if st.button("เริ่มต้นประเมินราคา →", use_container_width=True):
            go_page("Estimator")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Estimator page
# ---------------------------
elif page == "Estimator":
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="big-title" style="font-size:48px;">
        ประเมินต้นทุนก่อสร้าง
    </div>
    <div class="subtitle-center">
        กรอกข้อมูลโครงการเพื่อรับการประเมินราคาที่แม่นยำ
    </div>
    """, unsafe_allow_html=True)

    with st.form("estimate_form"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📏 พื้นที่ (ตารางฟุต)</div>', unsafe_allow_html=True)
        area = st.number_input(" ", min_value=50.0, value=120.0, step=10.0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏢 จำนวนชั้น</div>', unsafe_allow_html=True)
        floors = st.number_input("  ", min_value=1, value=2, step=1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎨 เกรดวัสดุ</div>', unsafe_allow_html=True)
        material_grade = st.selectbox(
            "   ",
            ["Basic", "Standard", "Premium"],
            index=1,
            format_func=lambda x: material_multiplier_label(x),
            label_visibility="collapsed"
        )
        st.caption("เลือกระดับคุณภาพของวัสดุที่ใช้ในการก่อสร้าง")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📍 Location Factor (ค่าสัมประสิทธิ์ทำเล)</div>', unsafe_allow_html=True)
        location_factor = st.number_input("    ", min_value=0.5, max_value=2.0, value=1.0, step=0.1, label_visibility="collapsed")
        st.caption("1.0 = ทำเลราคาปานกลาง | 1.2 = แพงกว่า 20% | 0.8 = ถูกกว่า 20%")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Calculate Estimate", use_container_width=True)

    if submitted:
        result = compute_estimate(area, floors, material_grade, location_factor)
        st.session_state.estimate_data = {
            "area": area,
            "floors": floors,
            "material_grade": material_grade,
            "location_factor": location_factor,
            "total_cost": result["total_cost"],
            "structure": result["structure"],
            "finishing": result["finishing"],
            "mep": result["mep"]
        }
        st.success("Calculation completed. You can now open the Result page.")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("ไปหน้า Result →", use_container_width=True):
                go_page("Result")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Result page
# ---------------------------
elif page == "Result":
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    if st.session_state.estimate_data is None:
        st.warning("ยังไม่มีข้อมูลการประเมิน กรุณาไปที่หน้า Estimator ก่อน")
        if st.button("ไปหน้า Estimator", use_container_width=True):
            go_page("Estimator")
    else:
        d = st.session_state.estimate_data

        st.markdown('<div class="section-title" style="font-size:48px;">ผลการประเมินต้นทุน</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ข้อมูลโครงการ</div>', unsafe_allow_html=True)
        info1, info2 = st.columns(2)
        with info1:
            st.markdown(f"**พื้นที่:**  \n{d['area']:,.0f} ตารางฟุต")
            st.markdown(f"**เกรดวัสดุ:**  \n{material_multiplier_label(d['material_grade']).split(' (')[0]}")
        with info2:
            st.markdown(f"**จำนวนชั้น:**  \n{int(d['floors'])} ชั้น")
            st.markdown(f"**Location Factor:**  \n{d['location_factor']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="soft-orange-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-amount-label">ต้นทุนรวมทั้งหมด</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-amount">{format_currency(d["total_cost"])}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">รายละเอียดค่าใช้จ่ายแยกตามหมวด</div>', unsafe_allow_html=True)

        breakdown_items = [
            ("โครงสร้าง (Structure)", 45, d["structure"]),
            ("งานตกแต่ง (Finishing)", 35, d["finishing"]),
            ("ระบบ MEP (Mechanical, Electrical, Plumbing)", 20, d["mep"])
        ]

        for label, pct, amount in breakdown_items:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([8, 1])
            with c1:
                st.markdown(f"### {label}")
            with c2:
                st.markdown(f'<span class="mini-badge badge-orange">{pct}%</span>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="cost-row">
                <div class="cost-header">
                    <span></span>
                    <span>{format_currency(amount)}</span>
                </div>
                <div class="cost-track">
                    <div class="cost-fill" style="width:{pct}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("← ประเมินใหม่", use_container_width=True):
                go_page("Estimator")
        with b2:
            if st.button("เปรียบเทียบ Scenario", use_container_width=True):
                go_page("Comparison")
        with b3:
            csv_df = pd.DataFrame({
                "Category": ["Structure", "Finishing", "MEP"],
                "Cost": [d["structure"], d["finishing"], d["mep"]]
            })
            st.download_button(
                "พิมพ์รายงาน",
                data=csv_df.to_csv(index=False).encode("utf-8"),
                file_name="construction_cost_report.csv",
                mime="text/csv",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Comparison page
# ---------------------------
elif page == "Comparison":
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    if st.session_state.estimate_data is None:
        st.warning("ยังไม่มีข้อมูลการประเมิน กรุณาไปที่หน้า Estimator ก่อน")
        if st.button("ไปหน้า Estimator", use_container_width=True):
            go_page("Estimator")
    else:
        d = st.session_state.estimate_data
        st.markdown('<div class="section-title" style="font-size:48px;">เปรียบเทียบ Scenario</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ข้อมูลพื้นฐานโครงการ</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**พื้นที่:** {d['area']:,.0f} ตารางฟุต")
        with c2:
            st.markdown(f"**จำนวนชั้น:** {int(d['floors'])} ชั้น")
        st.markdown('</div>', unsafe_allow_html=True)

        low, medium, high = scenario_costs(d["total_cost"])
        low_b = make_breakdown(low)
        med_b = make_breakdown(medium)
        high_b = make_breakdown(high)

        s1, s2, s3 = st.columns(3)

        with s1:
            st.markdown('<div class="scenario-card scenario-green">', unsafe_allow_html=True)
            st.markdown('<div class="scenario-title">Low Cost</div>', unsafe_allow_html=True)
            st.markdown('<span class="mini-badge badge-green">Basic</span>', unsafe_allow_html=True)
            st.markdown('<div class="summary-label">Total Cost</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="scenario-total">{format_currency(low)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
            for label, val, pct in [
                ("Structure", low_b["Structure"], 45),
                ("Finishing", low_b["Finishing"], 35),
                ("MEP", low_b["MEP"], 20),
            ]:
                st.markdown(f"""
                <div class="cost-row">
                    <div class="cost-header">
                        <span>{label}</span>
                        <span>{format_currency(val).replace('.00','')}</span>
                    </div>
                    <div class="cost-track"><div class="cost-fill" style="width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with s2:
            st.markdown('<div class="scenario-card scenario-orange">', unsafe_allow_html=True)
            st.markdown('<div class="scenario-title">Medium Cost</div>', unsafe_allow_html=True)
            st.markdown('<span class="mini-badge badge-orange">Standard</span>', unsafe_allow_html=True)
            st.markdown('<div class="summary-label">Total Cost</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="scenario-total">{format_currency(medium)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
            for label, val, pct in [
                ("Structure", med_b["Structure"], 45),
                ("Finishing", med_b["Finishing"], 35),
                ("MEP", med_b["MEP"], 20),
            ]:
                st.markdown(f"""
                <div class="cost-row">
                    <div class="cost-header">
                        <span>{label}</span>
                        <span>{format_currency(val).replace('.00','')}</span>
                    </div>
                    <div class="cost-track"><div class="cost-fill" style="width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with s3:
            st.markdown('<div class="scenario-card scenario-red">', unsafe_allow_html=True)
            st.markdown('<div class="scenario-title">High Cost</div>', unsafe_allow_html=True)
            st.markdown('<span class="mini-badge badge-red">Luxury</span>', unsafe_allow_html=True)
            st.markdown('<div class="summary-label">Total Cost</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="scenario-total">{format_currency(high)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
            for label, val, pct in [
                ("Structure", high_b["Structure"], 45),
                ("Finishing", high_b["Finishing"], 35),
                ("MEP", high_b["MEP"], 20),
            ]:
                st.markdown(f"""
                <div class="cost-row">
                    <div class="cost-header">
                        <span>{label}</span>
                        <span>{format_currency(val).replace('.00','')}</span>
                    </div>
                    <div class="cost-track"><div class="cost-fill" style="width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        diff = high - low
        pct_more = (diff / low) * 100 if low != 0 else 0

        st.markdown('<div class="soft-orange-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">สรุปการเปรียบเทียบ Low vs High</div>', unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">ต้นทุนต่ำสุด (Basic)</div>
                <div class="summary-value-green">{format_currency(low).replace('.00','')}</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">ต้นทุนสูงสุด (Luxury)</div>
                <div class="summary-value-red">{format_currency(high).replace('.00','')}</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">ส่วนต่าง</div>
                <div class="summary-value-orange">{format_currency(diff).replace('.00','')}</div>
                <div class="small-note">({pct_more:.1f}% สูงกว่า)</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1, 1, 2.5])
        with f1:
            if st.button("← กลับหน้าผลลัพธ์", use_container_width=True):
                go_page("Result")
        with f2:
            if st.button("ประเมินใหม่", use_container_width=True):
                go_page("Estimator")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Error Analysis page
# ---------------------------
elif page == "Error Analysis":
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:48px;">Cost Estimation Error Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-center" style="text-align:left;margin-top:-4px;">Track and analyze the accuracy of your construction cost predictions</div>', unsafe_allow_html=True)

    # Prepare error dataframe
    error_df = pd.DataFrame(st.session_state.error_projects)
    error_df["Variance"] = error_df["Actual Cost"] - error_df["Predicted Cost"]
    error_df["Error Rate (%)"] = (error_df["Variance"].abs() / error_df["Actual Cost"]) * 100

    total_projects = len(error_df)
    avg_error = error_df["Error Rate (%)"].mean()
    high_accuracy_count = (error_df["Error Rate (%)"] < 5).sum()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Total Projects Analyzed</div>
            <div class="summary-value">{total_projects}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="soft-orange-card">
            <div class="summary-label">Average Error Rate</div>
            <div class="summary-value-orange">{avg_error:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="summary-card" style="background:#ecfdf5;border-color:#86efac;">
            <div class="summary-label">High Accuracy (&lt;5% error)</div>
            <div class="summary-value-green">{high_accuracy_count}/{total_projects}</div>
            <div class="small-note">({(high_accuracy_count/total_projects)*100:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add New Project Analysis</div>', unsafe_allow_html=True)

    with st.form("error_form"):
        c1, c2 = st.columns(2)
        with c1:
            project_name = st.text_input("Project Name")
            actual_cost = st.number_input("Actual Cost", min_value=0.0, value=1000000.0, step=50000.0)
        with c2:
            predicted_cost = st.number_input("Predicted Cost", min_value=0.0, value=950000.0, step=50000.0)
            area_sqft = st.number_input("Area (sq ft)", min_value=100.0, value=5000.0, step=100.0)

        category = st.selectbox("Category", ["Residential", "Commercial", "Retail", "Industrial"])
        add_btn = st.form_submit_button("Add Project")

    if add_btn:
        st.session_state.error_projects.append({
            "Project Name": project_name if project_name.strip() else f"Project {len(st.session_state.error_projects)+1}",
            "Category": category,
            "Area (sq ft)": area_sqft,
            "Predicted Cost": predicted_cost,
            "Actual Cost": actual_cost
        })
        st.success("Project added. Refreshing analysis...")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    error_df = pd.DataFrame(st.session_state.error_projects)
    error_df["Variance"] = error_df["Actual Cost"] - error_df["Predicted Cost"]
    error_df["Error Rate (%)"] = (error_df["Variance"].abs() / error_df["Actual Cost"]) * 100

    display_df = error_df.copy()
    display_df["Predicted Cost"] = display_df["Predicted Cost"].map(lambda x: f"${x:,.0f}")
    display_df["Actual Cost"] = display_df["Actual Cost"].map(lambda x: f"${x:,.0f}")
    display_df["Variance"] = error_df["Variance"].map(lambda x: f"{'+' if x > 0 else ''}${x:,.0f}")
    display_df["Area (sq ft)"] = display_df["Area (sq ft)"].map(lambda x: f"{x:,.0f}")

    st.markdown('<div class="section-title">Project Analysis Details</div>', unsafe_allow_html=True)
    st.dataframe(display_df[["Project Name", "Category", "Area (sq ft)", "Predicted Cost", "Actual Cost", "Variance"]], use_container_width=True, hide_index=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Error Distribution</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    x_labels = [name if len(name) < 12 else name[:10] + "..." for name in error_df["Project Name"]]
    y = error_df["Error Rate (%)"].values
    colors = []
    for val in y:
        if val < 5:
            colors.append("#16a34a")
        elif val <= 10:
            colors.append("#f97316")
        else:
            colors.append("#ef4444")

    ax.bar(x_labels, y, color=colors, width=0.38)
    ax.set_ylim(0, max(max(y) + 3, 12))
    ax.set_ylabel("Error Rate (%)")
    ax.set_xlabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)

    for i, val in enumerate(y):
        ax.text(i, val + 0.25, f"{val:.1f}%", ha="center", va="bottom", fontsize=11)

    st.pyplot(fig)

    l1, l2, l3 = st.columns(3)
    with l1:
        st.markdown('<span class="mini-badge badge-green">&lt;5% (Excellent)</span>', unsafe_allow_html=True)
    with l2:
        st.markdown('<span class="mini-badge badge-orange">5–10% (Good)</span>', unsafe_allow_html=True)
    with l3:
        st.markdown('<span class="mini-badge badge-red">&gt;10% (Needs Improvement)</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)