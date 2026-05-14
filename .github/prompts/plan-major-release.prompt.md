---
description: "Plan and coordinate a major release (breaking changes, new modules, migration plan). Produce scope, risks, decision log entries, and a concrete rollout checklist."
name: "Plan Major Release"
argument-hint: "Create a vetted plan for a major version upgrade (e.g., v1.x -> v2.0)"
agent: "senior-architect"
---

# PLAN MAJOR RELEASE

Bu prompt büyük, köklü sürüm yükseltmeleri ve yeni modül/özellik eklemeleri için kullanılır. Amaç: kapsam, risk, migrasyon adımları, test matrisi ve karar kayıtlarını üretip yöneticinin onayına sunmaktır.

## 1) Girdi
- `version.txt` içeriğini okuyarak mevcut sürümü belirle ve hedef sürümü buna göre seç.
- Hedef sürüm etiketi ve kısa açıklama (ör. `v2.0` için neden yükseltme yapıldığı).
- Etkilenen bileşenler listesi (örn. API, DB, frontend, servisler).
- Plan başlamadan önce ilgili ürün/doküman kapsamının `DOKÜMAN Ekle/Güncelle` komutuyla güncel olduğundan emin ol; eksik veya çelişkili bilgi varsa önce o akış çalıştırılmalıdır.

## 2) Çıktılar
- Kapsam ve başarı kriterleri
- Riskler ve rollback stratejileri
- Etkilenecek dosyaların açık listesi (kod, konfigürasyon, servisler, `.memory-bank`, `.github/instructions`)
- Etkilenen alanların ve önerilen değişikliklerin kısa diff özetleri
- Önerilen `.memory-bank` değişiklikleri için taslak notlar (`decisions.md`, `state.md`)
- Önerilen bir inceleme dokümanı: `docs/<hedef-sürüm>/<hedef-sürüm>.md` şeklinde oluşturulacak sürüm notu
- Adım adım rollout kontrol listesi (migrationlar, veri doğrulama, feature flagler, vb.)
- Onaylanacak difflar ve PR önerileri

## 3) Akış
1. Önce `DOKÜMAN Ekle/Güncelle` akışının tamamlandığını veya gerekli dokümanların güncel olduğunu doğrula.
2. Hedef ve kapsamı doğrula.
3. Etkilenecek dosyaları ve alanları listele.
4. Breaking change maddelerini `decisions.md` için taslakla (neden, alternatifler, geri alma planı).
5. Migrasyon adımları ve veri doğrulama planını hazırla.
6. Test planı ve başarılı/kabul kriterlerini belirt.
7. Rollout checklist ve rollback adımlarını yaz.
8. `docs/<hedef-sürüm>/<hedef-sürüm>.md` altında yöneticinin incelemesi için bir sürüm notu dosyası oluştur.
9. Oluşan değişikliklerin kısa diff özetini oluştur ve yönetici onayı iste.

## 4) Onay & Sonraki Adımlar
- Yöneticiye plan sunulur; onay vermesi ya da geri bildirimde bulunması istenir.
- Onaylanmadan `.memory-bank` dosyalarına doğrudan yazma.
- Yöneticinin incelemesi için `docs/<hedef-sürüm>/<hedef-sürüm>.md` sürüm notu dosyasını oluştur ve onay paketine dahil et.
- Onaydan sonra `.github/skills/plan-major-release/SKILL.md` tarafından `memory-sync` akışı tetiklenir; `.memory-bank` ve varsa `.github/instructions/` güncellemeleri onaylı şekilde planlanır ve uygulanır.

## 5) Beklenen Davranış
Bu prompt tek bir tutarlı plan üretmelidir; büyük değişiklikleri doğrudan uygulamamalı — önce diff özetini gösterip insan onayı almalıdır.
