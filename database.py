import sqlite3
from datetime import datetime, timezone


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS analiz_gecmisi (
    app_id                TEXT PRIMARY KEY,
    app_name              TEXT NOT NULL,
    store                 TEXT NOT NULL,
    analyzed_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_path           TEXT,
    description           TEXT,
    opportunity_map_path  TEXT,
    opportunity_map_at    TIMESTAMP,
    master_prompt_path    TEXT,
    master_prompt_at      TIMESTAMP
);
"""

_MIGRATIONS = [
    ("description",          "ALTER TABLE analiz_gecmisi ADD COLUMN description TEXT"),
    ("opportunity_map_path", "ALTER TABLE analiz_gecmisi ADD COLUMN opportunity_map_path TEXT"),
    ("opportunity_map_at",   "ALTER TABLE analiz_gecmisi ADD COLUMN opportunity_map_at TIMESTAMP"),
    ("master_prompt_path",   "ALTER TABLE analiz_gecmisi ADD COLUMN master_prompt_path TEXT"),
    ("master_prompt_at",     "ALTER TABLE analiz_gecmisi ADD COLUMN master_prompt_at TIMESTAMP"),
]


def init_db(db_path: str) -> sqlite3.Connection:
    """Veritabanı bağlantısını açar; tablo yoksa oluşturur.

    Args:
        db_path: SQLite dosya yolu (örn: 'analiz_gecmisi.db').

    Returns:
        Açık sqlite3.Connection nesnesi.
    """
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_TABLE_SQL)
    # Yeni ilişki tablosunu oluştur
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS app_keywords (
            keyword TEXT,
            app_id  TEXT,
            PRIMARY KEY (keyword, app_id)
        );
        """
    )
    conn.commit()

    cursor = conn.execute("PRAGMA table_info(analiz_gecmisi)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    for column_name, migration_sql in _MIGRATIONS:
        if column_name not in existing_columns:
            conn.execute(migration_sql)
            conn.commit()

    return conn


def is_analyzed(conn: sqlite3.Connection, app_id: str) -> bool:
    """app_id daha önce analiz edildiyse True döner.

    Args:
        conn: Açık veritabanı bağlantısı.
        app_id: Uygulamanın benzersiz kimliği.

    Returns:
        True — daha önce analiz edilmiş, False — yeni uygulama.
    """
    cursor = conn.execute(
        "SELECT 1 FROM analiz_gecmisi WHERE app_id = ?",
        (app_id,),
    )
    return cursor.fetchone() is not None


def get_analyzed_app_names(conn: sqlite3.Connection) -> set[str]:
    """Daha önce analiz edilmiş tüm uygulama adlarını döndürür.

    Args:
        conn: Açık veritabanı bağlantısı.

    Returns:
        Normalize edilmemiş ham app_name değerlerinden oluşan set.
    """
    cursor = conn.execute("SELECT app_name FROM analiz_gecmisi")
    return {row[0] for row in cursor.fetchall()}


def save_analysis(
    conn: sqlite3.Connection,
    app_id: str,
    app_name: str,
    store: str,
    report_path: str,
    description: str | None = None,
) -> None:
    """Analiz kaydını veritabanına yazar.

    Aynı app_id zaten varsa sessizce görmezden gelir (INSERT OR IGNORE).

    Args:
        conn: Açık veritabanı bağlantısı.
        app_id: Uygulamanın benzersiz kimliği.
        app_name: Uygulamanın adı.
        store: 'android' veya 'ios'.
        report_path: Oluşturulan .md rapor dosyasının yolu.
        description: Uygulama açıklaması (Türkçeye çevrilmiş olabilir).
    """
    conn.execute(
        """
        INSERT OR IGNORE INTO analiz_gecmisi
            (app_id, app_name, store, analyzed_at, report_path, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            app_id,
            app_name,
            store,
            datetime.now(timezone.utc).isoformat(),
            report_path,
            description,
        ),
    )
    conn.commit()


def save_opportunity_map(
    conn: sqlite3.Connection,
    app_id: str,
    opportunity_map_path: str,
) -> None:
    """Mevcut analiz kaydına fırsat haritası yolunu ekler.

    Args:
        conn: Açık veritabanı bağlantısı.
        app_id: Uygulamanın benzersiz kimliği.
        opportunity_map_path: Oluşturulan opportunity_map_*.md dosyasının yolu.
    """
    conn.execute(
        """
        UPDATE analiz_gecmisi
        SET opportunity_map_path = ?, opportunity_map_at = ?
        WHERE app_id = ?
        """,
        (
            opportunity_map_path,
            datetime.now(timezone.utc).isoformat(),
            app_id,
        ),
    )
    conn.commit()


def save_master_prompt(
    conn: sqlite3.Connection,
    app_id: str,
    master_prompt_path: str,
) -> None:
    """Mevcut analiz kaydına master prompt yolunu ekler.

    Args:
        conn: Açık veritabanı bağlantısı.
        app_id: Uygulamanın benzersiz kimliği.
        master_prompt_path: Oluşturulan master_prompt_*.md dosyasının yolu.
    """
    conn.execute(
        """
        UPDATE analiz_gecmisi
        SET master_prompt_path = ?, master_prompt_at = ?
        WHERE app_id = ?
        """,
        (
            master_prompt_path,
            datetime.now(timezone.utc).isoformat(),
            app_id,
        ),
    )
    conn.commit()


def save_keyword_association(conn: sqlite3.Connection, keyword: str, app_id: str) -> None:
    """Uygulama ile arama anahtar kelimesi arasındaki ilişkiyi veritabanına kaydeder."""
    conn.execute(
        "INSERT OR IGNORE INTO app_keywords (keyword, app_id) VALUES (?, ?)",
        (keyword.strip().lower(), app_id),
    )
    conn.commit()


def get_reports_for_keyword(conn: sqlite3.Connection, keyword: str) -> list[dict]:
    """Belirli bir arama anahtar kelimesine ait analiz ve fırsat raporlarını döndürür."""
    cursor = conn.execute(
        """
        SELECT ag.app_name, ag.report_path, ag.opportunity_map_path
        FROM analiz_gecmisi ag
        JOIN app_keywords ak ON ag.app_id = ak.app_id
        WHERE ak.keyword = ? AND ag.report_path IS NOT NULL AND ag.report_path != 'skipped'
        """,
        (keyword.strip().lower(),),
    )
    return [
        {
            "app_name": row[0],
            "report_path": row[1],
            "opportunity_map_path": row[2],
        }
        for row in cursor.fetchall()
    ]

