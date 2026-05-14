# Documentation Index

Bu klasör proje belgelerinin ikincil kaynaklarını içerir. `README.md` ana proje seviyesinde genel bir bakış sunarken, `docs/` altındaki dosyalar belirli konulara ve teknik ayrıntılara odaklanır.

## Belgeler

- `architecture.md` - Projenin bileşenleri, 3 aşamalı veri akışı, sorumluluk sınırları ve genişletilebilirlik stratejileri.
- `configuration.md` - `.env` ve OpenRouter temelli yapılandırma ayarları, önerilen modeller, LangChain değişkenleri ve tüm çevresel değişkenler.
- `database-schema.md` - SQLite tablosu yapısı, alan açıklamaları ve şema genişletme notları.
- `installation.md` - Projeyi klonlama, sanal ortam oluşturma, bağımlılık yükleme ve kurulum doğrulama adımları.
- `usage.md` - CLI çalıştırma örnekleri, parametre açıklamaları, beklenen çıktılar ve hata durumu önerileri.
- `scrapers.md` - Google Play ve App Store veri toplama katmanının işleyişi, giriş/çıkış yapısı ve hata sınırları.
- `security.md` - API anahtarları, gizli veri yönetimi, `.env` kullanımı ve güvenlik önerileri.
- `prompt-guidelines.md` - OpenRouter için prompt tasarımı, model seçimi ve analiz çıktısı kalitesini artırma rehberi.
- `opportunity-map.md` - Aşama 2: LangChain ile fırsat haritası üretimi, zincir yapısı, prompt şablonu ve kabul kriterleri.
- `master-prompt-synthesis.md` - Aşama 3: İki raporu birleştirerek frontier LLM'lere (Claude, Gemini, GPT) hazır master prompt sentezi.

## Nasıl kullanılır

- Ana proje dokümanı olarak önce kök `README.md` okunmalıdır.
- Daha sonra spesifik teknik alanlarla ilgileniliyorsa ilgili `docs/` belgesi açılmalıdır.
- `docs/` içeriği projenin uygulama detaylarını ve bakım rehberini desteklemek için tasarlanmıştır.

## Not

Bu dosya, `.github/prompts/document-update.prompt.md` ve ilgili dökümantasyon ajanları tarafından kullanılan belge ailesi mantığını desteklemek için oluşturulmuştur.
