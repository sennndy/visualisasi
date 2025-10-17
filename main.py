# app.py
from flask import Flask

# Membuat instance aplikasi Flask
app = Flask(__name__)

# Membuat rute utama (root route)
@app.route('/')
def hello_world():
    return 'Halo, Flask! (Tanpa venv) 👋'

# Jalankan aplikasi
if __name__ == '__main__':
    # Server akan berjalan di http://127.0.0.1:5000/
    app.run(debug=True)