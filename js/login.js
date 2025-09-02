// Referencias a los elementos del DOM
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const emailMsg = document.getElementById("emailMsg");
const passMsg = document.getElementById("passMsg");
const mensajeExito = document.getElementById("mensajeExito");

const emailRegex = /^[^@]+@[^@]+\.[a-zA-Z]{2,}$/;
const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{6,18}$/;

// Validación en tiempo real del correo
emailInput.addEventListener("input", () => {
  if (emailRegex.test(emailInput.value)) {
    emailMsg.textContent = "Correo válido ✔";
    emailMsg.classList.add("ok");
    emailMsg.classList.remove("error");
  } else {
    emailMsg.textContent = "Correo inválido";
    emailMsg.classList.remove("ok");
    emailMsg.classList.add("error");
  }
});

// Validación en tiempo real de la contraseña
passwordInput.addEventListener("input", () => {
  if (passwordRegex.test(passwordInput.value)) {
    passMsg.textContent = "Contraseña segura ✔";
    passMsg.classList.add("ok");
    passMsg.classList.remove("error");
  } else {
    passMsg.textContent = "Debe tener entre 6 y 18 caracteres, una mayúscula y un número.";
    passMsg.classList.remove("ok");
    passMsg.classList.add("error");
  }
});

// Validación al enviar el formulario
document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  mensajeExito.classList.add("oculto");

  if (!email || !password) {
    alert("Por favor, complete todos los campos.");
    return;
  }

  if (!emailRegex.test(email)) {
    alert("Ingrese un correo electrónico válido.");
    return;
  }

  if (!passwordRegex.test(password)) {
    alert("La contraseña debe tener entre 6 y 18 caracteres, al menos una mayúscula y un número.");
    return;
  }

  // Obtener credenciales guardadas desde localStorage
  const emailGuardado = localStorage.getItem("email");
  const passwordGuardada = localStorage.getItem("password");

  if (email === emailGuardado && password === passwordGuardada) {
    localStorage.setItem("sesionActiva", "true");
    mensajeExito.classList.remove("oculto");
    alert("Inicio de sesión exitoso ✔ Bienvenido a PlayVerse");
    window.location.href = "../index.html";
  } else {
    alert("Credenciales inválidas ❌. Verifique su correo y contraseña.");
    emailMsg.textContent = "Correo no coincide con el registrado";
    emailMsg.classList.remove("ok");
    emailMsg.classList.add("error");

    passMsg.textContent = "Contraseña incorrecta";
    passMsg.classList.remove("ok");
    passMsg.classList.add("error");
  }
});
