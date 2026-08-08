const API_BASE = "http://127.0.0.1:5000";

const form = document.getElementById("riskForm");
const formError = document.getElementById("formError");
const resultSection = document.getElementById("results");
const riskLabel = document.getElementById("riskLabel");
const probabilityElement = document.getElementById("probability");
const predictionMessage = document.getElementById("predictionMessage");
const loadingOverlay = document.getElementById("loadingOverlay");
const logoutButton = document.getElementById("logoutButton");
const welcomeUser = document.getElementById("welcomeUser");

function setLoading(isLoading) {
  loadingOverlay.classList.toggle("hidden", !isLoading);
}

function displayError(message) {
  formError.textContent = message;
}

async function loadUser() {
  const response = await fetch(`${API_BASE}/me`, {
    credentials: "include"
  });

  if (!response.ok) {
    window.location.href = "login.html";
    return;
  }

  const data = await response.json();
  welcomeUser.textContent = `Welcome, ${data.user.name}`;
}

function buildFormData() {
  return {
    age: Number(document.getElementById("age").value),
    sex: Number(document.getElementById("sex").value),
    cp: Number(document.getElementById("cp").value),
    trestbps: Number(document.getElementById("trestbps").value),
    chol: Number(document.getElementById("chol").value),
    fbs: Number(document.getElementById("fbs").value),
    restecg: Number(document.getElementById("restecg").value),
    thalach: Number(document.getElementById("thalach").value),
    exang: Number(document.getElementById("exang").value),
    oldpeak: Number(document.getElementById("oldpeak").value),
    slope: Number(document.getElementById("slope").value),
    ca: Number(document.getElementById("ca").value),
    thal: Number(document.getElementById("thal").value)
  };
}

function validateInput(fields) {
  if (!Number.isInteger(fields.age) || fields.age < 1 || fields.age > 120)
    return "Enter a valid age.";

  if (![0, 1].includes(fields.sex)) return "Select a valid gender.";
  if (![1, 2, 3, 4].includes(fields.cp)) return "Select a valid chest pain type.";
  if (fields.trestbps < 80 || fields.trestbps > 220) return "Enter valid blood pressure.";
  if (fields.chol < 100 || fields.chol > 600) return "Enter valid cholesterol.";
  if (![0, 1].includes(fields.fbs)) return "Select fasting blood sugar.";
  if (![0, 1, 2].includes(fields.restecg)) return "Select resting ECG.";
  if (fields.thalach < 60 || fields.thalach > 220) return "Enter valid maximum heart rate.";
  if (![0, 1].includes(fields.exang)) return "Select exercise-induced angina.";
  if (fields.oldpeak < 0 || fields.oldpeak > 10) return "Enter valid ST depression.";
  if (![1, 2, 3].includes(fields.slope)) return "Select slope.";
  if (fields.ca < 0 || fields.ca > 3) return "Enter major vessel count.";
  if (![3, 6, 7].includes(fields.thal)) return "Select thalassemia.";

  return "";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = buildFormData();
  const validationError = validateInput(payload);

  if (validationError) {
    displayError(validationError);
    return;
  }

  displayError("");
  setLoading(true);

  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.status === 401) {
      window.location.href = "login.html";
      return;
    }

    if (!response.ok || !data.success) {
      throw new Error(data.message || "Unable to get a prediction.");
    }

    resultSection.classList.remove("hidden");
    riskLabel.textContent = data.risk;
    probabilityElement.textContent = `${Number(data.probability).toFixed(2)}% probability`;
    predictionMessage.textContent = data.message;

    resultSection.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    displayError(error.message);
  } finally {
    setLoading(false);
  }
});

logoutButton.addEventListener("click", async () => {
  await fetch(`${API_BASE}/logout`, {
    method: "POST",
    credentials: "include"
  });

  window.location.href = "login.html";
});

loadUser();
