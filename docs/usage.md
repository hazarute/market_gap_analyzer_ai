# Usage

## OpenRouter ile Çalışma

Projeyi OpenRouter ücretsiz modelleriyle kullanmak için `.env` dosyasında `OPENROUTER_API_KEY` ve `OPENROUTER_MODEL` alanlarını tanımlayın. En güçlü varsayılan model olarak `nvidia/nemotron-3-super:free` önerilir.

## Temel Çalıştırma

```bash
python main.py --keyword "Proje Yönetimi" --store android
```

## Parametreler

- `--keyword`
  - Analiz edilecek arama anahtar kelimesi.
  - Bu anahtar kelime mağazada arama sorgusuna dönüştürülür; hedef, rastgele uygulamalar değil, ilgili alandaki en popüler ve yüksek puanlı uygulamalardır.
  - Örnek: "Finansal Okuryazarlık", "Meditasyon"
- `--store`
  - `android` veya `ios`
  - Hangi mağazadan veri çekileceğini belirler.
- `--all-stages`
  - Tüm aşamaları çalıştırır: analiz, fırsat haritası ve master prompt.
  - `--opportunity-map` ve `--master-prompt` bayraklarının tamamını tek komutta çalıştırmak için kullanılır.

## Örnek Senaryo

```bash
python main.py --keyword "Finansal Okuryazarlık" --store android
```

Bu komut, Play Store'da belirtilen anahtar kelimeyle alakalı uygulamaları tarar, yeni uygulamalar için analiz yapar ve her biri için Markdown raporu üretir.

Aşağıdaki komut ise tüm pipeline aşamalarını çalıştırır:

```bash
python main.py --keyword "Finansal Okuryazarlık" --store android --all-stages
```

Her uygulama için çıktı dosyaları `reports/<uygulama_adi>/` alt klasörüne yazılır.

## Çıktılar

- `reports/<uygulama_adi>/rapor_<uygulama_adi>.md`
  - Her analiz sonucunu ayrı Markdown dosyasına yazar.
  - Raporlar proje kökündeki `reports/<uygulama_adi>/` alt klasörüne kaydedilir.
- `analiz_gecmisi.db`
  - Analiz geçmişini ve rapor dosyası yollarını saklar.

## Hata Durumları

- Eğer aynı `app_id` zaten veritabanında varsa, analiz atlanır.
- Yapay zeka çağrısı başarısız olursa hata mesajı döner; önce OpenRouter API anahtarını ve model adını kontrol edin.

## İpuçları

- `ANALYSIS_PROMPT` içeriğini özelleştirerek analiz çerçevesini değiştirebilirsiniz.
- Uzun ve karmaşık analizler için `nvidia/nemotron-3-super:free` veya `tencent/hy3-preview:free` tercih edin.
- Hız öncelikli görevlerde `qwen/qwen3-coder:free` veya `liquid/lfm-2.5-1.2b-thinking:free` seçebilirsiniz.
- Çok sayıda uygulama analizi yapılıyorsa, veritabanı `analiz_gecmisi.db` dosyasını takip edin.
