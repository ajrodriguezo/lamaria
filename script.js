document.addEventListener("DOMContentLoaded", function() {
  // Obtén la referencia a la imagen y ajusta el clip-path
  var image = document.getElementById("image-1");
  var porcentajeVisible = 50; // Puedes cambiar este valor según tus necesidades

  // Calcula la coordenada y para el porcentaje dado
  var yCoordinate = 100 - porcentajeVisible;

  // Aplica el clip-path con la coordenada y calculada
  image.style.clipPath = `polygon(0 ${yCoordinate}%, 100% ${yCoordinate}%, 100% 100%, 0 100%)`;
});