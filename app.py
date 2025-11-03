from flask import Flask, request, jsonify
import paramiko
import os

app = Flask(__name__)

# Configuración de tu servidor Namecheap
SFTP_HOST = "4lpes.com"
SFTP_PORT = 21098
SFTP_USER = "llpekgwy"
SFTP_PASS = "Argentina2025*"
SFTP_PATH = "/home/llpekgwy/public_html/public/uploads/"

# --------------------- Endpoint para subir imágenes ---------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Archivo sin nombre"}), 400

    try:
        # Conexión SFTP
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Guardar archivo en hosting
        remote_path = os.path.join(SFTP_PATH, file.filename)
        sftp.putfo(file.stream, remote_path)
        
        sftp.close()
        transport.close()
        
        return jsonify({"message": "Archivo subido correctamente", 
                        "url": f"http://{SFTP_HOST}/uploads/{file.filename}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Ejecutar la app ---------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
