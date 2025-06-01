# Trendyol Ürün Yorum Analizi

Bu proje, Trendyol'da satılan ürünlerin yorumlarını analiz ederek duygu analizi yapar ve ürünleri karşılaştırır.

## Özellikler

- Ürün yorumlarını otomatik toplama
- Duygu analizi
- Ürün karşılaştırma (maksimum 10 ürün)
- En iyi ve en kötü 5 konu analizi
- Görsel grafikler ile sonuç gösterimi

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. NLTK verilerini indirin:
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

4. Tarayıcınızda `http://localhost:5000` adresine gidin.

## Kullanım

1. Ana sayfada "Ürün Ekle" bölümünden ürün adı ve Trendyol ürün URL'sini girin
2. En fazla 10 ürün ekleyebilirsiniz
3. "Ürünleri Analiz Et" butonuna tıklayarak analizi başlatın
4. Sonuçlar görsel grafikler ve detaylı bilgiler ile gösterilecektir

## Geliştirme

- HTML dosyaları `templates` klasöründe
- CSS dosyaları `static/css` klasöründe
- JavaScript dosyaları `static/js` klasöründe bulunmaktadır

## Lisans

MIT
# tyyorum2
