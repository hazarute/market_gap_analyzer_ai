# Usage

## Sağlayıcı Seçimi

Projeyi OpenRouter veya DeepSeek ile kullanabilirsiniz. Varsayılan sağlayıcı OpenRouter'dır. DeepSeek kullanmak için `.env` dosyasında `LLM_PROVIDER=deepseek` ile birlikte `DEEPSEEK_API_KEY` tanımlayın; yeni resmi modeller olarak `deepseek-v4-flash` veya `deepseek-v4-pro` kullanın. Düşünme modu için `DEEPSEEK_THINKING_ENABLED=true` ve gerekirse `DEEPSEEK_REASONING_EFFORT=max` ayarlarını ekleyin.

OpenRouter tarafında `OPENROUTER_API_KEY` ve `OPENROUTER_MODEL` alanları yeterlidir. En güçlü varsayılan model olarak `nvidia/nemotron-3-super:free` önerilir.

## Temel Çalıştırma

```bash
python main.py --keyword "Proje Yönetimi" --store android ios
```

## Parametreler

- `--keyword`
  - Analiz edilecek arama anahtar kelimesi.
  - Bu anahtar kelime mağazada arama sorgusuna dönüştürülür; hedef, rastgele uygulamalar değil, ilgili alandaki en popüler ve yüksek puanlı uygulamalardır.
  - Örnek: "Finansal Okuryazarlık", "Meditasyon"
- `--store`
  - `android` ve/veya `ios`
  - Bir veya daha fazla mağazadan veri çekmeyi sağlar.
- `--limit`
  - Arama sonuçlarından tek seferinde analiz edilecek maksimum uygulama sayısı (varsayılan: 10).
  - Program her çalışmada tam olarak bu kadar **yeni** (daha önce analiz edilmemiş) uygulama bulmaya çalışır. Bulunan uygulamalar veritabanında zaten varsa otomatik olarak sonraki batch'e geçer.
  - Örneğin `--limit 10` ile ikinci kez aynı anahtar kelimeyle çalıştırdığınızda, ilk 10 uygulama atlanır ve 11–20 arasındaki uygulamalar analiz edilir.
- `--all-stages`
  - Tüm aşamaları çalıştırır: analiz, fırsat haritası ve master prompt.
  - `--opportunity-map` ve `--master-prompt` bayraklarının tamamını tek komutta çalıştırmak için kullanılır.

## Örnek Senaryo

```bash
python main.py --keyword "Finansal Okuryazarlık" --store android ios
```

Bu komut, Play Store'da belirtilen anahtar kelimeyle alakalı uygulamaları tarar, yeni uygulamalar için analiz yapar ve her biri için Markdown raporu üretir.

Aşağıdaki komut ise tüm pipeline aşamalarını çalıştırır:

```bash
python main.py --keyword "Finansal Okuryazarlık" --store android ios --all-stages
```

İkinci çalıştırmada aynı anahtar kelimeyle tekrar çalıştırdığınızda:

```bash
python main.py --keyword "Finansal Okuryazarlık" --store android ios
```

Program veritabanını kontrol eder; önceki 10 uygulama zaten kayıtlıysa otomatik olarak 11–20 arasındaki uygulamaları analiz eder. **Herhangi bir ek parametre girmenize gerek yoktur.**

"spor" aramasından 6 uygulamanız DB'deyken "antrenman" araması yaparsanız: program ilk 10 uygulamadan 6'sını veritabanında bulur, atlar ve toplamda 10 yeni uygulama analiz edilene kadar otomatik olarak sonraki batch'lere geçer.

Her uygulama için çıktı dosyaları `reports/<uygulama_adi>/` alt klasörüne yazılır.

## Çıktılar

- `reports/<uygulama_adi>/rapor_<uygulama_adi>.md`
  - Her analiz sonucunu ayrı Markdown dosyasına yazar.
  - Raporlar proje kökündeki `reports/<uygulama_adi>/` alt klasörüne kaydedilir.
- `analiz_gecmisi.db`
  - Analiz geçmişini ve rapor dosyası yollarını saklar.

## Hata Durumları

- Eğer aynı `app_id` zaten veritabanında varsa, analiz atlanır.
- Yapay zeka çağrısı başarısız olursa hata mesajı döner; önce seçili sağlayıcının API anahtarını ve model adını kontrol edin.

## İpuçları

- `ANALYSIS_PROMPT` içeriğini özelleştirerek analiz çerçevesini değiştirebilirsiniz.
- Uzun ve karmaşık analizler için OpenRouter tarafında `nvidia/nemotron-3-super:free` veya `tencent/hy3-preview:free`, DeepSeek tarafında `deepseek-v4-pro` tercih edin.
- Hız öncelikli görevlerde `qwen/qwen3-coder:free` veya `liquid/lfm-2.5-1.2b-thinking:free` seçebilirsiniz.
- Çok sayıda uygulama analizi yapılıyorsa, veritabanı `analiz_gecmisi.db` dosyasını takip edin.
