# Security

## API Anahtarları

- `OPENROUTER_API_KEY` gibi gizli anahtarlar asla kaynak kodda saklanmamalıdır.
- Anahtarlar `.env` dosyasında tutulmalı ve `.gitignore` içinde korunmalıdır.

## Model Erişimi

- Free modeller OpenRouter tarafında erişim politikalarına bağlı olabilir.
- Model adını paylaşımlı dokümanlarda sabit bir secret gibi ele almayın; yalnızca izin verilen projelerde kullanın.
- Hassas kullanım durumlarında model çıktısını doğrulayın ve kritik kararları insan onayından geçirin.

## `.env` Dosyası

- `.env` dosyası yalnızca yerel geliştirme ortamı için kullanılmalıdır.
- Üretim ortamında gizli bilgiler için daha güvenli secret yönetimi kullanın.

## Hassas Veri Yönetimi

- Analiz edilen uygulama verisi, genel olarak kamuya açık mağaza bilgisine dayanır.
- Ancak dökümante edilen raporlar, kullanıcıya özel ya da gizli bilgiler içermemelidir.

## Dosya Yedekleme

- `analiz_gecmisi.db` veritabanı dosyası hassas olabilir.
- Yedeklerinizde API anahtarı veya kullanıcı kimlik bilgileri içermediğinden emin olun.

## Güvenlik İpuçları

- `requirements.txt` içindeki bağımlılıkları düzenli olarak güncelleyin.
- Oluşturulan raporları paylaşmadan önce içerik doğrulaması yapın.
- Eğer dış hizmetlere istek gönderiliyorsa, bağlantı güvenliğini (`HTTPS`) kontrol edin.
