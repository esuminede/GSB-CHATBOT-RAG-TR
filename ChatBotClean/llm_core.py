import pickle 
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import requests
import json
import pyodbc
from datetime import datetime
import socket

with open("faiss_index.pkl", "rb") as f:
    data = pickle.load(f)

index = data["index"]
sorular = data["sorular"]
cevaplar = data["cevaplar"]
adresler = data["adresler"]
kurumlar = data["kurum"]
model_name = data["model"]
model = SentenceTransformer(model_name)

def truncate_text(text, max_chars=750):
    if len(text) > max_chars:
        return text[:max_chars].rsplit('.', 1)[0] + "..."
    return text

def generate_llm_answer(user_question, kb_cevap, adres, kurum):
    prompt = f"""
Sen bir dijital bilgi asistanısın. Aşağıda verilen kullanıcı sorusu ve veritabanından elde edilen bilgiye dayanarak sadece kısa, kurumsal ve net bir Türkçe cevap ver.

 Kurallar:
- Cevabın yalnızca veritabanındaki bilgiye dayanmalı.
- Tahmin etme, yorumlama yapma.
- Selamlaşma sorularına "Merhaba!" de ve başka bir şey söyleme.
- Bilgi yetersizse hiç cevap verme.
- Cevabın sonunda sadece aşağıdaki bağlantıyı ver.

 Kullanıcı Sorusu:
{user_question}

 Veritabanı Bilgisi:
{kb_cevap}

 Kurum:
{kurum}

 Bağlantı:
{adres}

Yalnızca cevap:"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral:7b-instruct", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]
    
def cevap_uret(soru, client_ip = ""):
    q_vec = model.encode([f"query: {soru}"], convert_to_tensor=True)
    D, I = index.search(np.array(q_vec), 1)
    distance = float(D[0][0])
    idx = I[0][0]

    en_yakin_soru = sorular[idx]
    en_yakin_id = data["idler"][idx] + 1  
    
    
    if distance > 0.3:
        log_soru(soru, "", client_ip, en_yakin_soru, float(distance), en_yakin_id, 0)
        return "Bu konuda yeterli bilgi bulunmamaktadır.", distance, 0

        
    kb_cevap = truncate_text(cevaplar[idx])
    yanit = generate_llm_answer(soru, kb_cevap, adresler[idx], kurumlar[idx])
    log_soru(soru, yanit, client_ip, en_yakin_soru, float(distance), en_yakin_id, 1)
    return yanit, float(distance), 1
    

def log_soru(soru, cevap, ip, en_yakin_soru, distance, soru_id=None, yansitildi=None):
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=;"
            "Database=;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ChatLog (Soru, Cevap, Tarih, IP, EnYakinSoru, Distance, EslesenID, CevapYansitildiMi) 
            VALUES (?, ?, GETDATE(), ?, ?, ?, ?, ?)
        """, (soru, cevap, ip, en_yakin_soru, float(distance), soru_id, yansitildi))
        
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Loglama hatası: {e}")
    