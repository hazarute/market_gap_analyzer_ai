---
name: scaffold-component
description: ".memory-bank/codingStandards.md kurallarına sıkı sıkıya bağlı kalarak yeni modül, bileşen veya servis iskeletleri oluşturan yetenek. Use when: scaffold a new module, component, service, or empty test skeleton while preserving project naming, architecture, and testing conventions."
argument-hint: "Create a standards-compliant scaffold for a new module, component, or service"
user-invocable: true
disable-model-invocation: false
---

# Scaffold Component

## When to Use
- Yeni bir modül, bileşen veya servis iskeleti oluşturulurken
- Mevcut mimariyi bozmadan yeni dosya ağacı başlatmak gerektiğinde
- Gerekli ise birlikte test iskeleti de üretmek gerektiğinde

## Procedure
1. İlk olarak `.memory-bank/codingStandards.md` dosyasını oku ve isimlendirme, dosya yapısı, katman ayrımı, hata yönetimi ve test kurallarını hafızaya al.
2. `.memory-bank/foundation.md` içindeki mimari vizyonla çelişki olup olmadığını doğrula.
3. Üretilecek iskeletin kapsamını netleştir: backend modülü, servis katmanı, frontend bileşeni veya yardımcı altyapı.
4. Kodu ve dosya adlarını projedeki kurallara uygun üret:
   - Python için `snake_case` modül ve fonksiyon adları, `PascalCase` sınıflar.
   - Frontend component dosyalarında proje ekosistemine uygun `PascalCase` kullanımını koru.
   - Endpoint, servis ve model katmanlarını birbirine karıştırma.
5. Import yollarını, hata yönetimini ve yorumları standartlara uygun biçimde yerleştir.
6. Eğer proje kuralları test dosyası gerektiriyorsa, aynı anda boş bir test iskeleti de üret:
   - Backend için `tests/` altında uygun `test_*.py`
   - Frontend için proje konvansiyonuna uygun test/spec dosyası
7. Çıktıyı doğrudan uygulanabilir dosyalar halinde sun; eksik parça bırakma.

## Quality Checks
- Dosya adı ve sembol adı tutarlı mı?
- Katman sınırları korunuyor mu?
- Tenant izolasyonu, güvenlik ve hata yönetimi ihlal edilmiyor mu?
- Yeni iskelet, mevcut `foundation.md` vizyonuna uyuyor mu?
- Gerekli test dosyası eklendi mi?

## Output Expectations
- Oluşturulan dosyaları açıkça listele
- Kısa bir gerekçe ver
- Gerekirse test iskeletlerini ayrıca belirt
