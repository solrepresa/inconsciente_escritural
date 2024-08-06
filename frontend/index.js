let img;
let imgLoaded = false;
let imageURL = ''; // URL de la imagen que se leerá del archivo
let textToDisplay = ''; // Texto a mostrar
const textMargin = 20; // Margen para el texto

function processUrls(data) {
  console.log("Datos recibidos del backend:", data);

  if (data && data.url) {
    imageURL = data.url.trim();
    console.log("URL original:", imageURL);

    // Modificar la URL si es necesario
    if (imageURL.includes('https://github.com/')) {
      imageURL = imageURL.replace('https://github.com/', 'https://raw.githubusercontent.com/');
      imageURL = imageURL.replace('/raw/main/', '/main/');

      console.log("URL modificada:", imageURL);

      // Cargar la imagen usando la URL modificada
      let proxyURL = 'https://cors-anywhere.herokuapp.com/';
      img = loadImage(proxyURL + imageURL, imageLoaded, imageFailed);

    } else {
      console.error("La URL no necesita modificaciones.");
    }
  } else {
    console.error("La respuesta del backend no contiene una URL.");
  }
}

function preload() {
  loadJSON('http://127.0.0.1:5000/data/known_images.txt', processUrls, handleError);
  loadJSON('http://127.0.0.1:5000/data/text_output.txt', processText); // Cargar el archivo de texto
}

function processText(data) {
  if (data.length > 0) {
    textToDisplay = data[0].trim();
    console.log("Texto cargado:", textToDisplay);
  } else {
    console.error("El archivo de texto está vacío.");
  }
}

function imageLoaded() {
  imgLoaded = true;
  console.log("Imagen cargada con éxito.");
}

function imageFailed() {
  console.error("No se pudo cargar la imagen. Verifica la URL.");
}

function handleError(error) {
  console.error("No se pudo cargar el archivo:", error);
}

function setup() {
  createCanvas(windowWidth, windowHeight); // Crear el lienzo del tamaño de la ventana
  noLoop(); // Para que el sketch no se dibuje continuamente
  textFont('Arial'); // Fuente del texto
  textSize(18); // Tamaño del texto
  textAlign(LEFT, TOP); // Alineación del texto
}

function draw() {
  background(0); // Fondo negro

  if (imgLoaded) {
    let imgWidth = width * 2 / 3; // Ancho de la imagen (2/3 del ancho de la pantalla)
    let imgHeight = img.height * (imgWidth / img.width); // Altura proporcional de la imagen

    // Calcular la posición de la imagen para centrarla horizontalmente y ubicarla en la parte superior
    let imgX = (width - imgWidth) / 2;
    let imgY = 0; // Imagen ubicada en la parte superior

    // Dibujar la imagen
    image(img, imgX, imgY, imgWidth, imgHeight);

    // Dibujar la franja negra en el tercio restante
    fill(0); // Color negro
    noStroke(); // Sin borde
    rect(0, imgHeight, width, height - imgHeight); // Franja negra en el tercio inferior

    // Mostrar el texto en la franja negra
    fill(255); // Color blanco para el texto
    let textX = textMargin;
    let textY = imgHeight + textMargin;
    let textWidth = width - 2 * textMargin; // Ancho disponible para el texto
    let textHeight = height - imgHeight - 2 * textMargin; // Altura disponible para el texto

    // Ajustar el texto para que se ajuste al área del rectángulo negro
    textWrap(WORD); // Ajustar el texto a la palabra
    text(textToDisplay, textX, textY, textWidth); // Mostrar el texto dentro del área definida

  } else {
    
    // Mensaje de carga si la imagen no está lista
    fill(0); // Color negro
    textSize(24); // Tamaño del texto de carga
    textAlign(CENTER, CENTER); // Alineación del texto
    text("Cargando imagen...", width / 2, height / 2);
  }
}

