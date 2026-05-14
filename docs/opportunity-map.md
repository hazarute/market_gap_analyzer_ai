# Opportunity Map

## Genel Bakış

Opportunity Map özelliği, pipeline'ın ikinci aşamasıdır. Birinci aşamada üretilen `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` dosyasını girdi olarak alır ve OpenRouter çağrısı ile işleyerek çıktıyı `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` adıyla kaydeder.

Bu aşamanın amacı birinci rapora daha stratejik bir mercekten bakmaktır: rakip analizi değil, somut fırsat haritası. Çıktı üçüncü aşama (Master LLM Prompt Sentezi) için birincil referans kaynaklarından biri olacaktır.

---

## Bileşen

```
opportunity_mapper.py
```

Bu modül aşağıdaki sorumlulukları üstlenir:

- `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` dosyasını doğrudan okuyup `PromptTemplate` ile AI çağrı mesajına ekler.
- `ChatOpenAI` ve `StrOutputParser()` kullanarak OpenRouter üzerinden prompt'u işler.
- Dönen çıktıyı `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` olarak kaydeder.
- Başarılı kayıt sonrasında rapor yolunu konsola yazar ve `database.py` aracılığıyla veritabanına işler.

---

## LangChain Zinciri

```
Path.read_text() (rapor_*.md)
    └─> PromptTemplate (OPPORTUNITY_MAP_PROMPT + belge içeriği)
         └─> ChatOpenAI (OpenRouter uyumlu)
              └─> StrOutputParser()
                   └─> opportunity_map_*.md
```

Kullanılan LangChain bileşenleri:

| Bileşen | Açıklama |
|---------|----------|
| `PromptTemplate` | Sistem talimatı + rapor içeriğini birleştirir |
| `ChatOpenAI` | `base_url` olarak OpenRouter endpoint'ini kullanır |
| `StrOutputParser` | LLM çıktısını düz metin olarak ayrıştırır |

---

## Giriş / Çıkış

| | Format | Konum |
|--|--------|-------|
| **Giriş** | `rapor_<uygulama_adi>.md` | `reports/<uygulama_adi>/` |
| **Çıkış** | `opportunity_map_<uygulama_adi>.md` | `reports/<uygulama_adi>/` |

---

## Opportunity Map Prompt Yapısı

Prompt aşağıdaki bölümleri içermelidir:

```
Rol: Sen kıdemli bir SaaS Growth Stratejisti ve Fırsat Analistisisin.

Bağlam: Aşağıda bir rakip uygulamanın pazar analiz raporu verilmiştir.
Bu raporu okuyarak yalnızca gerçekten boş olan ve yeni bir SaaS ile doldurulabilecek
fırsat alanlarını haritalandır.

Üret:
1. Öncelikli Fırsat Alanları (3-5 madde, kanıta dayalı)
2. Hedef Müşteri Segmenti (en az 2 spesifik segment)
3. Rekabet Kör Noktaları (mevcut oyuncuların görmezden geldiği)
4. Hızlı Kazanım (0-3 ay içinde konumlandırılabilecek fırsat)
5. Orta Vadeli Fırsat (3-12 ay)
6. Uzun Vadeli Stratejik Pozisyon (12+ ay)
7. Risk Faktörleri (bu fırsatı zorlaştırabilecek 2-3 etken)

Rapor:
{rapor_icerigi}
```

> `OPPORTUNITY_MAP_PROMPT` değişkeni `.env` dosyasından okunur. Varsayılan değer yoksa yukarıdaki şablon `config.py` içinde fallback olarak tanımlanır.

---

## Veritabanı Entegrasyonu

`database.py` şeması, `opportunity_map_path` ve `opportunity_map_at` sütunlarını ekleyerek fırsat haritası çıktısının izlenmesini sağlar.

| Sütun | Veri Tipi | Açıklama |
|-------|-----------|----------|
| `opportunity_map_path` | TEXT | `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` dosya yolu |
| `opportunity_map_at` | TIMESTAMP | Harita üretilme tarihi |

Detaylı şema için `docs/database-schema.md` belgesine bakın.

---

## Kabul Kriterleri

**Diyelim ki** geçerli bir `reports/evernote/rapor_evernote.md` dosyası mevcutsa  
**ve** kullanıcı `--opportunity-map` bayrağıyla ya da CLI'dan Opportunity Map adımını tetiklerse  
**Beklenen:**
- `reports/evernote/opportunity_map_evernote.md` dosyası oluşturulur.
- Dosya en az `Öncelikli Fırsat Alanları`, `Hedef Müşteri Segmenti`, `Rekabet Kör Noktaları` bölümlerini içerir.
- Veritabanındaki ilgili kayıtta `opportunity_map_path` ve `opportunity_map_at` alanları dolar.
- Kaynak rapor dosyası değiştirilmez.

**Diyelim ki** kaynak `rapor_*.md` dosyası yoksa  
**Beklenen:**
- İşlem hata mesajıyla durur, yeni dosya oluşturulmaz.

**Diyelim ki** AI yanıt üretemezse (API hatası)  
**Beklenen:**
- Hata loglanır, veritabanı güncellenmez, yarım dosya silinir.

---

## Yeni Oluşturulan Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `opportunity_mapper.py` | LangChain zincirini kuran ve çalıştıran ana modül |
| `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` | Her uygulama için üretilen fırsat haritası |
