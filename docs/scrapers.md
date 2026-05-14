# Scrapers

## Genel Bakış

Market Gap Analyzer AI'da scraper katmanı, mobil uygulama mağazalarından sektör bazlı arama sonuçlarını toplar ve analiz pipeline'ına girdi sağlar. Bu katman, doğrudan analiz yapmaz; yalnızca uygulama kimliği, adı, puanı, açıklaması ve yorumlar gibi verileri çeker.

## Modüller

### `scrapers/google_play.py`

- Google Play Store aramalarını yönetir.
- Anahtar kelimeye göre uygulama listesi döndürür.
- Uygulama detaylarını ve gerekiyorsa yorum gibi ek alanları toplar.

### `scrapers/app_store.py`

- Apple App Store aramalarını yönetir.
- Anahtar kelimeye göre uygulama listesi döndürür.
- Uygulama detaylarını ve gerekiyorsa yorum gibi ek alanları toplar.

## Beklenen Girdi

Scraper katmanı temel olarak şu bilgileri kullanır:

- `sektor` veya anahtar kelime
- `store` değeri (`android` ya da `ios`)
- Gerekirse sonuç sayısı ya da filtreleme kriterleri

## Beklenen Çıktı

Scraper fonksiyonları, sonraki aşamaların kullanabileceği yapılandırılmış uygulama verisi üretmelidir. Tipik alanlar:

- `app_id`
- `app_name`
- `store`
- `score`
- `description`
- `url`

Detay toplama aşamasında ek olarak:

- `reviews`
- `rating_count`
- `category`
- `developer`

## İş Akışı

1. Kullanıcı `main.py` üzerinden sektör ve mağaza seçer.
2. İlgili scraper modülü anahtar kelime ile arama yapar.
3. Uygulama listesi elde edilir.
4. Her uygulama için detay verisi gerekiyorsa ek istek yapılır.
5. Veriler `database.py` üzerinden kontrol edilir.
6. Yeni uygulamalar `analyzer.py` katmanına aktarılır.

## Tasarım İlkeleri

- Scraper katmanı yalnızca veri toplama sorumluluğu taşır.
- Analiz, prompt yönetimi ve rapor üretimi bu katmanda yapılmaz.
- Aynı uygulama tekrar taransa bile, veritabanı katmanı tarafından gereksiz analiz engellenir.
- Modüller mağaza bazında ayrıdır; yeni bir mağaza desteği eklemek için yeni bir scraper modülü oluşturulabilir.

## Hata ve Sınırlar

- Mağaza tarafındaki yanıt yapısı değişirse scraper güncellenmelidir.
- Boş sonuçlar durumunda kullanıcıya anlamlı bir geri dönüş verilmelidir.
- Ağ hataları, rate limit ve erişim kısıtları için dayanıklı hata yönetimi gerekir.
- Scraper katmanı, yalnızca açıkça erişilebilir mağaza verileriyle çalışmalıdır.

## Genişletme Notları

- Yeni mağaza desteği eklenecekse `scrapers/` altına yeni bir modül eklenmelidir.
- Arama parametreleri ve çıktı şeması ortak tutulursa `analyzer.py` ve `report_generator.py` ile entegrasyon daha kolay olur.
- Uygulama verisini standart bir sözlük yapısında döndürmek, downstream modüllerin bakımını kolaylaştırır.
