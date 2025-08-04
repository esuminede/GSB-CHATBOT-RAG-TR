import pyodbc
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from tqdm import tqdm

# MSSQL bağlantısı
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=;"  
    "Database=;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

cursor.execute("SELECT ID, SORU, CEVAP, ADRES, GOZLEMCIYORUM, KURUM FROM GSB")
rows = cursor.fetchall()
conn.close()


print(" Embedding modeli yükleniyor...")
model = SentenceTransformer('embed model')

sorular = [row[1] for row in rows]
cevaplar = [row[2] for row in rows]
adresler = [row[3] for row in rows]
kurum = [row[5] for row in rows]
idler = [row[0] for row in rows]

embedding_texts = [
    f"query: {sorular[i]} {cevaplar[i]} {adresler[i]} {kurum[i]}" 
    for i in range(len(sorular))
    ]




print("Sorular vektöre dönüştürülüyor...")
soru_embeddings = model.encode(embedding_texts, convert_to_numpy=True)
# FAISS index oluştur
#index = faiss.IndexFlatL2(soru_embeddings.shape[1])
#index.add(soru_embeddings)

index = faiss.IndexFlatL2(soru_embeddings.shape[1])
index.add(soru_embeddings)


with open("faiss_index.pkl", "wb") as f:
    pickle.dump({
        "index": index,
        "sorular": sorular,
        "cevaplar": cevaplar,
        "idler": idler,
        "adresler": adresler,
        "kurum": kurum,
        "model": ''
    }, f)

print(" FAISS index başarıyla oluşturuldu ve kaydedildi.")
print(" Vektör indexleme işlemi tamamlandı.")