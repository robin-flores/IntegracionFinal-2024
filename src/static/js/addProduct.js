const productForm = document.getElementById("product-form");
const productAlert = document.getElementById("product-alert");

productForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const productId = document.getElementById("product-id").value.trim();
  const productName = document.getElementById("product-name").value.trim();
  const productDesc = document.getElementById("product-desc").value.trim();
  const productUbi = document.getElementById("product-ubi").value.trim();
  const productCant = parseInt(document.getElementById("product-cant").value, 10);
  const productPdf = document.getElementById("product-pdf").files[0];
  const productCateg = document.getElementById("product-categ").value;

  const newProduct = {
    id: productId,
    name: productName,
    desc: productDesc,
    ubi: productUbi,
    cant: productCant,
    pdf: productPdf ? productPdf.name : "",
    categ: productCateg,
  };

  const products = getProductsFromLocalStorage();

  const productExists = products.some((product) => product.id === productId);

  if (productExists) {
    productAlert.classList.remove("d-none");
    productAlert.textContent = "El producto con este número de serie ya existe.";
    return;
  }

  productAlert.classList.add("d-none");

  // GUARDAR EN LOCAL STORAGE
  products.push(newProduct);
  setProductsInLocalStorage(products);


  productForm.reset();


  window.location.href = "/inventario/editor";
});


function getProductsFromLocalStorage() {
  const productsJSON = localStorage.getItem("products");
  return productsJSON ? JSON.parse(productsJSON) : [];
}

function setProductsInLocalStorage(products) {
  localStorage.setItem("products", JSON.stringify(products));
}
