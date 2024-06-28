
/*Funcion para buscar productos */
document.addEventListener("DOMContentLoaded", function () {
  function setupSearch(listId){

    const searchBar = document.querySelector('input[type="search"]');
    const productRows = document.querySelectorAll(`#${listId} tbody tr`);
  
    searchBar.addEventListener("input", function (e) {
      const searchTerm = searchBar.value.toLowerCase();
  
      productRows.forEach(function (row) {
        let found = false;
  
        row.querySelectorAll("td").forEach(function (cell) {
          const cellText = cell.textContent.toLowerCase();
          if (cellText.includes(searchTerm)) {
            found = true;
          }
        });
  
        if (found) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });
    });
  }
  /*Configurar busquedas */
  setupSearch("product-table");
  setupSearch("supplier-table");
  setupSearch("modification-table");
}); 