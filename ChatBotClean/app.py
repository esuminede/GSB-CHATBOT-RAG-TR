from flask import Flask, request, jsonify, render_template
from llm_core import cevap_uret
import pyodbc

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cevap', methods=['POST'])  
def cevap():
    data = request.get_json()
    soru = data.get("soru", "")
    
    if not soru:
        return jsonify({"hata": "Soru boş olamaz."}), 400
    
    client_ip = request.remote_addr
    yanit, distance, yansitildi= cevap_uret(soru, client_ip)
    return jsonify({"cevap": yanit, "distance": float(distance), "yansitildi": yansitildi})

@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    soru = data.get("soru", "")
    begeni = data.get("begeni", None)

    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=;"
            "Database="
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ChatLog
            SET BegenildiMi = ?
            WHERE Soru = ?
        """, (begeni, soru))
        conn.commit()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        print("Beğeni log hatası:", e)
        return jsonify({"ok": False}), 500



if __name__ == "__main__":
    app.run(debug=True)


