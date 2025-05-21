from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Clé temporaire (session) – version GET simple
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encrypt_get(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:valeur>')
def decrypt_get(valeur):
    try:
        valeur_bytes = valeur.encode()
        decrypted = f.decrypt(valeur_bytes)
        return f"Valeur déchiffrée : {decrypted.decode()}"
    except InvalidToken:
        return "Erreur : valeur non déchiffrable"
    except Exception as e:
        return f"Erreur : {str(e)}"

# Génération de clé personnelle (GET)
@app.route('/generate-key/', methods=['GET'])
def generate_key():
    key = Fernet.generate_key().decode()
    return jsonify({'key': key})

# Chiffrement personnalisé via POST
@app.route('/encrypt/', methods=['POST'])
def encrypt_post():
    try:
        data = request.get_json()
        key = data['key'].encode()
        message = data['message'].encode()

        f = Fernet(key)
        encrypted_token = f.encrypt(message).decode()
        return jsonify({'encrypted_token': encrypted_token})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Déchiffrement personnalisé via POST
@app.route('/decrypt/', methods=['POST'])
def decrypt_post():
    try:
        data = request.get_json()
        key = data['key'].encode()
        token = data['token'].encode()

        f = Fernet(key)
        decrypted_message = f.decrypt(token).decode()
        return jsonify({'decrypted_message': decrypted_message})
    except InvalidToken:
        return jsonify({'error': 'Token invalide ou clé incorrecte'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Pour Alwaysdata
application = app

if __name__ == "__main__":
    app.run(debug=True)
