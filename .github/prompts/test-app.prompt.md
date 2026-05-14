---
description: "Use when testing the current project after implementation or before review. Loads only the necessary testing context, selects the right test scope, runs or proposes the relevant tests, and reports concise results."
name: "Test App"
argument-hint: "Test the current task, changed files, or a specified workflow"
agent: "agent"
---

# UYGULAMAYI TEST ET

Bu komut tetiklendiğinde mevcut projede yapılan işi doğrulamak için doğru test kapsamını seçmen ve test akışını yürütmen gerekir.

## 1. Minimum Test Bağlamını Yükle
1. Önce `.memory-bank/foundation.md` dosyasından test frameworklerini, ana teknoloji yığınını ve test yaklaşımını belirle.
2. Mevcut görev veya yakın tarihli değişiklikler test kapsamını etkiliyorsa `.memory-bank/state.md` dosyasını oku.
3. Yeni iş kuralı, risk veya davranış değişikliği söz konusuysa `.memory-bank/decisions.md` dosyasını oku.
4. `.memory-bank/codingStandards.md` varsa ve test isimlendirmesi, dosya yapısı veya test tarzı için faydalıysa yardımcı referans olarak kullan.
5. `.github/instructions/` altındaki yalnızca testle ilgili teknoloji kurallarını tara.

## 2. Test Kapsamını Belirle
1. Kullanıcının açıkça verdiği hedefi öncelikli kabul et:
   - belirli bir dosya
   - belirli bir özellik
   - belirli bir hata senaryosu
   - tüm uygulama veya belirli katman
2. Kullanıcı kapsam vermediyse, yakın zamanda değişen dosyalara veya mevcut aktif göreve göre en dar ve anlamlı test kapsamını seç.
3. Kapsamı şu sırayla daralt:
   - ilgili birim testleri
   - ilgili entegrasyon testleri
   - sadece gerekliyse uçtan uca veya daha geniş regresyon testleri
4. Gereksiz yere tüm test paketini çalıştırma; önce en yüksek sinyalli en dar kapsamı seç.

## 3. Eksik Testleri Yaz ve Test Stratejisini Uygula (KRİTİK ADIM)
1. **Kapsam Kontrolü:** Testleri çalıştırmadan ÖNCE, son eklenen veya değiştirilen modülleri (git diff veya son değişiklikler üzerinden) kesinlikle kontrol et.
2. **Eksik Testleri Tamamla:** Eğer projeye yeni bir dosya, fonksiyon veya iş kuralı eklenmiş ancak `tests/` klasöründe buna karşılık gelen bir test dosyası/senaryosu yoksa, testleri doğrudan çalıştırmak YASAKTIR. Önce `@senior-test-engineer` kurallarına uyarak bu eksik testleri **YAZ**.
3. Tüm yeni/değişen kodların güncel testlere sahip olduğundan emin olduktan sonra test komutunu (örn: `python -m pytest -v`) çalıştır.
4. Mümkün olduğunda önce hızlı doğrulama yap (syntax, import, unit), ihtiyaç varsa daha geniş kapsamlı entegrasyon testlerine geç.
5. Dış bağımlılıklar, test ortamı eksikliği veya belirsiz kurulumlar varsa bunu açıkça belirt ve en yakın güvenli alternatifi uygula.
6. Testler başarısız olursa, kısa bir hata analizi yap ve hemen ardından `.github/prompts/fix-test-failures.prompt.md` dosyasındaki direktifleri (promptunu) çağırarak onarım sürecini başlat.

## 4. Sonuç Raporu
Yöneticiye kısa ve net bir rapor ver:
- **Test Kapsamı:** hangi dosya, akış veya modül test edildi
- **Çalıştırılan Testler:** hangi testler veya komutlar kullanıldı
- **Sonuç:** geçti / kaldı / kısmi doğrulandı
- **Bulgu:** varsa hata, risk veya eksik kapsama dair kısa not
- **Sonraki Adım:** gerekliyse önerilen bir sonraki test veya düzeltme

## 5. Çalışma Prensibi
- Bilgi uydurma; test kapsamını mevcut kod, istek ve belgelere dayandır.
- Test mümkün değilse nedenini açıkça söyle, ama güvenli alternatif doğrulamayı atlama.
- Küçük değişikliklerde geniş regresyonu varsayılan yapma.
- Büyük davranış değişikliklerinde sadece happy path ile yetinme; edge-case ve failure path kapsamını düşün.
- Gerekirse test tamamlandıktan sonra `DEĞİŞİKLİKLERİ İŞLE` akışına bırakılacak hafıza etkilerini not et.

## Beklenen Sonuç
Bu prompt çalıştırıldığında ajan doğru test kapsamını seçer, uygun testleri yürütür veya hazırlar ve sonucu kısa, uygulanabilir bir raporla sunar.
