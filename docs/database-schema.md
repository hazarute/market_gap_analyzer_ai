# Database Schema

## Veritabanı Yapısı

Proje, analiz geçmişini SQLite ile saklar. Varsayılan veritabanı dosyası `analiz_gecmisi.db` olarak kullanılır.

## Tablo: analiz_gecmisi

| Sütun Adı | Veri Tipi | Açıklama |
| --- | --- | --- |
| `app_id` | TEXT | Uygulamanın benzersiz kimliği. Primary key olarak kullanılır. |
| `app_name` | TEXT | Uygulamanın adı. |
| `store` | TEXT | `android` veya `ios`. |
| `analyzed_at` | TIMESTAMP | Analizin yapıldığı tarih/saat. |
| `report_path` | TEXT | Oluşturulan Markdown rapor dosyasının yolu. (
  `reports/<uygulama_adi>/rapor_<uygulama_adi>.md`)
|
| `description` | TEXT | Uygulama açıklaması veya kısa özet. |
| `opportunity_map_path` | TEXT | Oluşturulan fırsat haritası dosyasının yolu. (
  `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md`)
|
| `opportunity_map_at` | TIMESTAMP | Fırsat haritası üretim tarihi.
|
| `master_prompt_path` | TEXT | Oluşturulan master prompt dosyasının yolu. (
  `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md`)
|
| `master_prompt_at` | TIMESTAMP | Master prompt sentezleme tarihi.
|

## Tablo: app_keywords

Bu ilişki tablosu, uygulamaların hangi arama kelimeleriyle taranıp analiz edildiğini eşleştirir. Böylece pazar bazlı kolektif sentez (niche synthesis) yaparken ilgili raporları hızlıca çekebilmemizi sağlar.

| Sütun Adı | Veri Tipi | Açıklama |
| --- | --- | --- |
| `keyword` | TEXT | Arama anahtar kelimesi (örn: "proje yonetimi"). Composite Primary Key alanıdır. |
| `app_id` | TEXT | Uygulamanın benzersiz kimliği. Composite Primary Key alanıdır. |

## İşlev

- Aynı `app_id` tekrar analiz edildiğinde sistem analiz yapmadan atlar.
- Yetersiz yorum veya değerlendirme puanı olan uygulamalar için `report_path` sütunu `"skipped"` değerini alır. Bu sayede bu uygulamalar sonraki çalıştırmalarda tekrar taranıp zaman/API harcamadan atlanır.
- `report_path`, normal durumlarda ilgili rapor dosyasının yerini gösterir.
- `analyzed_at` geçmiş analiz takibi için kullanılır.
- `app_keywords` tablosu, araması yapılan bir anahtar kelimenin daha önce analiz edilmiş olan (veya yeni taranan) tüm rakiplerle eşleştirilmesini ve küresel sentez adımında taranabilmesini koordine eder.

## Genişletme

Bunlara ihtiyaç duyulursa ek alanlar eklenebilir:

- `category` — uygulama kategorisi
- `score` — uygulama puanı
- `source_url` — mağaza sayfası URL’si

## Dikkat

Veritabanı dosyası proje kökünde oluşturulur. Dosya boyutu ve yedekleme gerekirliyse uygun `.gitignore` yapılandırmasına dikkat edin.
