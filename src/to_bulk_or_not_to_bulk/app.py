import os
import requests
import streamlit as st
import pandas as pd

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Neraca Kalori",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Neraca Kalori")
st.caption("Hitung target kalori harian untuk bulking atau cutting, lengkap dengan BMI, BMR, TDEE, dan perkiraan berat badan di akhir target waktu.")

# Sidebar Data Input Form
with st.sidebar:
    st.subheader("Data tubuh")

    # Preset Demo button
    if st.button("Isi dengan data contoh", use_container_width=True):
        st.session_state["unit"] = "Metrik (kg, cm)"
        st.session_state["weight"] = 72.0
        st.session_state["height"] = 172.0
        st.session_state["age"] = 24
        st.session_state["sex"] = "Pria"
        st.session_state["act"] = "1.55"
        st.session_state["goal"] = "Naik berat (bulking)"
        st.session_state["target_days"] = 180
        st.session_state["level"] = "0.1"

    unit_choice = st.radio(
        "Satuan",
        ["Metrik (kg, cm)", "Imperial (lbs, in)"],
        key="unit",
    )
    is_metric = "Metrik" in unit_choice
    unit_code = "m" if is_metric else "i"
    w_label = "kg" if is_metric else "lbs"
    h_label = "cm" if is_metric else "in"

    col_w, col_h = st.columns(2)
    with col_w:
        weight = st.number_input(
            f"Berat badan ({w_label})",
            min_value=30.0 if is_metric else 66.0,
            max_value=300.0 if is_metric else 660.0,
            value=st.session_state.get("weight", 72.0 if is_metric else 158.0),
            step=0.5,
            key="weight_input",
        )
    with col_h:
        height = st.number_input(
            f"Tinggi badan ({h_label})",
            min_value=120.0 if is_metric else 47.0,
            max_value=230.0 if is_metric else 90.0,
            value=st.session_state.get("height", 172.0 if is_metric else 68.0),
            step=0.5,
            key="height_input",
        )

    col_a, col_s = st.columns(2)
    with col_a:
        age = st.number_input(
            "Usia (tahun)",
            min_value=15,
            max_value=90,
            value=st.session_state.get("age", 24),
            step=1,
            key="age_input",
        )
    with col_s:
        sex_choice = st.radio(
            "Jenis kelamin",
            ["Pria", "Wanita"],
            key="sex",
        )
        sex_code = "m" if sex_choice == "Pria" else "f"

    st.subheader("Aktivitas")
    activity_map = {
        "1.2": ("Sedenter · x1,2", "Hampir tidak berolahraga, misalnya kerja di meja tanpa aktivitas fisik tambahan."),
        "1.375": ("Ringan · x1,375", "Olahraga ringan 1–2 hari per minggu."),
        "1.55": ("Sedang · x1,55", "Olahraga sedang 3–5 hari per minggu."),
        "1.725": ("Aktif · x1,725", "Olahraga berat 6–7 hari per minggu."),
        "1.9": ("Sangat aktif · x1,9", "Olahraga berat setiap hari dengan pekerjaan fisik, atau latihan dua kali sehari."),
    }

    act_key = st.selectbox(
        "Olahraga dalam seminggu",
        options=list(activity_map.keys()),
        format_func=lambda k: activity_map[k][0],
        index=2,
        key="act",
    )
    st.caption(activity_map[act_key][1])

    st.subheader("Target")
    goal_choice = st.radio(
        "Tujuan",
        ["Naik berat (bulking)", "Turun berat (cutting)"],
        key="goal",
    )
    goal_code = "gain" if "Naik" in goal_choice else "loss"

    target_days = st.number_input(
        "Target waktu (hari)",
        min_value=7,
        max_value=1095,
        value=st.session_state.get("target_days", 180),
        step=1,
        key="days_input",
    )
    st.caption("Isi 7–1.095 hari. Model perkiraan berlaku sampai 3 tahun.")

    level_map = {
        "0.1": "Direkomendasikan (10% dari TDEE)",
        "0.15": "Agresif (15% dari TDEE)",
        "0.2": "Sangat agresif (20% dari TDEE)",
        "c": "Kustom (isi sendiri)",
    }
    level_key = st.selectbox(
        "Besar surplus/defisit",
        options=list(level_map.keys()),
        format_func=lambda k: level_map[k],
        key="level",
    )

    custom_cal = None
    if level_key == "c":
        custom_cal = st.number_input(
            "Kalori per hari (kcal)",
            min_value=50,
            max_value=1500,
            value=300,
            step=25,
            key="custom_cal_input",
        )

# Payload for calculation
payload = {
    "unit": unit_code,
    "weight": weight,
    "height": height,
    "age": age,
    "sex": sex_code,
    "activity_level": act_key,
    "goal": goal_code,
    "target_days": target_days,
    "level": level_key,
    "custom_calories": custom_cal,
}


