# AI Disease Risk Prediction System - Authentication Version

This version adds:
- User registration
- Secure password hashing
- Login/logout using Flask sessions
- SQLite user database
- Protected `/predict` endpoint
- Manual patient data entry
- Loading overlay only during prediction
- Existing Random Forest model support

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Copy your existing trained `disease_model.pkl` into `backend/`.

If you have not trained the model yet:

```powershell
cd backend
python train_model.py
```

Then start the backend:

```powershell
cd backend
python app.py
```

In a second terminal:

```powershell
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Open:

http://127.0.0.1:5500/login.html

Register a user, log in, then enter patient details manually.

## Important

This is an educational prototype, not a medical diagnostic product. Do not use it for real clinical decisions or store real patient information without appropriate security, privacy, compliance, and clinical validation.
