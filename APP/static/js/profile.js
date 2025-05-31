document.addEventListener("DOMContentLoaded", function () {
    // Manejo del formulario de comentarios
    const form = document.getElementById("commentForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            const editableDiv = document.getElementById("editableDiv");
            const hiddenInput = document.getElementById("hiddenContentInput");
            if (editableDiv && hiddenInput) {
                hiddenInput.value = editableDiv.innerText.trim();
            }
        });
    }

    // Mostrar el modal si hay mensajes
    const messages = document.querySelectorAll('.alert');
    const modalElement = document.getElementById('editProfileModal');
    if (messages.length > 0 && modalElement) {
        try {
            const modal = new mdb.Modal(modalElement); // Inicializar el modal de MDB
            modal.show(); // Mostrar el modal automáticamente
        } catch (error) {
            console.error("Error al inicializar o mostrar el modal:", error);
            // Limpiar mensajes al cerrar el modal
        }
    }

    if (modalElement) {
        modalElement.addEventListener('hide.mdb.modal', () => {
            document.querySelectorAll('.alert').forEach(alert => alert.remove());
        });
    }
});



