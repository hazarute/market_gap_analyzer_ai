# Prompt Guidelines

## OpenRouter Model Stratejisi

Bu proje için prompt kalitesi kadar model seçimi de önemlidir. OpenRouter üzerindeki ücretsiz modeller arasında stratejik analiz için en güçlü seçenek `nvidia/nemotron-3-super:free`, güçlü alternatif ise `tencent/hy3-preview:free` olarak önerilir.

### Model Seçim Rehberi

- Derin pazar analizi ve uzun yorum toplulukları için `nvidia/nemotron-3-super:free` kullanın.
- Daha hızlı ama hâlâ güçlü analizler için `tencent/hy3-preview:free` deneyin.
- Dengeli performans için `qwen/qwen3-next-80b-a3-instruct:free` veya `openai/gpt-oss-120b:free` seçin.
- Çok dilli veri için `google/gemma-4-31b:free` tercih edin.
- Kısa, hızlı veya maliyet odaklı analizlerde `qwen/qwen3-coder:free` ve `liquid/lfm-2.5-1.2b-thinking:free` yeterli olabilir.

## Amaç

Bu doküman `ANALYSIS_PROMPT` değerinin nasıl yapılandırıldığını ve AI analizinin hangi mantıkla çalıştığını açıklar.

## Temel İlkeler

1. `Rol` verin
   - AI’a "Kıdemli bir Ürün Yöneticisi" rolünü atayın.
2. `Bağlam` sağlayın
   - Analiz edilecek uygulama adı, açıklaması ve puanı gibi bilgileri ekleyin.
3. `Çıktı formatı` belirleyin
   - AI’dan rapor başlıklarını net şekilde isteyin.

## Örnek Ana Prompt

```text
Rol: Sen kıdemli bir Ürün Yöneticisi...
Bağlam ve Hedef: Aşağıda belirteceğim uygulamayı derinlemesine analiz et...
Analiz Edilecek Uygulama: {app_name}, {app_description}, Puan: {score}

Bana şu başlıkları içeren bir rapor sun:
1. Mevcut İdeal Müşteri Kitlesi (ICP)
2. Kritik Kullanıcı Problemleri (Pain Points)
3. Pazardaki Boşluk (Market Gap)
4. Çekirdek ICP Önerisi
5. Yapay Zeka (AI) Çözüm Stratejisi (10x Değer Teklifi ile)
```

## İyi Prompt Örnekleri

- `"Uygulamanın ana kullanıcı kitlesini, kritik sorunlarını ve raporun sonunda 10x değer üreten AI çözümünü açıkla."`
- `"Pazar boşluğunu belirle ve hedef ICP için öne çıkan farklılaştırıcı özellik öner."`

## Kötü Prompt Örnekleri

- `"Bu uygulamayı analiz et."`
- `"Bana genel bilgi ver."`

## Özelleştirme Önerileri

- Hedef anahtar kelime veya coğrafya ekleyin.
- Analizi daha teknik veya daha ürün odaklı hale getirin.
- `prompt` içeriğini `config.py` veya `.env` üzerinden dinamik yapın.
- Model seçimini `OPENROUTER_MODEL` ile ayrı yönetin; prompt ile model kararını birbirine karıştırmayın.
