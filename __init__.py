from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
#j'ai oublié le commit
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encrypt(valeur):
    key = request.args.get('key')
    if not key:
        return "Erreur : clé de chiffrement manquante (?key=...)"
    try:
        f = Fernet(key.encode())
        encrypted = f.encrypt(valeur.encode()).decode()
        return f"Valeur chiffrée : {encrypted}"
    except Exception as e:
        return f"Clé invalide : {str(e)}"

@app.route('/decrypt/<string:valeur>')
def decrypt(valeur):
    key = request.args.get('key')
    if not key:
        return "Erreur : clé de déchiffrement manquante (?key=...)"
    try:
        f = Fernet(key.encode())
        decrypted = f.decrypt(valeur.encode()).decode()
        return f"Valeur déchiffrée : {decrypted}"
    except InvalidToken:
        return "Erreur : la clé ne permet pas de déchiffrer cette valeur"
    except Exception as e:
        return f"Clé invalide : {str(e)}"
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
