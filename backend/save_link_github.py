''' Código 1 - Unidad Cerebro. Este codigo guarda en un archivo txt las nuevas imagenes q encuentra en un repo de github.'''

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Configuración
GITHUB_URL = 'https://github.com/solrepresa/inconsciente_escritural/tree/main/images'
KNOWN_IMAGES_FILE = 'C:\\Users\\solre\\Desktop\\MAE\\4.TP_maquina\\web\\frontend\\data\\known_images.txt'  # Archivo para almacenar las direcciones conocidas


def get_image_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(href.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
            image_links.append('https://github.com' + href.replace('/blob/', '/raw/'))
    return image_links

def load_known_images(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()

def save_new_images(file_path, new_images):
    with open(file_path, 'a') as file:
        for image in new_images:
            file.write(image + '\n')
            print(f'{datetime.now()} - Nueva imagen encontrada: {image}')

def main():
    try:
        # Obtener la lista de enlaces de imágenes en el repositorio
        image_links = set(get_image_links(GITHUB_URL))

        # Cargar las imágenes conocidas desde el archivo
        known_images = load_known_images(KNOWN_IMAGES_FILE)

        # Determinar las nuevas imágenes
        new_images = image_links - known_images

        if new_images:
            # Guardar las nuevas imágenes en el archivo
            save_new_images(KNOWN_IMAGES_FILE, new_images)

    except Exception as e:
        print(f'{datetime.now()} - Error: {e}')


if __name__ == '__main__':
    main()
