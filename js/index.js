// Validación de sesión
const sesionActiva = localStorage.getItem("sesionActiva");
if (sesionActiva !== "true") {
  window.location.href = "acceso/login.html";
}

function cerrarSesion() {
  localStorage.removeItem("email");
  localStorage.removeItem("password");
  localStorage.removeItem("sesionActiva");
  alert("Sesión cerrada");
  window.location.href = "acceso/login.html";
}
