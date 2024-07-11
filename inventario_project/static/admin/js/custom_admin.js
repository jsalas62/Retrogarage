function openModal(src) {
    var modal = document.getElementById('myModal');
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");

    modal.style.display = "block";
    modalImg.src = src;
    captionText.innerHTML = src;

    // Añadir evento para cerrar el modal al hacer clic fuera de la imagen
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}

function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = "none";

    // Eliminar el evento para evitar múltiples escuchas
    modal.removeEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}
