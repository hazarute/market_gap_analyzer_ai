---
applyTo: "database.py"
---

# Veritabanı Kuralları — Market Gap Analyzer AI

## Teknoloji

- Standart kütüphane `sqlite3` kullanılır; üçüncü taraf ORM (SQLAlchemy vb.) eklenmez.
- Veritabanı dosyası: `analiz_gecmisi.db` (varsayılan); `DATABASE_PATH` `.env` değişkeniyle override edilebilir.

## Tablo Şeması

```sql
CREATE TABLE IF NOT EXISTS analiz_gecmisi (
    app_id      TEXT PRIMARY KEY,
    app_name    TEXT NOT NULL,
    store       TEXT NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_path TEXT
);
```

- `app_id` birincil anahtardır; tekrar ekleme denemesi `INSERT OR IGNORE` ile sessizce geçilir.
- `store` değeri yalnızca `'android'` veya `'ios'` olabilir.

## Zorunlu Fonksiyonlar

```python
def init_db(db_path: str) -> sqlite3.Connection:
    """Veritabanı bağlantısını döndürür; tablo yoksa oluşturur."""

def is_analyzed(conn: sqlite3.Connection, app_id: str) -> bool:
    """app_id daha önce analiz edildiyse True döner."""

def save_analysis(
    conn: sqlite3.Connection,
    app_id: str,
    app_name: str,
    store: str,
    report_path: str,
) -> None:
    """Analiz kaydını veritabanına yazar."""
```

## Güvenlik Kuralları

- Tüm sorgular parametreli (`?`) kullanır; string birleştirme yasaktır.
- Veritabanı bağlantısı `with` bloğunda veya `close()` çağrısıyla kapatılır.
- `analiz_gecmisi.db` dosyası `.gitignore`'a eklenir.

## Bağlantı Yönetimi

- `init_db()` her çalıştırmada bağlantıyı açar ve döndürür; `main.py` bu bağlantıyı pipeline boyunca taşır.
- Bağlantı `main.py` düzeyinde kapatılır; alt fonksiyonlar bağlantıyı kapatmaz.
