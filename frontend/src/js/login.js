/* =========================================
   Coinlytics Auth Logic
========================================= */

/* ========= CONFIG ========= */

/*
  Change ONLY this when deploying
*/
const API_BASE_URL = "http://127.0.0.1:8080";

/* ========= ELEMENTS ========= */

const signIn = document.querySelector(".sign-in");
const signUp = document.querySelector(".sign-up");

const showSignup = document.getElementById("show-signup");
const showSignin = document.getElementById("show-signin");

const signInForm = document.querySelector(".sign-in form");
const signUpForm = document.querySelector(".sign-up form");

/* ========= SWITCH FORMS ========= */

showSignup.addEventListener("click", () => {
  signIn.classList.remove("active");
  signUp.classList.add("active");

  clearMessages();
});

showSignin.addEventListener("click", () => {
  signUp.classList.remove("active");
  signIn.classList.add("active");

  clearMessages();
});

/* =========================================
   PASSWORD TOGGLE
========================================= */

const toggleIcons = document.querySelectorAll(".toggle-password");

toggleIcons.forEach((icon) => {
  icon.addEventListener("click", () => {
    const input = icon.parentElement.querySelector("input");

    if (input.type === "password") {
      input.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
    } else {
      input.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
    }
  });
});

/* =========================================
   MESSAGE HELPERS
========================================= */

function clearMessages() {
  document.querySelectorAll(".api-message").forEach((el) => el.remove());
}

function showMessage(container, message, type = "error") {
  clearMessages();

  const div = document.createElement("div");
  div.className = `api-message ${type}`;

  div.style.marginTop = "14px";
  div.style.padding = "12px";
  div.style.borderRadius = "10px";
  div.style.fontSize = "14px";
  div.style.fontWeight = "500";

  if (type === "error") {
    div.style.background = "rgba(255,0,0,0.08)";
    div.style.border = "1px solid rgba(255,0,0,0.2)";
    div.style.color = "#ff6b6b";
  } else {
    div.style.background = "rgba(0,255,100,0.08)";
    div.style.border = "1px solid rgba(0,255,100,0.2)";
    div.style.color = "#4ade80";
  }

  div.textContent = message;

  container.appendChild(div);
}

/* =========================================
   SIGNUP API
========================================= */

signUpForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  clearMessages();

  const inputs = signUpForm.querySelectorAll("input");

  const name = inputs[0].value.trim();
  const phoneNumber = inputs[1].value.trim();
  const email = inputs[2].value.trim();
  const password = inputs[3].value.trim();

  const submitBtn = signUpForm.querySelector("button");

  submitBtn.disabled = true;
  submitBtn.textContent = "Creating Account...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        password,
        phoneNumber,
        role: "USER",
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Signup failed");
    }

    /*
      Store token
    */
    sessionStorage.setItem("coinlytics_token", data.accessToken);
    sessionStorage.setItem("coinlytics_user", data.username);

    showMessage(signUpForm, "Account created successfully!", "success");

    /*
      Redirect
    */
    setTimeout(() => {
      window.location.href = "./dashboard.html";
    }, 1000);

  } catch (error) {
    showMessage(signUpForm, error.message || "Something went wrong");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Create Account";
  }
});

/* =========================================
   LOGIN API
========================================= */

signInForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  clearMessages();

  const inputs = signInForm.querySelectorAll("input");

  const email = inputs[0].value.trim();
  const password = inputs[1].value.trim();

  const submitBtn = signInForm.querySelector("button");

  submitBtn.disabled = true;
  submitBtn.textContent = "Signing In...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Login failed");
    }

    /*
      Store JWT
    */
    sessionStorage.setItem("coinlytics_token", data.jwt);
    sessionStorage.setItem("coinlytics_user", data.username);

    showMessage(signInForm, "Login successful!", "success");

    /*
      Redirect
    */
    setTimeout(() => {
      window.location.href = "./dashboard.html";
    }, 1000);

  } catch (error) {
    showMessage(signInForm, error.message || "Something went wrong");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Sign In";
  }
});