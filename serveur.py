from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('formatif.html') # Le fichier formatif doit être dans le dossier templates qui se trouve à la racine avec app.py

if __name__ == '__main__':
    # 0.0.0.0 makes it look for Wi-Fi and Ethernet automatically
    app.run(host='0.0.0.0', port=5001)