document.addEventListener("DOMContentLoaded", function () {

  // Buscar todos los contenedores de contraseña
  const containers = document.querySelectorAll(".password-container");

  containers.forEach(container => {
    const toggle = container.querySelector(".toggle-password");
    const input = container.querySelector(".password-input");

    if (toggle && input) {
      toggle.addEventListener("click", function () {
        const type = input.getAttribute("type") === "password" ? "text" : "password";
        input.setAttribute("type", type);
        this.classList.toggle("fa-eye");
        this.classList.toggle("fa-eye-slash");
      });
    }
  });
});