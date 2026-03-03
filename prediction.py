import joblib
import pandas as pd
import numpy as np
import os

# ─── Load Model & Artifacts ────────────────────────────────────────────────────
MODEL_DIR = "model"

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
label_maps = joblib.load(os.path.join(MODEL_DIR, "label_maps.pkl"))

print(f"Model loaded: XGBoost ({model.n_estimators} trees)")
print(f"Features    : {len(feature_names)} columns")
print()


# ─── Encoding Helper ───────────────────────────────────────────────────────────
def encode_input(data: dict, label_maps: dict) -> dict:
    # Encode categorical variables using saved label maps
    encoded = data.copy()
    for col, mapping in label_maps.items():
        if col in encoded:
            val = encoded[col]
            if val not in mapping:
                raise ValueError(
                    f"Nilai '{val}' tidak valid untuk kolom '{col}'. "
                    f"Pilihan: {list(mapping.keys())}"
                )
            encoded[col] = mapping[val]
    return encoded


# ─── Prediction Function ───────────────────────────────────────────────────────
def predict_attrition(employee_data: dict) -> dict:
    # Encode categorical
    encoded = encode_input(employee_data, label_maps)

    # Build dataframe
    df_input = pd.DataFrame([encoded])[feature_names]

    # Predict
    prob = model.predict_proba(df_input)[0][1]
    pred = int(prob >= 0.4)  # ← threshold 0.4

    # Risk level
    if prob >= 0.4:
        risk = "🔴 HIGH RISK"
    elif prob >= 0.25:
        risk = "🟡 MEDIUM RISK"
    else:
        risk = "🟢 LOW RISK"

    return {
        "prediction": "Yes — Berisiko Resign" if pred == 1 else "No — Kemungkinan Bertahan",
        "probability": round(float(prob), 4),
        "risk_level": risk,
    }


# ─── Example Data ──────────────────────────────────────────────────────────────
# Contoh 1: Karyawan Berisiko Tinggi / Resign
employee_high_risk = {
    "Age": 26,
    "BusinessTravel": "Travel_Frequently",
    "DailyRate": 450,
    "Department": "Sales",
    "DistanceFromHome": 25,
    "Education": 3,
    "EducationField": "Marketing",
    "EnvironmentSatisfaction": 1,       # Low
    "Gender": "Male",
    "HourlyRate": 45,
    "JobInvolvement": 2,
    "JobLevel": 1,
    "JobRole": "Sales Representative",
    "JobSatisfaction": 1,               # Low
    "MaritalStatus": "Single",
    "MonthlyIncome": 2500,              # Rendah
    "MonthlyRate": 8000,
    "NumCompaniesWorked": 5,
    "OverTime": "Yes",                  # Overtime
    "PercentSalaryHike": 11,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 2,
    "StockOptionLevel": 0,              # Tanpa stock option
    "TotalWorkingYears": 3,
    "TrainingTimesLastYear": 0,
    "WorkLifeBalance": 1,              # Low
    "YearsAtCompany": 1,               # Baru bergabung
    "YearsInCurrentRole": 1,
    "YearsSinceLastPromotion": 0,
    "YearsWithCurrManager": 0,
}

# Contoh 2: Karyawan Aman / Bertahan
employee_low_risk = {
    "Age": 42,
    "BusinessTravel": "Non-Travel",
    "DailyRate": 1200,
    "Department": "Research & Development",
    "DistanceFromHome": 5,
    "Education": 4,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 4,       # Very High
    "Gender": "Female",
    "HourlyRate": 85,
    "JobInvolvement": 4,
    "JobLevel": 4,
    "JobRole": "Research Director",
    "JobSatisfaction": 4,               # Very High
    "MaritalStatus": "Married",
    "MonthlyIncome": 15000,             # Tinggi
    "MonthlyRate": 20000,
    "NumCompaniesWorked": 2,
    "OverTime": "No",                   # Tidak overtime
    "PercentSalaryHike": 22,
    "PerformanceRating": 4,
    "RelationshipSatisfaction": 4,
    "StockOptionLevel": 3,              # Stock option tertinggi
    "TotalWorkingYears": 18,
    "TrainingTimesLastYear": 4,
    "WorkLifeBalance": 4,              # Outstanding
    "YearsAtCompany": 15,              # Veteran
    "YearsInCurrentRole": 8,
    "YearsSinceLastPromotion": 2,
    "YearsWithCurrManager": 5,
}


# ─── Run Predictions ───────────────────────────────────────────────────────────
def print_result(title: str, employee: dict, result: dict):
    print(f"\n{'─'*55}")
    print(f"👤 {title}")
    print(f"{'─'*55}")
    print(f"   Usia           : {employee['Age']} tahun")
    print(f"   Department     : {employee['Department']}")
    print(f"   MonthlyIncome  : ${employee['MonthlyIncome']:,}")
    print(f"   OverTime       : {employee['OverTime']}")
    print(f"   JobSatisfaction: {employee['JobSatisfaction']} (1=Low, 4=VHigh)")
    print(f"   YearsAtCompany : {employee['YearsAtCompany']} tahun")
    print(f"   MaritalStatus  : {employee['MaritalStatus']}")
    print()
    print(f"   Prediksi   : {result['prediction']}")
    print(f"   Probabilitas: {result['probability']:.2%}")
    print(f"   Risk Level : {result['risk_level']}")


if __name__ == "__main__":
    try:
        result_high = predict_attrition(employee_high_risk)
        print_result("KARYAWAN A — Profil Berisiko", employee_high_risk, result_high)

        result_low = predict_attrition(employee_low_risk)
        print_result("KARYAWAN B — Profil Aman", employee_low_risk, result_low)

        print(f"\n{'='*55}")
        print("CARA MENGGUNAKAN UNTUK DATA BARU:")
        print("   1. Buat dictionary dengan data karyawan")
        print("   2. Panggil: result = predict_attrition(data_karyawan)")
        print("   3. Cek result['prediction'] dan result['probability']")
        print("=" * 55)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise
