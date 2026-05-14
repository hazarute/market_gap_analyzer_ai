# Master LLM Prompt Sentezi

## Genel Bakış

Master LLM Prompt Sentezi, pipeline'ın üçüncü ve son aşamasıdır. Aynı uygulama için üretilmiş iki referans belgesini — `rapor_<uygulama_adi>.md` (Aşama 1) ve `opportunity_map_<uygulama_adi>.md` (Aşama 2) — birleştirerek, Claude Opus, Gemini Pro ve GPT serisi gibi büyük, ücretli frontier modellerine doğrudan verilmek üzere tasarlanmış kapsamlı ve yapılandırılmış bir prompt belgesi (`master_prompt_<uygulama_adi>.md`) üretir.

Bu belgenin amacı; ham veriyi ve fırsat haritasını tek bir meta-prompt'ta yoğunlaştırarak frontier modelden **hareket planı**, **MVP çerçevesi** veya **yatırımcı özeti** gibi yüksek katma değerli çıktılar elde etmeyi kolaylaştırmaktır.

---

## Bileşen

```
prompt_synthesizer.py
```

Bu modül aşağıdaki sorumlulukları üstlenir:

- `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` ve `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` dosyalarını okur.
- İki belgeyi `SYNTHESIS_PROMPT` şablonuna enjekte eder.
- `ChatOpenAI` ve `StrOutputParser()` kullanarak OpenRouter üzerinden birleşik prompt'u işler.
- Çıktıyı `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md` olarak kaydeder.
- Veritabanındaki ilgili kaydı `master_prompt_path` ve `master_prompt_at` alanlarıyla günceller.

---

## Pipeline Bağlamı

```
Aşama 1: rapor_<uygulama_adi>.md          (Rakip analizi)
Aşama 2: opportunity_map_<uygulama_adi>.md (Fırsat haritası)
Aşama 3: master_prompt_<uygulama_adi>.md  (Frontier LLM için nihai prompt)
```

Aşama 3, Aşama 1 ve Aşama 2'nin her ikisi de tamamlanmış olmadan çalıştırılamaz.

---

## Synthesis Prompt Yapısı

`prompt_synthesizer.py` içinde kullanılan birleştirme talimatı:

```
Rol: Sen bir AI Ürün Stratejisti ve Prompt Mimarısısın.

Görev: Aşağıda iki kaynak belge verilmiştir:
  - [RAPOR]: Bir rakip uygulamanın derinlemesine pazar analizi
  - [FIRSAT HARİTASI]: Bu analizden çıkarılan fırsat alanları

Bu iki belgeyi sentezleyerek, Claude Opus / Gemini Pro / GPT-5 seviyesinde
bir frontier AI modeline verilmek üzere "tek seferde çalışan" kapsamlı bir
master prompt üret.

Master prompt aşağıdaki bölümleri içermelidir:
1. Görev Çerçevesi (frontier modelin ne yapması gerektiği)
2. Bağlam Paketi (pazar özeti, fırsat alanları, rekabet kör noktaları)
3. Kısıtlar ve Varsayımlar (bütçe, timeline, minimum ekip büyüklüğü)
4. İstenen Çıktı Formatı (MVP planı, GTM stratejisi veya yatırımcı sunumu)
5. Kalite Eşiği (kabul edilebilir minimum çıktı standartları)
6. Örnek Giriş / Beklenen Çıktı Formatı

[RAPOR]:
{rapor_icerigi}

[FIRSAT HARİTASI]:
{firsat_haritasi_icerigi}
```

---

## Giriş / Çıkış

| | Format | Konum |
|--|--------|-------|
| **Giriş 1** | `rapor_<uygulama_adi>.md` | `reports/<uygulama_adi>/` |
| **Giriş 2** | `opportunity_map_<uygulama_adi>.md` | `reports/<uygulama_adi>/` |
| **Çıkış** | `master_prompt_<uygulama_adi>.md` | `reports/<uygulama_adi>/` |

---

## Master Prompt Dosyasının İçeriği

Üretilen `master_prompt_*.md` dosyası bir "kullanıma hazır prompt belgesi"dir. İçeriği:

- Frontier modele açıklama gerektirmeden yapıştırılabilecek tam bağlam
- Hangi modele (Claude Opus, Gemini Pro, GPT-5 vb.) verildiğine bağlı olarak önerilmesi gereken parametreler (temperature, max_tokens, system role)
- Opsiyonel: modelden beklenen çıktı türüne göre 2-3 alternatif soru çerçevesi

---

## Veritabanı Entegrasyonu

`database.py` şemasına eklenen yeni sütunlar:

| Sütun | Veri Tipi | Açıklama |
|-------|-----------|----------|
| `master_prompt_path` | TEXT | `master_prompt_*.md` dosya yolu |
| `master_prompt_at` | TIMESTAMP | Sentez tarihi |

Detaylı şema için `docs/database-schema.md` belgesine bakın.

---

## Kabul Kriterleri

**Diyelim ki** `reports/<uygulama_adi>/rapor_*.md` ve `reports/<uygulama_adi>/opportunity_map_*.md` her ikisi de mevcutsa  
**ve** kullanıcı `--master-prompt` bayrağıyla ya da tam pipeline modunda Aşama 3'ü tetiklerse  
**Beklenen:**
- `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md` oluşturulur.
- Dosya en az `Görev Çerçevesi`, `Bağlam Paketi` ve `İstenen Çıktı Formatı` bölümlerini içerir.
- Veritabanındaki ilgili kayıtta `master_prompt_path` ve `master_prompt_at` alanları dolar.
- Kaynak dosyalar (rapor ve fırsat haritası) değiştirilmez.

**Diyelim ki** `opportunity_map_*.md` henüz oluşturulmamışsa  
**Beklenen:**
- Aşama 2 otomatik olarak çalıştırılır veya kullanıcıya açık hata mesajı verilir; Aşama 3 atlanmaz.

**Diyelim ki** AI sentez yanıtı üretemezse (API hatası, token limiti)  
**Beklenen:**
- Hata loglanır, veritabanı güncellenmez, yarım dosya silinir.

**Diyelim ki** kullanıcı çıktıyı Claude Opus 4 veya Gemini 2.5 Pro'ya yapıştırdığında  
**Beklenen:**
- Frontier model ek açıklama istemeksizin görevi anlayabilir.
- Ek bağlam sağlamadan ilk yanıtta MVP planı, GTM stratejisi veya yatırımcı özeti içeren yapılandırılmış çıktı üretir.

---

## Yeni Oluşturulan Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `prompt_synthesizer.py` | İki raporu birleştiren ve master prompt'u üreten modül |
| `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md` | Her uygulama için üretilen nihai frontier LLM prompt belgesi |

---

## Önerilen Frontier Modeller

Bu özelliğin ürettiği `master_prompt_*.md` dosyaları aşağıdaki modeller için optimize edilmiştir:

| Model | Sağlayıcı | Önerilen Kullanım |
|-------|-----------|-------------------|
| Claude Opus 4 / 4.5 | Anthropic | Uzun bağlam, nüanslı strateji, yatırımcı özeti |
| Gemini 2.5 Pro / Ultra | Google | Çok modlu girdi, güçlü akıl yürütme, GTM planı |
| GPT-4o / o3 | OpenAI | Kod entegrasyonlu MVP planı, teknik çerçeve |
| GPT-5 | OpenAI | Geniş bağlam penceresi, derin çıkarım |

> `master_prompt_*.md` dosyası hangi modele verilirse verilsin aynı kalır. Model özelinde küçük ayarlamalar için çıktıdaki "Önerilen Parametreler" bölümü rehberlik eder.
