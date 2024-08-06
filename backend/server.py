from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import subprocess
import time
import threading


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite solicitudes desde cualquier origen

# Rutas a las carpetas de datos
folder = 'C:/Users/solre/Desktop/MAE/4.TP_maquina/web/frontend/data'
backend_folder = 'C:\\Users\\solre\\Desktop\\MAE\\4.TP_maquina\\web\\backend'

# Variable global
ultima_url_procesada = ""

def obtener_ultima_url(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        if lineas:
            return lineas[-1].strip()  # Devuelve la última línea sin espacios adicionales
        return None



def run_save_link_github():
    global ultima_url_procesada
    print("Hilo run_save_link_github iniciado")
    venv_path = 'C:/Users/solre/Desktop/MAE/4.TP_maquina/web/backend/venv/Scripts/activate'

    while True:
        try:
            command = f'"{venv_path}" && python "{os.path.join(backend_folder, "save_link_github.py")}"'
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            print("Resultado:", result.stdout)
            
            if result.returncode == 0:
                print('URL updated successfully')
                nueva_url = obtener_ultima_url(os.path.join(folder, 'known_images.txt'))
                if nueva_url != ultima_url_procesada:
                    ultima_url_procesada = nueva_url
                    print("Nueva URL detectada. Ejecutando send_url_to_openai...")
                    run_send_url_to_openai()
            else:
                print('Failed to update URL')
                print('stderr:', result.stderr)
        except Exception as e:
            print('Error:', e)
            print('Tipo de error:', type(e))
        time.sleep(20)  # Espera 20 segundos antes de ejecutar nuevamente


def run_send_url_to_openai():
    print("Hilo de send_url_to_openai iniciado")
    venv_path = 'C:/Users/solre/Desktop/MAE/4.TP_maquina/web/backend/venv/Scripts/activate'

    try:
        command = f'"{venv_path}" && python "{os.path.join(backend_folder, "send_url_to_openai.py")}"'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print("Resultado de send_url_to_openai:", result.stdout)
        
        if result.returncode == 0:
            print('Script ejecutado exitosamente.')
        else:
            print('Error al ejecutar el script.')
            print('stderr:', result.stderr)
    except Exception as e:
        print('Error:', e)
        print('Tipo de error:', type(e))



@app.route('/data/known_images.txt', methods=['GET'])
def get_last_image_url():
    try:
        # Abre el archivo para lectura
        with open(os.path.join(folder, 'known_images.txt'), 'r') as file:
            lines = file.readlines()
        if lines:
            last_url = lines[-1].strip()
            # Asegúrate de que el JSON sea válido
            return jsonify({'url': last_url}), 200
        else:
            return jsonify({'error': 'No content in file'}), 404
    except FileNotFoundError:
        # Devuelve un mensaje de error si el archivo no se encuentra
        return jsonify({'error': 'File not found'}), 404


@app.route('/data/text_output.txt', methods=['GET'])
def get_text_output():
    try:
        with open(os.path.join(folder, 'text_output.txt'), 'r') as file:
            content = file.readlines()
        return jsonify(content), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(folder, filename)


@app.route('/update_url', methods=['POST'])
def update_url():
    try:
        result = subprocess.run(['python', os.path.join(backend_folder, 'save_link_github.py')],
                                capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'message': 'URL updated successfully', 'output': result.stdout}), 200
        else:
            return jsonify({'error': 'Failed to update URL', 'details': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/test_update_url', methods=['GET'])
def test_update_url():
    try:
        result = subprocess.run(['python', os.path.join(backend_folder, 'save_link_github.py')],
                                capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'message': 'URL updated successfully', 'output': result.stdout}), 200
        else:
            return jsonify({'error': 'Failed to update URL', 'details': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    # Inicia el hilo que ejecutará el script en segundo plano
    threading.Thread(target=run_save_link_github, daemon=True).start()
    app.run(debug=True)
