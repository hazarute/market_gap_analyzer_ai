---
description: "Use when a specific task block in .memory-bank/state.md is claimed complete and needs deep verification against state, code, tests, and referenced documentation."
name: "Verify Task"
argument-hint: "Which task block from state.md should be verified? (e.g. 14.2 Asset lifecycle schema)"
agent: "task-verifier"
skill: "task-verification"
---

# Görev Kontrol Et

Bu komut tetiklendiğinde, tamamlandığı iddia edilen görev bloğunu `.memory-bank/state.md` içinde tespit edip doğrulamalısın. Görevle ilişkili referans dokümanlar varsa bunları destekleyici kanıt olarak kullan.

## 1. Hedefi Tanımla
1. Verilen görev bloğunu (`14.1`, `14.2` vb.) ve açıklamasını `.memory-bank/state.md` içinde bul.
2. Görevin kendisi ile birlikte eğer varsa referans dokümanlarını (`docs/2.1.0/...` gibi) tespit et.

## 2. Gereksinimleri Çıkar
1. Task bloğundaki her bir maddeden hangi davranışın, schema değişikliğinin, feature flag’in veya testin beklendiğini belirle.
2. Eğer görev doküman referansı içeriyorsa bu referansı destekleyici kanıt olarak kullan.
3. `state.md` maddesi doğrudan yeterli bilgi veriyorsa, doğrulamayı öncelikle bu bilgiye göre yap.

## 3. Kod ve Test Kapsamını Kontrol Et
1. İlgili kaynak kodu ve testleri tara: şema (schema), servisler, task/işleyiciler, entegrasyon bileşenleri, watcher/worker, API ve test dosyaları.
2. Task bloğundaki her gereksinimin kodda bir karşılığı olduğunu doğrula.
3. Karşılık gelen testlerin varlığını ve yeterliliğini kontrol et.

## 4. State ve Memory Bank Senkronu
1. `.memory-bank/state.md` içindeki ilgili görevi `[x]` olarak işaretlemeden önce doğruluğunu onayla.
2. Görev tamam ise önce `state.md` güncellemesini planla; yalnızca gerekli onay ve yetki varsa doğrudan uygula.
3. Görevle ilgili yeni karar, risk veya not çıkarsa `.memory-bank/decisions.md` veya `.memory-bank/foundation.md` için öneri hazırla.

## 5. Çıktı
- Hangi görev bloğunu (örn. `14.2`) kontrol ettiğini ve `state.md` içindeki referans satırını açıkça belirt.
- Her bir doğrulama maddesi için "doğrulandı" veya "eksik" şeklinde rapor ver.
- Eksikse ne eksik olduğunu, hangi dosyada ve mümkünse hangi satır veya kod bloğunda düzeltme gerektiğini belirt.
- `state.md` ve gerekiyorsa `decisions.md` için net öneri ver.
- Gerekirse bu komutu çalıştıran kişiye sonraki adımı öner.
