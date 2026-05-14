---
description: "Önceden dokümante edilmiş küçük değişiklikleri doğrudan koda uygula. Öncelik sırası: önce doküman doğrulaması, sonra geriye dönük uyumluluk ve güvenlik, ardından test ve memory bank güncellemeleri; sonucu commit'e hazırla."
name: "KÜÇÜK SÜRÜM REVİZYONU"
argument-hint: "v1.7 -> v1.8: X endpoint eklendi, Y hatası düzeltildi"
---

# KÜÇÜK SÜRÜM REVİZYONU

Bu komut, **zaten netleştirilmiş ve dokümante edilmiş** küçük değişiklikleri (yeni özellik, hata düzeltmesi, ufak iyileştirme) doğrudan koda dökmek için kullanılır. Yeni bir planlama aşaması yürütmez; mevcut dokümantasyonu doğrudan uygulamaya çevirir.

**Ön koşul:** `DOKÜMAN EKLE/GÜNCELLE` komutu tamamlanmış olmalıdır. Bu komut, ilgili dokümanları referans alarak çalışır.

**Kanonik workflow:** Önce `.github/skills/apply-minor-release/SKILL.md` skill'ini yükle ve aşağıdaki adımları bu skill'in karar noktaları ile tamamlama kontrollerini temel alarak uygula.

## 1) Girdi
- Mevcut sürüm (`version.txt` dosyasından okunur).
- Kullanıcının belirttiği hedef sürüm etiketi (ör. `v1.8`).
- Değişikliklerin kısa özeti veya referans gösterilen dokümanlar (genellikle bir önceki `DOKÜMAN EKLE/GÜNCELLE` çıktısı).

## 2) Akış (Uygulama Odaklı)

Aşağıdaki adımları **otomatik olarak, sırayla** gerçekleştir. Her aşamada alt ajanları gerektiği gibi yönlendir.

0. **Skill Yükleme:**
   - `.github/skills/apply-minor-release/SKILL.md` dosyasını yükle.
   - Skill içindeki `Decision Points` ve `Completion Checks` bölümlerini bu çalışmanın kanonik uygulama ve doğrulama çerçevesi olarak kullan.

1. **Bağlam Yükleme:**
   - `version.txt`, `.memory-bank/state.md` ve `.memory-bank/decisions.md` dosyalarını oku.
   - Önceki adımda güncellenmiş dokümanları (genellikle `docs/` altındaki ilgili belgeler) tespit et.

2. **Etki Alanı Tespiti:**
   - Dokümantasyonda eklenen/değiştirilen endpoint, veri modeli, iş kuralı vb. maddeleri çıkart.
   - Bu maddelerin kod karşılıklarını (mevcut dosyalar, oluşturulması gereken yeni dosyalar) belirle.
   - **Değişiklik yapılacak tüm dosyaların tam listesini kullanıcıya göster.**

3. **Kod Uygulaması (Sırayla her bir değişiklik için):**
   - `@senior-code-writer` ajanını çağır. İlgili dosyaları oluştur, güncelle veya gerekiyorsa sil.
   - Her kod değişikliğinden sonra, değişikliğin gerekçesini ve neyi etkilediğini özetle.
   - Yeni bir bağımlılık ekleniyorsa (`pyproject.toml`, `package.json` vb.) bunu da güncelle.

4. **Test Güncellemesi:**
   - `@senior-test-engineer` ajanını çağır.
   - Eklenen/değiştirilen her özellik için gerekli testleri yazdır (happy path, edge case, hata durumları).
   - Mevcut testlerin hala çalıştığından emin ol.

5. **Bellek Bankası Senkronizasyonu:**
   - `@memory-bank-librarian` ajanını çağır.
   - `state.md`: Tamamlanan görevleri `[x]` işaretle, hedef sürüm bilgisini güncelle.
   - `decisions.md`: Varsa yeni mimari karar veya iş kuralı ekle.
   - `version.txt`: Hedef sürümle güncelle.

6. **Özet ve Sonraki Adım:**
   - Yapılan tüm değişikliklerin özetini (etkilenen dosyalar, eklenen testler, bellek güncellemeleri) tablo halinde sun.
   - Eksik kalan veya manuel müdahale gerektiren bir nokta varsa belirt.
   - Commit için `DEĞİŞİKLİKLERİ İŞLE` komutunu hatırlat.

## 3) Çıktı Formatı

✅ KÜÇÜK SÜRÜM UYGULANDI: v1.7 -> v1.8

📄 Kod Değişiklikleri:
- backend/api/suggest.py: suggest endpoint eklendi (+45 satır)
- backend/models/suggestion.py: Suggestion modeli oluşturuldu (+30 satır)
- backend/services/suggest_service.py: SuggestService sınıfı eklendi (+120 satır)
- pyproject.toml: openai bağımlılığı eklendi

🧪 Testler:
- tests/api/test_suggest.py: 3 happy path, 2 edge case, 1 hata durumu
- tests/services/test_suggest_service.py: 5 birim testi

🗂 Bellek Güncellemeleri:
- .memory-bank/state.md: suggest endpoint görevi [x] işaretlendi, yeni görevler eklendi
- .memory-bank/decisions.md: Yapay zeka servisi entegrasyon kararı eklendi
- version.txt: v1.8 olarak güncellendi

⚠️ Eksik / Manuel Gereksinimler:
- .env dosyasına OPENAI_API_KEY eklenmesi gerekiyor (gizli anahtar)

## 4) Kritik Kurallar

- **Geriye dönük uyumluluğu bozma.** API imzalarını, veri modellerini veya yapılandırma anahtarlarını sessizce değiştirme.
- **Her kod değişikliğinden sonra ilgili testi yaz veya güncelle.**
- **Güvenlik kontrolü yap:** hardcoded gizli anahtar, SQL injection, XSS riski taşıyan kod ekleme.
- **Eksik doküman varsa dur ve bildir.** Dokümante edilmemiş bir değişikliği uygulamaya çalışma.
- **Yönetici onayı istenmez.** Bu komut zaten yöneticinin uygulama niyetini temsil eder. Doğrudan uygula.
