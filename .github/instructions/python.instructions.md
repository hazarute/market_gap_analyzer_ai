---
applyTo: "**/*.py"
---

# Python Kuralları — Market Gap Analyzer AI

## Genel Prensipler

- Python 3.10+ söz dizimi kullanılır.
- Her modül tek bir sorumluluğa sahiptir (Single Responsibility Principle).
- Pseudo-code yasaktır; tüm kod çalıştırılabilir, tip güvenlikli ve eksiksiz olmalıdır.
- Type hint'ler tüm yeni fonksiyon imzalarında kullanılır.

## İsimlendirme

- Fonksiyonlar ve değişkenler: `snake_case`
- Sabitler: `UPPER_SNAKE_CASE`
- Sınıflar (gerekirse): `PascalCase`
- Modül/dosya adları: `snake_case.py`

## İmport Düzeni

Standart kütüphane → üçüncü taraf → yerel modüller sırası korunur. Her grup arasında boş satır bırakılır:

```python
import os
import sqlite3

from dotenv import load_dotenv
from openai import OpenAI

from config import settings
```

## Yapılandırma Yönetimi

- `.env` dosyasından değerleri yalnızca `config.py` okur; diğer modüller `config.py`'den import eder.
- Zorunlu değişkenler `config.py`'de doğrulanır; eksik değer `ValueError` fırlatır ve hangi değişkenin eksik olduğunu belirtir.
- API anahtarı, model adı veya prompt asla kaynak kodda sabit olarak yazılmaz.

## Hata Yönetimi

- Ağ isteklerinde (`scrapers/`, `analyzer.py`) `try/except` kullanılır.
- Hata mesajları açıklayıcı ve kullanıcıya yönlendirici olmalıdır.
- İç fonksiyonlarda gereksiz savunmacı kontrol eklenmez; doğrulama yalnızca sistem girişlerinde yapılır.
- Pipeline'da bir uygulama başarısız olursa istisna loglanır ve sonraki uygulamaya geçilir; program çökmez.

## Modül Bağımlılık Kuralı

```
main.py
  ├── scrapers/google_play.py
  ├── scrapers/app_store.py
  ├── database.py
  ├── analyzer.py
  └── report_generator.py
      (hepsi config.py'yi import eder)
```

Alt katmanlar birbirini doğrudan import etmez. Orkestrasyon `main.py` sorumluluğundadır.

## Fonksiyon Sözleşmeleri

- Scraper fonksiyonları `list[dict]` döndürür; her dict standart anahtar setine sahiptir.
- `analyzer.analyze_app(app_data: dict) -> str` — ham AI metnini döndürür.
- `report_generator.generate_report(app_name: str, analysis_result: str) -> str` — kaydedilen dosya yolunu döndürür.
- `database.is_analyzed(app_id: str) -> bool` — daha önce analiz edilmişse `True` döner.

## SQL Güvenliği

- Tüm SQL sorgularında parametreli sorgu (`?` yer tutucu) kullanılır. String birleştirme ile sorgu oluşturmak kesinlikle yasaktır.

```python
# DOĞRU
cursor.execute("SELECT * FROM analiz_gecmisi WHERE app_id = ?", (app_id,))

# YANLIŞ — SQL Injection riski
cursor.execute(f"SELECT * FROM analiz_gecmisi WHERE app_id = '{app_id}'")
```

## Güvenlik Kontrol Listesi (OWASP)

- [ ] Tüm dış girişler (CLI parametreleri) doğrulanır.
- [ ] API anahtarı log çıktısına yazılmaz.
- [ ] Veritabanı sorguları parametrelidir.
- [ ] `requirements.txt` bağımlılıkları güncel tutulur.
