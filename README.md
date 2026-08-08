# Disease Risk Prediction System

## About the Project

The **Disease Risk Prediction System** is a web-based application that provides an ML-based estimate of heart disease risk.

Users can create an account, log in, enter patient health information, and receive a risk prediction with a probability result.

> **Disclaimer:** This system provides an ML-based risk estimate and is not a medical diagnosis.

## Features

* User registration
* User login
* User logout
* Patient risk evaluation form
* Heart disease risk prediction
* Prediction probability
* Input validation
* Loading indicator
* Responsive web design

## Technologies

* HTML
* CSS
* JavaScript
* REST API
* Machine Learning

## Project Files

```text
Disease-Risk-Prediction-System/
│
├── index.html
├── login.html
├── register.html
├── style.css
├── auth.js
├── script.js
└── README.md
```

## Patient Information

The application collects the following information for risk evaluation:

* Age
* Gender
* Chest Pain Type
* Resting Blood Pressure
* Cholesterol
* Fasting Blood Sugar
* Resting ECG
* Maximum Heart Rate
* Exercise-Induced Angina
* ST Depression (oldpeak)
* Slope of ST Segment
* Number of Major Vessels
* Thalassemia

## Authentication

The application includes registration and login functionality.

Users can:

1. Create an account.
2. Log in using their email and password.
3. Access the risk prediction system.
4. Log out of the application.

## Prediction

After entering the required patient information, the application sends the data to the backend prediction API.

The result displays:

* Risk classification
* Probability percentage
* Prediction message

## Backend Connection

The frontend communicates with a backend API running at:

```text
http://127.0.0.1:5000
```

The application uses API endpoints for:

```text
/register
/login
/logout
/me
/predict
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Gali-karthik/Disease-Risk-Prediction-System.git
```

### 2. Open the project folder

```bash
cd Disease-Risk-Prediction-System
```

### 3. Start the backend

Run the backend server on:

```text
http://127.0.0.1:5000
```

### 4. Open the application

Open:

```text
login.html
```

in your web browser.

Create an account, log in, and use the prediction form.

## Disclaimer

This project is developed for educational and demonstration purposes. The prediction provided by the system is not a substitute for professional medical advice, diagnosis, or treatment.

## Author

**Karthik**

GitHub:
https://github.com/Gali-karthik
