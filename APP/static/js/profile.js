/**
     * Listener del formulario.
     * Se usa para obtener el contenido de un div editable a través de un input oculto
     * Debido a que el div editable donde el usuario escribe el comentario no es de tipo input, 
     * se crea un input invisible que sí tomará el formulario y se le asigna a dicho input el valor
     * del div editable antes de que se envíe.
    */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("commentForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            const editableDiv = document.getElementById("editableDiv");
            const hiddenInput = document.getElementById("hiddenContentInput");
            hiddenInput.value = editableDiv.innerText.trim();
        });
    }
});