document.addEventListener("DOMContentLoaded", function () {
    const productId = new URLSearchParams(window.location.search).get("id");
    const products = JSON.parse(localStorage.getItem("products")) || [];
    const product = products.find((p) => p.id === productId);

    if (product) {
        document.getElementById("product-id").value = product.id;
        document.getElementById("product-name").value = product.name;
        document.getElementById("product-desc").value = product.desc;
        document.getElementById("product-ubi").value = product.ubi;
        document.getElementById("product-cant").value = product.cant;
        document.getElementById("product-categ").value = product.categ;

        const productPdfInput = document.getElementById("product-pdf");

        // Si hay un PDF guardado, mostrar el nombre del archivo y el botón de eliminación
        if (product.pdf) {
            productPdfInput.value = product.pdf;
            const deletePdfButton = document.createElement("button");
            deletePdfButton.className = "btn btn-danger delete-pdf";
            deletePdfButton.innerHTML = '<i class="bi bi-trash"></i>';
            deletePdfButton.addEventListener("click", function () {
                productPdfInput.value = ""; // Borrar el nombre del archivo
                productPdfInput.type = "file"; // Cambiar el tipo de input a file para permitir actualizar el PDF
                deletePdfButton.remove(); // Remover el botón de eliminación
            });
            productPdfInput.parentNode.insertBefore(deletePdfButton, productPdfInput.nextSibling);
        }
    } else {
        // Manejar el caso en que el producto no se encuentre
        console.log("Producto no encontrado");
    }

    // Evento para guardar los cambios
    document.getElementById("edit-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Evita que se recargue la página al enviar el formulario

        // Obtener los valores del formulario
        const productId = document.getElementById("product-id").value;
        const productName = document.getElementById("product-name").value;
        const productDesc = document.getElementById("product-desc").value;
        const productUbi = document.getElementById("product-ubi").value;
        const productCant = document.getElementById("product-cant").value;
        const productCateg = document.getElementById("product-categ").value;
        const productPdf = document.getElementById("product-pdf").value;

        // Actualizar el producto en la lista de productos
        const updatedProducts = products.map((p) => {
            if (p.id === productId) {
                return {
                    id: productId,
                    name: productName,
                    desc: productDesc,
                    ubi: productUbi,
                    cant: productCant,
                    pdf: productPdf, // Actualizar el nombre del PDF
                    categ: productCateg,
                };
            } else {
                return p;
            }
        });

        // Guardar la lista actualizada en el almacenamiento local
        localStorage.setItem("products", JSON.stringify(updatedProducts));

        // Redirigir de vuelta a la lista de productos
        window.location.href = "inventario.html";
    });
});
