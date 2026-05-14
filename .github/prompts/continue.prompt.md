---
description: "Use when continuing work in an existing AI-Driven Development project. Reuses already loaded context when available, reads only the minimum memory needed, aligns with relevant instructions, and resumes execution from the right place."
name: "Continue Work"
argument-hint: "Continue from the current project context or from a specified task"
agent: "agent"
---

# DEVAM ET

Bu komut tetiklendiğinde mevcut AI-Driven Development projesinde kaldığın yerden devam et. Aşağıdaki akışı uygula.

## 1. Minimum Bağlamı Yükle
1. Varsayılan olarak yalnızca `.memory-bank/state.md` dosyasını oku.
2. Kullanıcının isteği, mevcut görev veya dosya bağlamı bunu gerektiriyorsa `.memory-bank/decisions.md` dosyasını oku.
3. Sadece mimari yön, teknoloji yığını veya temel proje amacı gerekli olduğunda `.memory-bank/foundation.md` dosyasını oku.
4. `.memory-bank/codingStandards.md` varsa ve görev gerçekten proje standardı özeti gerektiriyorsa oku; yoksa bunu zorunlu adım yapma.
5. `.github/instructions/` altındaki yalnızca ilgili teknoloji ve görev bazlı kuralları tara.
6. Eğer oturum başında `BELLEĞİ YÜKLE` zaten çalıştırıldıysa, aynı bilgileri gereksiz yere tekrar yükleme.

## 2. Devam Noktasını Belirle
1. Varsayılan olarak `state.md` içindeki `Mevcut Odak` bölümünü ana bağlam kabul et.
2. `Mevcut Odak` ile uyumlu aktif `[ ]` görevi bul.
3. Eğer bu eşleşme net değilse `Aktif Faz` altındaki ilk `[ ]` görevi kullan.
4. Kullanıcı mevcut istekte farklı bir görev, farklı bir dosya ya da farklı bir iş paketi belirtiyorsa bunu öncelikli kabul et.
5. Kullanıcının yönlendirmesi ile `state.md` arasındaki farkı kısa bir notla belirt, ancak işi durdurma.

## 3. Çalışma Stratejisi
1. Devam edilecek göreve ilişkin ilgili kod, dosya veya klasörleri incele.
2. Gerekli `.github/instructions/` kurallarını uygula.
3. Gerekirse uygun özel ajan yaklaşımını kullan:
   - Kod inceleme ise `@senior-code-reviewer` — gereken durumlar aşağıdaki kriterlere göre değerlendirilir.
   - Kod yazımı, yeni özellik uygulama veya küçük refaktörlerde `@senior-code-writer` kullan.
   - Test üretimi veya test genişletme ise `@senior-test-engineer` kullan.
   - Hafıza güncelleme ve bağlam senkronizasyonu ise `@memory-bank-librarian` kullan.

### Eşikler ve Kabul Kriterleri
- Dosya uzunluğu (uyarı eşiği): 300 satır
- Dosya uzunluğu (zorunlu inceleme eşiği): 500 satır
- Fonksiyon/metot uzunluğu (uyarı): 80 satır
- Fonksiyon/metot uzunluğu (zorunlu inceleme): 120 satır
- Sınıf boyutu (uyarı): 200 satır
- Sınıf boyutu (zorunlu inceleme): 300 satır
- Siklomatik karmaşıklık (uyarı): 10
- Siklomatik karmaşıklık (zorunlu inceleme): 20
- Fonksiyon argüman sayısı (uyarı): 5
- Fonksiyon argüman sayısı (zorunlu inceleme): 7

4. Kullanıcının açıkça istemediği sürece uzun plan anlatımıyla oyalanma; uygun olduğunda doğrudan işe başla.

## 4. Kısa Açılış Raporu
Çalışmaya başlamadan hemen önce yöneticiye çok kısa bir başlangıç özeti ver:
- **Mevcut Durum:** `Mevcut Odak`
- **Devam Noktası:** seçilen görev veya kullanıcının belirttiği hedef
- **Yaklaşım:** uygulanacak kısa çalışma yönü

## 5. Çalışma Prensibi
- Bilgi uydurma; bağlamı belgelere ve mevcut isteğe dayandır.
- `state.md` bağlamı ile kullanıcının yeni yönlendirmesi çelişirse kullanıcı yönlendirmesini esas al.
- Her devam akışında önce minimum bağlam yükle, ihtiyaç varsa sonra derinleş.
- Eğer tamamlanan iş tek anlamlı, dar kapsamlı ve `state.md` içindeki belirli bir göreve açıkça karşılık geliyorsa yalnızca minimal bir state güncellemesi yapabilirsin:
   - ilgili `[ ]` görevi `[x]` yap
   - gerekirse `Mevcut Odak` satırını bir sonraki aktif işe kaydır
- İş birden fazla görevi etkiliyorsa, yeni karar ürettiyse, kapsam kayması içeriyorsa veya `decisions.md` güncellemesi gerektiriyorsa tam hafıza senkronunu burada yapma; bunun yerine `DEĞİŞİKLİKLERİ İŞLE` akışına bırak.
- Bu prompt mevcut projede tekrar tekrar kullanılabilir; `BAŞLAT` gibi tek seferlik değildir.

## Beklenen Sonuç
Bu prompt çalıştırıldığında ajan mevcut proje bağlamını yükler, doğru devam noktasını seçer ve işi kaldığı yerden sürdürür.