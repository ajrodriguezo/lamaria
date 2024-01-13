document.addEventListener("DOMContentLoaded", function() {
  // Obtén la referencia a la imagen y ajusta el clip-path
var image = document.getElementById("image-1");

var total_ciclo_str = document.getElementById('total_ciclo').dataset.variable;
var porcentajeVisible = parseInt(total_ciclo_str, 10);

// Calcula la coordenada y para el porcentaje dado
var yCoordinate = 100 - porcentajeVisible;

// Aplica el clip-path con la coordenada y calculada
image.style.clipPath = `polygon(0 ${yCoordinate}%, 100% ${yCoordinate}%, 100% 100%, 0 100%)`;
});

var ctx = document.getElementById('myChart').getContext('2d');

var datos_grafica = document.getElementById('datos_grafica').dataset.variable;
datos_grafica = datos_grafica.replace(/'/g, '"');
var arreglo_grafica = JSON.parse(datos_grafica);

Chart.defaults.font.size = 16;
Chart.defaults.font.family = 'Arial';
Chart.defaults.color = '#eee127';

var myChart = new Chart(ctx, {
    type: 'line',
    defaultFontSize: 18,
    data: {
        datasets: [{
            label: 'gr acumulados por semana',
            data: arreglo_grafica,
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,

        }],
        font: {
            size: 30
        }
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Semanas'
                },
                ticks: {
                    stepSize: 1, // Configura el tamaño del paso para que sea 1 (entero)
                    precision: 0 // Configura la precisión para que no se muestren decimales
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
                text: 'Ciclo de cosecha'
            }
        }
    }
});


document.getElementById('gracumulados').innerText = 'Nuevo Contenido 1';
document.getElementById('faltante').innerText = 'Nuevo Contenido 1';
document.getElementById('vendidoahoy').innerText = 'Nuevo Contenido 1';
document.getElementById('promedioprecio').innerText = 'Nuevo Contenido 1';

