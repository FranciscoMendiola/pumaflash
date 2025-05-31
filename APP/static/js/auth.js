// Eliminar mensajes de alerta al cambiar de pestaña
document.getElementById("tab-login").addEventListener("click", () => {
  document.querySelectorAll(".alert").forEach(alert => alert.remove());
});

document.getElementById("tab-register").addEventListener("click", () => {
  document.querySelectorAll(".alert").forEach(alert => alert.remove());
});