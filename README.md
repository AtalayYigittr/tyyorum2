# 🛍️ Trendyol Ürün Yorum Analizi

Bu web uygulaması, Trendyol'daki ürün yorumlarını otomatik olarak analiz eder, duygu analizi yapar ve ürünleri karşılaştırmanıza olanak sağlar.

![Uygulama Önizlemesi](screenshot.png)

## ✨ Özellikler

- 🤖 Otomatik yorum toplama ve analiz
- 📊 Gelişmiş duygu analizi
- 🔄 10 ürüne kadar karşılaştırma
- 📈 Görsel grafiklerle sonuç gösterimi
- 🏷️ En çok bahsedilen konuların analizi
- 🎯 Olumlu/olumsuz yorum oranları
- 📱 Mobil uyumlu tasarım

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Git

### Adımlar

1. Repository'yi klonlayın:
```bash
git clone https://github.com/yourusername/trendyol-review-analysis.git
cd trendyol-review-analysis
```

2. Virtual environment oluşturun ve aktive edin:
```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux için
# veya
.\venv\Scripts\activate  # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı başlatın:
```bash
python app.py
```

5. Tarayıcınızda şu adrese gidin:
```
http://localhost:5000
```

## 📝 Kullanım

1. **Ürün Ekleme:**
   - "Ürün Ekle" bölümünden ürün adını girin
   - Trendyol ürün URL'sini yapıştırın
   - "Ekle" butonuna tıklayın

2. **Analiz:**
   - İstediğiniz kadar ürün ekleyin (max. 10)
   - "Ürünleri Analiz Et" butonuna tıklayın
   - Sonuçları bekleyin

3. **Sonuçlar:**
   - Karşılaştırmalı duygu analizi grafiği
   - Her ürün için detaylı analiz
   - En çok bahsedilen konular
   - Örnek yorumlar

## 🔧 Geliştirme

Proje yapısı:
```
├── app.py              # Flask uygulaması
├── requirements.txt    # Python bağımlılıkları
├── static/            # Statik dosyalar
│   ├── css/          # Stil dosyaları
│   └── js/           # JavaScript dosyaları
└── templates/         # HTML şablonları
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing`)
5. Bir Pull Request oluşturun

## ⚠️ Notlar

- Bu uygulama eğitim ve araştırma amaçlıdır
- Trendyol'un kullanım koşullarına uygun kullanılmalıdır
- Rate limiting ve diğer kısıtlamalara dikkat edilmelidir

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📧 İletişim

Sorularınız için bir Issue açabilir veya şu adresten bana ulaşabilirsiniz:
[GitHub Issues](https://github.com/yourusername/trendyol-review-analysis/issues)
# tyyorum2