def get_results(data):
    try:
        r = requests.post(f"{API_URL}/calculate", json=data, timeout=3)
        if r.status_code == 200:
            return r.json(), None
        return None, f"API Response Error: {r.text}"
    except Exception:
        from to_bulk_or_not_to_bulk.models import UserInput
        from to_bulk_or_not_to_bulk.calculator import compute_metrics
        res = compute_metrics(UserInput(**data))
        return res.model_dump(), None


result, err = get_results(payload)

if err:
    st.error(err)
elif result:
    u = result["unit"]
    sd = result["surplus_deficit"]
    sd_sign = "+" if sd > 0 else "−"
    sd_type = "surplus" if sd > 0 else "defisit"
    abs_sd = abs(sd)

    # 1. Target Kalori Harian
    st.subheader("Target Kalori Harian")
    st.metric(
        label="Target",
        value=f"{result['target_calories']:,.0f} kcal",
        delta=f"TDEE {result['tdee']:,.0f} {sd_sign} {sd_type} {abs_sd:,.0f} kcal",
        delta_color="off",
    )

    # 2. Main Metrics Table
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("BMI", f"{result['bmi']:.1f}", result["bmi_category"], delta_color="off")
        st.metric("BMR", f"{result['bmr']:,.0f} kcal", "Kebutuhan saat istirahat", delta_color="off")
    with m_col2:
        st.metric("TDEE", f"{result['tdee']:,.0f} kcal", f"BMR x {result['activity_multiplier']}", delta_color="off")
        st.metric(f"{sd_type.capitalize()} per hari", f"{sd:+,.0f} kcal", f"{result['surplus_deficit_pct']:.0f}% dari TDEE", delta_color="off")
    with m_col3:
        st.metric("Perkiraan berat akhir", f"{result['final_weight']:.1f} {u}", f"Dari {result['weight']:.1f} {u}", delta_color="off")
        st.metric(f"Perubahan dalam {result['target_days']} hari", f"{result['weight_change']:+.1f} {u}", f"≈ {result['target_days']/7:.1f} minggu", delta_color="off")

    st.caption(f"Eventual Weight Change (EWC): Perubahan setelah 3 tahun konsisten = {result['ewc']:+.1f} {u}")

    # 3. Health Warnings
    if result["warnings"]:
        for w in result["warnings"]:
            st.warning(f"Perhatian: {w}")

    st.divider()

    # 4. Energy & Macronutrients
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Komposisi kalori")
        energy_df = pd.DataFrame([
            {"Komponen": "BMR", "Kalori (kcal)": result["bmr"]},
            {"Komponen": "Aktivitas", "Kalori (kcal)": max(0, result["tdee"] - result["bmr"])},
            {"Komponen": sd_type.capitalize(), "Kalori (kcal)": abs_sd},
        ])
        st.bar_chart(energy_df.set_index("Komponen")["Kalori (kcal)"])

    with c2:
        st.subheader("Saran makronutrien per hari")
        mac = result["macros"]
        st.write(f"- Protein: {mac['protein_g']:,.0f} g ({mac['protein_per_kg']:.1f} g/kg)")
        st.write(f"- Lemak: {mac['fat_g']:,.0f} g (25% dari total kalori)")
        st.write(f"- Karbohidrat: {mac['carb_g']:,.0f} g (sisa kalori)")

        macro_df = pd.DataFrame([
            {"Makronutrien": f"Protein ({mac['protein_g']:,.0f}g)", "Kalori": mac["protein_g"] * 4},
            {"Makronutrien": f"Lemak ({mac['fat_g']:,.0f}g)", "Kalori": mac["fat_g"] * 9},
            {"Makronutrien": f"Karbohidrat ({mac['carb_g']:,.0f}g)", "Kalori": mac["carb_g"] * 4},
        ])
        st.bar_chart(macro_df.set_index("Makronutrien")["Kalori"])

    st.divider()

    # 5. Timeline Projections
    st.subheader("Perkiraan perjalanan berat badan")
    milestones = result["milestones"]
    chart_df = pd.DataFrame({
        "Hari": [0] + [m["day"] for m in milestones],
        "Berat": [result["weight"]] + [m["weight"] for m in milestones],
    })
    st.line_chart(chart_df.set_index("Hari")["Berat"])

    timeline_df = pd.DataFrame([
        {
            "Hari ke-": m["day"],
            "Perubahan": f"{m['change']:+.1f} {u}",
            "Berat": f"{m['weight']:.1f} {u}",
        }
        for m in milestones
    ])
    st.table(timeline_df)

    st.caption(
        f"Proyeksi dihitung linear dari EWC 3 tahun (kcal ÷ {'22' if is_metric else '10'}). "
        "Hasil nyata cenderung melambat karena metabolisme menyesuaikan. "
        "Makronutrien adalah titik awal; komposisi tubuh Anda belum diperhitungkan."
    )
