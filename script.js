window.onload = function() {
  // Carga los datos del inventario y precios en la página
  loadInventoryData();
  loadPricesData();
}

function loadInventoryData() {
  var inventario = {
      pesca: {
          cantidad: 800,
          unidad: 'gr',
          precio: 300,
          precioUnitario: 375
      }
  };

  var inventarioDiv = document.getElementById('inventario');

  for (var tipo in inventario) {
      var item = inventario[tipo];
      var divItem = document.createElement('div');
      divItem.innerHTML = 'Cantidad: ' + item.cantidad + ' ' + item.unidad +
                          '<br>Precio: ' + item.precio + ' €' +
                          '<br>Precio unitario: ' + item.precioUnitario + ' €/kg';
      inventarioDiv.appendChild(divItem);
  }
}

function loadPricesData() {
  var precios = [
      {semana: 1, precio: 350},
      {semana: 2, precio: 300},
      {semana: 3, precio: 250},
      {semana: 4, precio: 200},
      {semana: 5, precio: 150}
  ];

  var preciosDiv = document.getElementById('precios');

  for (var i = 0; i < precios.length; i++) {
      var precio = precios[i];
      var divPrecio = document.createElement('div');
      divPrecio.innerHTML = 'Semana ' + precio.semana + ': ' + precio.precio + ' €';
      preciosDiv.appendChild(divPrecio);
  }
}