from typing import List, Tuple
from to_bulk_or_not_to_bulk.models import (
    UserInput,
    CalculationResult,
    UnitSystem,
    Sex,
    GoalType,
    SurplusDeficitLevel,
    MacroRecommendation,
    MilestonePoint,
)

BMI_CATEGORIES = [
    (18.5, "Kurus (underweight)"),
    (25.0, "Normal"),
    (30.0, "Berat lebih (overweight)"),
    (35.0, "Obesitas"),
    (99.0, "Obesitas ekstrem"),
]


def get_bmi_category(bmi: float) -> str:
    for threshold, cat in BMI_CATEGORIES:
        if bmi < threshold:
            return cat
    return "Obesitas ekstrem"


def compute_metrics(inp: UserInput) -> CalculationResult:
    m = inp.unit == UnitSystem.METRIC
    w = inp.weight
    h = inp.height
    a = inp.age
    d = inp.target_days
    gain = inp.goal == GoalType.GAIN
    male = inp.sex == Sex.MALE
    act = float(inp.activity_level.value)
    lv = inp.level

    # 1. Standardize to metric kg & cm for calculation
    kg = w if m else w * 0.45359237
    cm = h if m else h * 2.54

    # 2. BMI
    if m:
        bmi = round(kg / (cm * cm) * 10000.0, 1)
    else:
        bmi = round(703.0 * w / (h * h), 1)

    bmi_cat = get_bmi_category(bmi)

    # 3. BMR (Mifflin-St Jeor)
    bmr = round(10.0 * kg + 6.25 * cm - 5.0 * a + (5.0 if male else -161.0), 0)

    # 4. TDEE
    tdee = round(bmr * act, 0)

    # 5. Surplus / Deficit Magnitude
    if lv == SurplusDeficitLevel.CUSTOM and inp.custom_calories is not None:
        mag = float(inp.custom_calories)
    else:
        multiplier = float(lv.value) if lv.value in ["0.1", "0.15", "0.2"] else 0.10
        mag = round(tdee * multiplier, 0)

    sd = mag if gain else -mag
    target_calories = round(tdee + sd, 0)

    # Surplus/deficit percentage of TDEE
    sd_pct = round(abs(sd) / tdee * 100.0, 0) if tdee > 0 else 0.0

    # 6. Eventual Weight Change (EWC) - per Neraca Kalori.html
    # ewc = m ? sd / 22 : sd / 10; chg = ewc * d / 1095; fin = w + chg;
    ewc = round(sd / 22.0 if m else sd / 10.0, 1)
    chg = round(ewc * d / 1095.0, 1)
    fin = round(w + chg, 1)

    fin_kg = fin if m else fin * 0.45359237
    fin_bmi = round(fin_kg / (cm * cm) * 10000.0, 1)

    # 7. Macronutrient Breakdown
    # Protein: kg * (gain ? 1.8 : 2.2)
    # Fat: 25% of target / 9
    # Carb: max(0, (target - pr*4 - fat*9)/4)
    protein_per_kg = 1.8 if gain else 2.2
    pr = round(kg * protein_per_kg, 0)
    fat = round((0.25 * target_calories) / 9.0, 0)
    carb = max(0.0, round((target_calories - (pr * 4.0) - (fat * 9.0)) / 4.0, 0))

    macros = MacroRecommendation(
        protein_g=pr,
        protein_per_kg=protein_per_kg,
        fat_g=fat,
        fat_pct=25.0,
        carb_g=carb,
    )

    # 8. Milestone tracking
    step = 30 if d <= 360 else 90
    milestone_days = []
    x = step
    while x < d:
        milestone_days.append(x)
        x += step
    milestone_days.append(d)

    per = chg / d if d > 0 else 0.0
    milestones = [
        MilestonePoint(
            day=day,
            change=round(per * day, 1),
            weight=round(w + per * day, 1),
        )
        for day in milestone_days
    ]

    # 9. Warnings logic matching Neraca Kalori.html
    warnings = []
    if a < 18:
        warnings.append("Rumus BMR ini disusun untuk orang dewasa. Untuk usia di bawah 18 tahun, konsultasikan target kalori ke dokter atau ahli gizi")
    if not gain and bmi < 18.5:
        warnings.append("BMI Anda sudah tergolong kurus. Defisit kalori tidak disarankan tanpa pengawasan tenaga kesehatan")
    if not gain and fin_bmi < 18.5 and bmi >= 18.5:
        warnings.append(f"Dengan target ini, BMI di akhir periode turun ke {fin_bmi:.1f}, di bawah batas normal 18,5. Perpanjang waktu atau kecilkan defisit")
    if gain and bmi >= 30.0:
        warnings.append("BMI Anda sudah ≥ 30. Surplus kalori akan menambah lemak lebih banyak daripada otot; pertimbangkan menjaga berat atau berkonsultasi dulu")
    if target_calories < bmr:
        warnings.append(f"Target harian ({int(target_calories):,} kcal) berada di bawah BMR ({int(bmr):,} kcal). Sulit dipertahankan dan berisiko kehilangan otot")
    if not gain and -sd > 1000:
        warnings.append("Defisit lebih dari 1.000 kcal per hari terlalu besar untuk kebanyakan orang. Turunkan ke tingkat Direkomendasikan atau Agresif")

    return CalculationResult(
        unit="kg" if m else "lbs",
        weight=w,
        target_days=d,
        goal=inp.goal,
        bmi=bmi,
        bmi_category=bmi_cat,
        bmr=bmr,
        tdee=tdee,
        activity_multiplier=act,
        surplus_deficit=sd,
        surplus_deficit_pct=sd_pct,
        target_calories=target_calories,
        ewc=ewc,
        weight_change=chg,
        final_weight=fin,
        final_bmi=fin_bmi,
        macros=macros,
        milestones=milestones,
        warnings=warnings,
    )
