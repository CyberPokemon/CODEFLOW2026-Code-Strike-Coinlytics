const signIn = document.querySelector(".sign-in");
const signUp = document.querySelector(".sign-up");

const showSignup = document.getElementById("show-signup");
const showSignin = document.getElementById("show-signin");

showSignup.addEventListener("click", () => {
  signIn.classList.remove("active");
  signUp.classList.add("active");
});

showSignin.addEventListener("click", () => {
  signUp.classList.remove("active");
  signIn.classList.add("active");
});

/* PASSWORD TOGGLE */

const toggleIcons = document.querySelectorAll(".toggle-password");

toggleIcons.forEach(icon => {

  icon.addEventListener("click", () => {

    const input = icon.parentElement.querySelector("input");

    if(input.type === "password"){
      input.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
    }
    else{
      input.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
    }

  });

});