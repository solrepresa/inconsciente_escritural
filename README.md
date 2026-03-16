# Inconsciente Escritural

**Motor interpretativo de instalación artística**  
Maestría en Artes Electrónicas — UNTREF

---

## ¿Qué es?

*Inconsciente Escritural* es una instalación artística que expone un cuaderno de notas íntimas —el inconsciente escritural de su autora— a una máquina que lo lee de forma autónoma.

Un mecanismo motorizado voltea las páginas del cuaderno de manera automática. Una cámara fotografía cada página al descubrirse, y esa imagen es enviada a la API de OpenAI (GPT-4o), que genera una interpretación poética y evocadora del pensamiento escrito. El resultado —imagen y texto— se proyecta en pantalla en tiempo real.


---

## Estado del proyecto

| Módulo | Estado |
|---|---|
| Mecanismo de volteo de páginas | ✅ Implementado |
| Captura fotográfica automática | 🔧 Pendiente de integración |
| Subida de imágenes al repositorio | ✅ Implementado (manual/semi-automático) |
| Detección de nuevas imágenes | ✅ Implementado |
| Interpretación con IA (GPT-4o) | ✅ Implementado |
| Visualización en pantalla (p5.js) | ✅ Implementado |

---

## Flujo de la instalación

```
Cuaderno con escritura íntima (el inconsciente)
      ↓
Mecanismo motorizado voltea las páginas
      ↓
[pendiente] Cámara fotografía cada página
      ↓
Foto → sube a /images en este repositorio
      ↓
[save_link_github.py] detecta la nueva imagen (cada 20 seg)
      ↓
[send_url_to_openai.py] envía la imagen a GPT-4o
      ↓
GPT-4o genera una interpretación poética (2 oraciones)
      ↓
[frontend p5.js] proyecta imagen + texto en pantalla
```

---

## Estructura del proyecto

```
inconsciente_escritural/
├── backend/
│   ├── server.py                # Servidor Flask — orquesta los hilos y expone la API
│   ├── save_link_github.py      # Detecta nuevas imágenes en el repo de GitHub
│   ├── send_url_to_openai.py    # Envía la imagen a GPT-4o y guarda la interpretación
│   └── requirements.txt         # Dependencias Python
├── frontend/
│   ├── index.html               # Página de la instalación
│   ├── index.js                 # Sketch en p5.js — muestra imagen e interpretación
│   └── data/
│       ├── known_images.txt     # URLs de imágenes ya procesadas
│       └── text_output.txt      # Última interpretación generada por la IA
└── images/                      # Fotografías del cuaderno (input de la instalación)
```

---

## Requisitos

- Python 3.10+
- Una clave de API de OpenAI con acceso a `gpt-4o-mini`
- Conexión a internet (para acceder a GitHub y a la API de OpenAI)
- Un navegador moderno para el frontend (p5.js)

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/solrepresa/inconsciente_escritural.git
cd inconsciente_escritural
```

### 2. Crear y activar un entorno virtual

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la clave de API de OpenAI

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-..."

# macOS / Linux
export OPENAI_API_KEY="sk-..."
```

### 5. Ajustar las rutas locales

En `server.py`, `save_link_github.py` y `send_url_to_openai.py`, reemplazar las rutas absolutas hardcodeadas con las rutas correspondientes en tu sistema.

> **Nota:** En una versión futura estas rutas pueden centralizarse en un archivo `.env`.

### 6. Iniciar el servidor

```bash
python server.py
```

El servidor Flask quedará corriendo en `http://127.0.0.1:5000` y monitoreará el repositorio cada 20 segundos en busca de nuevas imágenes.

### 7. Abrir el frontend

Abrir `frontend/index.html` en el navegador. La instalación mostrará la última página fotografiada junto con su interpretación generada por IA.

---

## Cómo agregar una nueva imagen (flujo actual)

Hasta integrar la captura automática, subir manualmente una fotografía del cuaderno a la carpeta `/images` del repositorio. El sistema la detectará en el próximo ciclo (≤ 20 segundos), la enviará a GPT-4o y actualizará la pantalla.

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Servidor backend | Python + Flask |
| Scraping de imágenes | BeautifulSoup4 + Requests |
| Visión por computadora e IA | OpenAI API (`gpt-4o-mini`) |
| Visualización | p5.js |
| Control de concurrencia | Python Threading |

---

## Contexto artístico

Esta instalación fue desarrollada como trabajo práctico para la **Maestría en Artes Electrónicas (MAE)** de la **Universidad Nacional de Tres de Febrero (UNTREF)**, Buenos Aires, Argentina.

La obra pone en escena una tensión entre lo íntimo y lo automático: un cuaderno de notas personales —escritura privada, no performativa— es expuesto a una máquina que lo hojea y a una inteligencia artificial que lo interpreta. La IA no responde al visitante sino al inconsciente de la artista. El sistema lee lo que ya estaba escrito.

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
