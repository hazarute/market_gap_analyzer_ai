---
description: "Use when syncing completed work back into the project's memory bank after implementation. Analyzes recent changes, updates state and decisions deliberately, and asks for confirmation before finalizing broader memory changes when needed."
name: "Commit Changes"
argument-hint: "Sync recent work into the memory bank and project context"
agent: "memory-bank-librarian"
---

# DEĞİŞİKLİKLERİ İŞLE

Bu komut tetiklendiğinde yakın zamanda yapılan işi projenin hafıza bankasına ve ilgili bağlamsal kayıtlara dikkatli ve kasıtlı şekilde işle. Bu komut, üretim sonrası hafıza senkronu için kanonik akıştır.

## 1. Değişiklikleri Analiz Et
1. Git geçmişini, staged/unstaged değişiklikleri veya yakın zamanda düzenlenen dosyaları incele.
2. Hangi işlerin gerçekten tamamlandığını ve hangilerinin kısmi kaldığını belirle.
3. Gerekirse ilgili kod ve test dosyalarına bakarak değişiklik kapsamını doğrula.

## 2. Hafıza Etkisini Sınıflandır
1. Değişiklik yalnızca dar kapsamlı bir görevin tamamlanmasıysa `state.md` üzerinde minimal güncelleme planla.
2. Yeni iş kuralı, mimari yön, operasyonel karar veya dikkat edilmesi gereken yeni risk oluştuysa `decisions.md` güncellemesini planla.
3. Projenin yüksek seviye amacı, teknoloji yığını veya temel mimari resmi değiştiyse yalnızca bu durumda `foundation.md` güncellemesini değerlendir.
4. `.memory-bank/codingStandards.md` varsa ve gerçek bir standart değişimi olduysa bunu da gözden geçir; sırf küçük kod değişti diye bu dosyayı büyütme.

## 3. İlgili Kuralları Oku
1. `.memory-bank/state.md` dosyasını oku.
2. `.memory-bank/decisions.md` dosyasını oku.
3. Gerekliyse `.memory-bank/foundation.md` dosyasını oku.
4. `.github/instructions/` altındaki ilgili teknoloji kuralları ile çelişki olup olmadığını kontrol et.
5. Yapı dağılmış, eksilmiş veya çelişkili hale geldiyse `.github/memory-blueprint.md` dosyasını onarım rehberi olarak kullan.

## 4. Güncelleme Planı Hazırla
Yöneticiye kısa, net ve bağlamsal bir değişiklik özeti sun:
- Güncellenecek dosyalar
- Her dosyada neden değişiklik gerektiği
- Tamamlandı sayılan görevler
- Varsa yeni karar veya risk kayıtları

## 5. Uygulama Kuralı
1. Değişiklik yalnızca açık ve tartışmasız bir state güncellemesi ise bunu doğrudan uygulayabilirsin.
2. `decisions.md`, `foundation.md` veya daha geniş hafıza değişiklikleri gerekiyorsa önce kısa diff özeti göster ve yönetici onayı iste.
3. Memory bank kayıtlarını gereksiz bilgiyle büyütme; yalnızca kalıcı değeri olan bilgileri yaz.

## 6. Çalışma Prensibi
- Bu komut, `DEVAM ET` sonrasında kapsamlı hafıza senkronu için birincil akıştır.
- Kısmi işleri tamamlanmış gibi işaretleme.
- Geçici uygulama detaylarını mimari karar gibi kaydetme.
- Mevcut gerçeklikle çelişen eski hafıza kayıtlarını fark edersen düzeltmeyi öner.

## 7. Commit & Push Pratiği (Kullanıcı tarafından takip edilecek, talep edilmediyse bu adımı otomatik yapma)
1. Bu adımı uygulamak için proje yönergeleri doğrultusunda `.github/prompts/commit-push.prompt.md` dosyasını kullan.
2. `commit-push.prompt.md` içinde sürüm tespit ve senkronizasyon adımları, `git add/commit/push` ve tag oluşturma örnekleri ayrıntılı olarak yer alır.

## Beklenen Sonuç
Bu komut çalıştırıldığında yakın tarihli işin hafıza etkisi analiz edilir, gerekli state/decision/foundation güncellemeleri planlanır ve uygun yerde uygulanır veya onaya sunulur.