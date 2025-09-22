// Referencias a los campos
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirmPassword');
const fechaInput = document.getElementById('fechaNacimiento');

const emailMsg = document.getElementById('emailMsg');
const passMsg = document.getElementById('passMsg');
const confirmMsg = document.getElementById('confirmMsg');
const edadMsg = document.getElementById('edadMsg');

const emailRegex = /^[^@]+@[^@]+\.[a-zA-Z]{2,}$/;
const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{6,18}$/;

// Validación en tiempo real
emailInput.addEventListener('input', () => {
  if (emailRegex.test(emailInput.value)) {
    emailMsg.textContent = "Correo válido ✔";
    emailMsg.classList.add("ok");
  } else {
    emailMsg.textContent = "Correo inválido";
    emailMsg.classList.remove("ok");
  }
});

passwordInput.addEventListener('input', () => {
  if (passwordRegex.test(passwordInput.value)) {
    passMsg.textContent = "Contraseña segura ✔";
    passMsg.classList.add("ok");
  } else {
    passMsg.textContent = "Debe tener entre 6 y 18 caracteres, una mayúscula y un número.";
    passMsg.classList.remove("ok");
  }
});

confirmInput.addEventListener('input', () => {
  if (confirmInput.value === passwordInput.value) {
    confirmMsg.textContent = "Las contraseñas coinciden ✔";
    confirmMsg.classList.add("ok");
  } else {
    confirmMsg.textContent = "Las contraseñas no coinciden";
    confirmMsg.classList.remove("ok");
  }
});

fechaInput.addEventListener('input', () => {
  const edad = calcularEdad(fechaInput.value);
  if (edad >= 13) {
    edadMsg.textContent = "Edad válida ✔";
    edadMsg.classList.add("ok");
  } else {
    edadMsg.textContent = "Debes tener al menos 13 años";
    edadMsg.classList.remove("ok");
  }
});

// Validación al enviar el formulario
document.getElementById('registroForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const nombre = document.getElementById('nombre').value.trim();
  const usuario = document.getElementById('usuario').value.trim();
  const email = emailInput.value.trim();
  const fechaNacimiento = fechaInput.value;
  const password = passwordInput.value;
  const confirmPassword = confirmInput.value;

  const mensajeExito = document.getElementById('mensajeExito');
  mensajeExito.classList.add('oculto');

  if (!nombre || !usuario || !email || !fechaNacimiento || !password || !confirmPassword) {
    alert('Por favor, complete todos los campos obligatorios.');
    return;
  }

  if (!emailRegex.test(email)) {
    alert('Ingrese un correo electrónico válido.');
    return;
  }

  if (password !== confirmPassword) {
    alert('Las contraseñas no coinciden.');
    return;
  }

  if (!passwordRegex.test(password)) {
    alert('La contraseña debe tener entre 6 y 18 caracteres, al menos una mayúscula y un número.');
    return;
  }

  const edad = calcularEdad(fechaNacimiento);
  if (edad < 13) {
    alert('Debe tener al menos 13 años para registrarse.');
    return;
  }

  // Guardar credenciales y sesión activa
  localStorage.setItem('email', email);
  localStorage.setItem('password', password);
  localStorage.setItem('sesionActiva', 'true');

  alert('Registro realizado con éxito');

  mensajeExito.classList.remove('oculto');
  this.reset();
  emailMsg.textContent = "";
  passMsg.textContent = "";
  confirmMsg.textContent = "";
  edadMsg.textContent = "";
});

// Función para calcular edad
function calcularEdad(fecha) {
  const hoy = new Date();
  const nacimiento = new Date(fecha);
  let edad = hoy.getFullYear() - nacimiento.getFullYear();
  const m = hoy.getMonth() - nacimiento.getMonth();
  if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) {
    edad--;
  }
  return edad;
}

// Función para cerrar sesión
function cerrarSesion() {
  localStorage.removeItem('email');
  localStorage.removeItem('password');
  localStorage.removeItem('sesionActiva');
  alert('Sesión cerrada');
  window.location.href = "../acceso/login.html";
}
