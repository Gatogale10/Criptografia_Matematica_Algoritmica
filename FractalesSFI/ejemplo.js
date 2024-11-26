//Jorge Gael Lopez Figueras 
//Instituto Politecnico Nacional

// Seleccionamos el canvas y su contexto 2D
const canvas = document.getElementById('gradientCanvas');
const ctx = canvas.getContext('2d');

const selectElement = document.querySelector(".figura");
const result = document.querySelector(".result");

// Variable para almacenar la figura seleccionada
let cuadradoOriginal;

selectElement.addEventListener("change", (event) => {
  result.textContent = `Escogiste ${event.target.value}`;

  // Coordenadas originales según la figura seleccionada
  if (event.target.value === 'cuadrado') {
    cuadradoOriginal = [
        [0, canvas.height - 1000],  // Esquina inferior izquierda
        [1000, canvas.height - 1000], // Esquina inferior derecha
        [1000, canvas.height],      // Esquina superior derecha
        [0, canvas.height]         // Esquina superior izquierda
    ];
  } 
  else if (event.target.value === 'triangulo') {
    cuadradoOriginal = [
        [500, canvas.height - 1000],  // Vértice inferior izquierdo
        [1000, canvas.height],        // Vértice inferior derecho
        [0, canvas.height]           // Vértice superior izquierdo
    ];
  }

  // Asegúrate de usar cuadradoOriginal después de actualizarlo
  console.log(cuadradoOriginal); // Verifica la figura seleccionada
});







// Variables globales para almacenar las funciones
let funciones = [];

// Función para agregar una nueva transformación
function agregarFuncion() {
    const functionList = document.getElementById('functionList');
    const div = document.createElement('div');
    div.classList.add('function');
    div.innerHTML = `
        <label>f: x * <input type="number" class="scaleX" value="0.5"> + <input type="number" class="offsetX" value="0.0">, y * <input type="number" class="scaleY" value="0.5"> + <input type="number" class="offsetY" value="0"></label>
    `;
    functionList.appendChild(div);
}

// Función para obtener las funciones de transformación
function obtenerFunciones() {
    const a = canvas.height; // Obtener el valor de "a"
    funciones = []; // Limpiar las funciones

    // Obtener las transformaciones definidas por el usuario
    const functionElements = document.querySelectorAll('.function');
    functionElements.forEach(element => {
        const scaleX = parseFloat(element.querySelector('.scaleX').value);
        const offsetX = parseFloat(element.querySelector('.offsetX').value);
        const scaleY = parseFloat(element.querySelector('.scaleY').value);
        const offsetY = parseFloat(element.querySelector('.offsetY').value);

        // Crear la función de transformación con los parámetros
        const func = ([x, y]) => [x * scaleX + offsetX, y * scaleY + (a-a*scaleY) - offsetY];
        funciones.push(func); // Agregar la función a la lista
    });
}

// Función recursiva para aplicar las transformaciones y dibujar los cuadrados
const dibujarRecursivo = (puntos, nivel) => {
    if (nivel === 0)
        {
            // Aplicamos las funciones de transformación a los puntos actuales
            funciones.forEach(f => {
            const puntosTransformados = puntos.map(f);
            dibujarCuadrado(puntosTransformados, getRandomColor()); // Dibujamos los cuadrados transformados
        });
            

            return;

        }  // Condición de parada (no hacer nada si llegamos al nivel 0)
    
    
    
    // Llamamos recursivamente para los nuevos cuadrados (con un nivel menor)
    funciones.forEach(f => {
        const puntosTransformados = puntos.map(f);
        dibujarRecursivo(puntosTransformados, nivel - 1);
    });
};

// Función para dibujar un cuadrado
const dibujarCuadrado = (puntos, color) => {
    ctx.beginPath();
    ctx.moveTo(...puntos[0]); // Moverse al primer punto
    for (let i = 1; i < puntos.length; i++) {
        ctx.lineTo(...puntos[i]); // Dibujar línea a cada punto
    }
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.stroke();
};

// Función para obtener un color aleatorio
function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random()* 256);
    const b = Math.floor(Math.random()* 256);
    return `rgb(${r}, ${g}, ${b})`;
}

// Función que se llama cuando el usuario hace clic en "Dibujar"
function iniciarDibujo() {
    // Obtener el valor de recursiones
    const n = parseInt(document.getElementById('recursiones').value);
    
    // Verificar que el valor de n sea un número válido y mayor que 0
    if (isNaN(n) || n <= 0) {
        
        funciones.forEach(f => {
            const puntosTransformados = cuadradoOriginal.map(f);
           dibujarCuadrado(puntosTransformados, getRandomColor()); // Dibujamos los cuadrados transformados
       });

        return;
    }

    // Limpiar el canvas antes de dibujar
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Obtener las funciones de transformación
    obtenerFunciones();

    // Llamar a la función recursiva con el número de recursiones proporcionado
    dibujarRecursivo(cuadradoOriginal, n);
}

// Capturar el evento de presionar "Enter" para el botón
document.querySelector('button').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        iniciarDibujo();
    }
});
// Añadir el event listener para el botón
document.getElementById('btnDibujar').addEventListener('click', iniciarDibujo);