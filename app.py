from flask import Flask, render_template, request, jsonify, send_file
import pickle, io
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

app = Flask(__name__)

# ================= LOAD MODEL =================
model = pickle.load(open("diabetes_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

features = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

# Store last analyzed patient
last_patient = {}

# ================= ROUTES =================

@app.route("/")
def overview():
    return render_template("overview.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", patient=last_patient)

@app.route("/decision")
def decision():
    return render_template("decision.html", patient=last_patient)

@app.route("/diet")
def diet():
    return render_template("diet.html", patient=last_patient)

@app.route("/reports")
def reports():
    return render_template("reports.html", patient=last_patient)

# ================= PREDICTION =================

@app.route("/predict", methods=["POST"])
def predict():
    global last_patient
    data = request.json

    # ---------- Convert input to numeric ----------
    clean_data = {
        "Pregnancies": int(data["Pregnancies"]),
        "Glucose": float(data["Glucose"]),
        "BloodPressure": float(data["BloodPressure"]),
        "SkinThickness": float(data["SkinThickness"]),
        "Insulin": float(data["Insulin"]),
        "BMI": float(data["BMI"]),
        "DiabetesPedigreeFunction": float(data["DiabetesPedigreeFunction"]),
        "Age": int(data["Age"])
    }

    # ---------- DataFrame ----------
    df = pd.DataFrame([[clean_data[f] for f in features]], columns=features)

    # ---------- Scale ----------
    scaled = scaler.transform(df)

    # ---------- Prediction ----------
    pred = model.predict(scaled)[0]

    # Probability (safe)
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(scaled)[0][1]
        risk_value = int(round(prob * 100))
    else:
        # fallback (SVM without probability)
        risk_value = 100 if pred == 1 else 20

    # ---------- Result ----------
    result = "🩸 Diabetes Detected" if pred == 1 else "✅ No Diabetes Detected"

    # ---------- Save patient ----------
    last_patient = clean_data.copy()
    last_patient.update({
        "Result": result,
        "Risk": f"{risk_value}%",
        "RiskValue": risk_value   # 🔑 IMPORTANT FIX
    })

    return jsonify(result=result, risk=risk_value)

# ================= PDF REPORT =================

@app.route("/download_report")
def download_report():
    if not last_patient:
        return "No report available"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, h - 50, "AI Diabetes Health Report")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, h - 80, "Report created by Shivam Singh")
    pdf.drawString(50, h - 100, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    y = h - 140
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Patient Details")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for k, v in last_patient.items():
        pdf.drawString(60, y, f"{k}: {v}")
        y -= 16

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Diabetes_Report_Shivam_Singh.pdf",
        mimetype="application/pdf"
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
