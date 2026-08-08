from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import os
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Frontend is served at http://127.0.0.1:5500
CORS(
    app,
    resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}},
    supports_credentials=True
)

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")
DB_PATH = os.path.join(BASE_DIR, "users.db")

FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

try:
    model = joblib.load(MODEL_PATH)
except Exception as load_error:
    model = None
    print(f"Error loading model: {load_error}")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return user


def login_required():
    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "message": "Please log in first."
        }), 401
    return None


def validate_patient_data(data):
    if not isinstance(data, dict):
        return "Invalid JSON payload."

    missing_fields = [field for field in FEATURES if field not in data]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}."

    try:
        age = int(data["age"])
        sex = int(data["sex"])
        cp = int(data["cp"])
        trestbps = int(data["trestbps"])
        chol = int(data["chol"])
        fbs = int(data["fbs"])
        restecg = int(data["restecg"])
        thalach = int(data["thalach"])
        exang = int(data["exang"])
        oldpeak = float(data["oldpeak"])
        slope = int(data["slope"])
        ca = int(data["ca"])
        thal = int(data["thal"])
    except (ValueError, TypeError):
        return "Some fields have invalid numeric values."

    if not 1 <= age <= 120:
        return "Age must be between 1 and 120."
    if sex not in (0, 1):
        return "Gender value must be 0 or 1."
    if cp not in (1, 2, 3, 4):
        return "Chest pain type must be 1, 2, 3, or 4."
    if not 80 <= trestbps <= 220:
        return "Resting blood pressure must be between 80 and 220."
    if not 100 <= chol <= 600:
        return "Cholesterol must be between 100 and 600."
    if fbs not in (0, 1):
        return "Fasting blood sugar must be 0 or 1."
    if restecg not in (0, 1, 2):
        return "Resting ECG must be 0, 1, or 2."
    if not 60 <= thalach <= 220:
        return "Maximum heart rate must be between 60 and 220."
    if exang not in (0, 1):
        return "Exercise-induced angina must be 0 or 1."
    if not 0.0 <= oldpeak <= 10.0:
        return "ST depression must be between 0.0 and 10.0."
    if slope not in (1, 2, 3):
        return "Slope must be 1, 2, or 3."
    if ca not in (0, 1, 2, 3):
        return "Number of major vessels must be between 0 and 3."
    if thal not in (3, 6, 7):
        return "Thalassemia must be 3, 6, or 7."

    return None


def build_feature_array(data):
    return np.array([
        data["age"], data["sex"], data["cp"], data["trestbps"], data["chol"],
        data["fbs"], data["restecg"], data["thalach"], data["exang"],
        float(data["oldpeak"]), data["slope"], data["ca"], data["thal"]
    ]).reshape(1, -1)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "AI Disease Risk Prediction System backend is running."
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "healthy",
        "model_loaded": model is not None
    })


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if len(name) < 2:
        return jsonify({"success": False, "message": "Enter a valid name."}), 400
    if "@" not in email or len(email) < 5:
        return jsonify({"success": False, "message": "Enter a valid email."}), 400
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400

    password_hash = generate_password_hash(password)

    try:
        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    session.clear()
    session["user_id"] = user_id

    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user": {"name": name, "email": email}
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session.clear()
    session["user_id"] = user["id"]

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "user": {"name": user["name"], "email": user["email"]}
    })


@app.route("/me", methods=["GET"])
def me():
    user = current_user()
    if not user:
        return jsonify({"success": False, "authenticated": False}), 401

    return jsonify({
        "success": True,
        "authenticated": True,
        "user": {"name": user["name"], "email": user["email"]}
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route("/predict", methods=["POST"])
def predict():
    auth_error = login_required()
    if auth_error:
        return auth_error

    if model is None:
        return jsonify({
            "success": False,
            "message": "ML model is not available. Please train and save disease_model.pkl first."
        }), 500

    request_data = request.get_json(silent=True)
    if request_data is None:
        return jsonify({
            "success": False,
            "message": "Invalid JSON payload."
        }), 400

    validation_error = validate_patient_data(request_data)
    if validation_error:
        return jsonify({
            "success": False,
            "message": validation_error
        }), 400

    features = build_feature_array(request_data)

    try:
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]
        probability = float(round(probabilities[1] * 100, 2))
    except Exception as err:
        return jsonify({
            "success": False,
            "message": f"Prediction failed: {err}"
        }), 500

    risk = "Higher Risk" if prediction == 1 else "Lower Risk"

    return jsonify({
        "success": True,
        "prediction": prediction,
        "risk": risk,
        "probability": probability,
        "message": (
            "The model predicts a higher risk based on the provided information."
            if prediction == 1
            else "The model predicts a lower risk based on the provided information."
        )
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
