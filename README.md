# GSB-CHATBOT-RAG-TR
# 🇹🇷 Türkçe RAG Tabanlı Chatbot (FAISS + MSSQL + Flask)

Bu proje, sadece **veritabanındaki sorulara** yanıt verebilen, yüksek hassasiyetli, Türkçe destekli bir chatbot sistemidir.  

##  Teknolojiler

-  **RAG (Retrieval-Augmented Generation)** mimarisi  
-  **FAISS** tabanlı semantik arama  
-  **MSSQL** veritabanı ile bağlantılı  
-  **Flask** tabanlı web arayüz  
-  Python backend, HTML/CSS/JS frontend  
-  Kullanıcı soruları detaylı şekilde **loglanır**

##  Özellikler

- Veritabanında olmayan sorulara cevap vermez, yalnızca “bilgim yok” der
- MSSQL'den gelen sorulara `sentence-transformers` modeli ile vektör tabanlı arama yapılır
- En yakın eşleşen soru, cevap, benzerlik oranı (`distance`) ve kullanıcı IP’si MSSQL'e loglanır
- Cevaplar link içeriyorsa tıklanabilir hâlde gösterilir
- Kullanıcıya “Bu cevabı beğendiniz mi?” sorusu sorulur (isteğe bağlı)
- `distance` eşiği özelleştirilebilir (örn. 0.3 altında ise cevap yansıtılır)

##  Kurulum

```bash
llm_core.py dosyasında bulunan sütun isimlerini mssql ya da farklı bir server'da bir database oluşturup tabloları bizim sütunlarımızca oluşturursanız daha düzgün çalışan bir log sistemi elde edersiniz. 
git clone https://github.com/kullaniciadi/chatbot-proje.git
cd chatbot-proje
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

