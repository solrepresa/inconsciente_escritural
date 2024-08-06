''' Código 2 - Unidad Cerebro. Este codigo tomas las url guardadas en un txt y las envia a open ai. El codigo devuelve un '''

from openai import OpenAI

client = OpenAI()

# Leer la última URL del archivo txt
def obtener_ultima_url(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        if lineas:
            return lineas[-1].strip()  # Devuelve la última línea sin espacios adicionales
        return None

# Guardar el texto en el archivo text_output.txt
def guardar_texto(ruta_archivo, texto):
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(texto)

# Ruta del archivo que contiene las URLs
ruta_archivo = 'C:/Users/solre/Desktop/MAE/4.TP_maquina/web/frontend/data/known_images.txt'
ruta_archivo_salida = 'C:/Users/solre/Desktop/MAE/4.TP_maquina/web/frontend/data/text_output.txt'

# Obtener la última URL
url = obtener_ultima_url(ruta_archivo)


# Crear la solicitud a la API de OpenAI
if url:
    # Crear la solicitud a la API de OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Crea una interpretación basada en mis ideas y pensamientos. Elabora una narrativa concisa y evocadora, revelando patrones y resonancias que reflejen mi subjetividad y perspectiva. El texto debe fusionar múltiples enfoques y miradas en una síntesis evocadora y compacta. NO HACER referencia al papel, al cuaderno, al lienzo o a la escritura como interfaz material. La extensión debe ser de 2 oraciones. Asegúrate de emplear diferentes estructuras gramaticales y estilos en la redacción para evitar repeticiones."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                            "detail": "high"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    # Extraer el texto de la respuesta y guardarlo en el archivo
    texto = response.choices[0].message.content
    guardar_texto(ruta_archivo_salida, texto)
else:
    print("No se encontró ninguna URL en el archivo.")

print(texto)