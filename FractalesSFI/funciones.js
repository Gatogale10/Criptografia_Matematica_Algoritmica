// Seleccionamos el canvas y su contexto 2D
const canvas = document.getElementById('gradientCanvas');
const ctx = canvas.getContext('2d');

// Valor para mover parte inferior izquierda
const a = 500;

// Funciones de transformación
const f1 = ([x, y]) => [x * 0.5, y * 0.5 + a]; // Escalado a la mitad del tamaño original
const f2 = ([x, y]) => [x * 0.5 + 500, y * 0.5 + a]; // Escalado y trasladado hacia la derecha
const f3 = ([x, y]) => [x * 0.5 + 250, y * 0.5 + a - 500]; // Escalado y trasladado hacia abajo

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

// Coordenadas originales del cuadrado (esquinas)
const cuadradoOriginal = [
    [0, canvas.height - 1000],  // Esquina inferior izquierda
    [1000, canvas.height -1000], // Esquina inferior derecha
    [1000, canvas.height],      // Esquina superior derecha
    [0, canvas.height]         // Esquina superior izquierda
];

// Función recursiva para aplicar las transformaciones y dibujar los cuadrados
const dibujarRecursivo = (puntos, nivel) => {
    if (nivel === 0)
        {
            const cuadradonuevo = puntos.map(f1);
            const cuadradonuevo1 = puntos.map(f2);
            const cuadradonuevo2 = puntos.map(f3);
            // Dibujamos los cuadrados transformados
        dibujarCuadrado(cuadradonuevo, "rgba(0, 255, 0, 0.5)");  // Cuadrado verde
        dibujarCuadrado(cuadradonuevo1, "rgba(0, 255, 24, 0.5)"); // Cuadrado verde claro
        dibujarCuadrado(cuadradonuevo2, "rgba(255, 0, 0, 0.5)");  // Cuadrado rojo
        return;

        }  // Condición de parada (no hacer nada si llegamos al nivel 0)
    
    // Aplicamos las tres funciones de transformación a los puntos actuales
    const cuadradonuevo = puntos.map(f1);
    const cuadradonuevo1 = puntos.map(f2);
    const cuadradonuevo2 = puntos.map(f3);
    
    

    // Llamamos recursivamente para los nuevos cuadrados (con un nivel menor)
    dibujarRecursivo(cuadradonuevo, nivel - 1);
    dibujarRecursivo(cuadradonuevo1, nivel - 1);
    dibujarRecursivo(cuadradonuevo2, nivel - 1);
};

// Función que se llama cuando el usuario hace clic en el botón "Dibujar"
function iniciarDibujo() {
    // Obtener el valor ingresado por el usuario
    const n = parseInt(document.getElementById('recursiones').value);
    
    // Limpiar el canvas antes de dibujar
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Llamar a la función recursiva con el número de recursiones proporcionado
    dibujarRecursivo(cuadradoOriginal, n);
}


