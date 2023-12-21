document.addEventListener("DOMContentLoaded", function() {
  // Obtén la referencia a la imagen y ajusta el clip-path
var image = document.getElementById("image-1");
var porcentajeVisible = 85; 

// Calcula la coordenada y para el porcentaje dado
var yCoordinate = 100 - porcentajeVisible;

// Aplica el clip-path con la coordenada y calculada
image.style.clipPath = `polygon(0 ${yCoordinate}%, 100% ${yCoordinate}%, 100% 100%, 0 100%)`;
});

var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Ciclo 1',
            data: [
                { x: 1, y: 70 },
                { x: 2, y: 140 },
                { x: 3, y: 400 },
                { x: 4, y: 1400 },
                { x: 5, y: 2500 }
            ],
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Semanas'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Peso en gr'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Ciclo 1'
            }
        }
    }
});


document.getElementById('gracumulados').innerText = 'Nuevo Contenido 1';
document.getElementById('faltante').innerText = 'Nuevo Contenido 1';
document.getElementById('vendidoahoy').innerText = 'Nuevo Contenido 1';
document.getElementById('promedioprecio').innerText = 'Nuevo Contenido 1';