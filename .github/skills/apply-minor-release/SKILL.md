---
name: apply-minor-release
description: "Önceden dokümante edilmiş küçük sürüm değişikliklerini doğrudan koda uygulayan çok adımlı iş akışı. Use when: minor release implementation, documented bug fix rollout, additive endpoint delivery, test update, version.txt bump, or memory-bank sync after a small documented change."
argument-hint: "v0.2.2 -> v0.2.3: uygulanacak değişiklik özeti veya referans dokümanlar"
user-invocable: true
disable-model-invocation: false
---

# Apply Minor Release

## When to Use
- Dokümante edilmiş küçük, geriye dönük uyumlu bir sürüm değişikliğini doğrudan koda uygulamak gerektiğinde
- Yeni bir endpoint, küçük feature, additive schema alanı veya hata düzeltmesi ilgili belgelerde zaten netleştirildiğinde
- Kod, test, `version.txt` ve `.memory-bank/` güncellemelerini tek akışta tamamlamak gerektiğinde
- Kullanıcı planlama değil uygulama, doğrulama ve commit'e hazırlık istediğinde

## Do Not Use
- Değişiklik henüz dokümante edilmemişse
- Kapsam breaking change, büyük mimari revizyon veya discovery gerektiriyorsa
- Hedef sürüm veya referans dokümanlar belirsizse

## Required Inputs
- Mevcut sürüm bilgisi (`version.txt`)
- Hedef sürüm etiketi
- Değişiklik özeti veya ilgili doküman referansları

## Procedure
1. `version.txt`, `.memory-bank/state.md` ve `.memory-bank/decisions.md` dosyalarını oku.
2. Son güncellenen veya kullanıcı tarafından referans verilen ilgili dokümanları tespit et.
3. Dokümanlardan uygulanacak maddeleri çıkar: endpoint, veri modeli, iş kuralı, test beklentisi, versiyon etkisi.
4. Değişiklik yapılacak tüm dosyaların tam listesini kullanıcıya göster.
5. Eğer bir madde dokümante edilmemiş, çelişkili veya eksikse uygulamayı durdur ve önce doküman netleştirmesi iste.
6. Kod değişikliklerini en küçük güvenli dilimler halinde uygula; her değişiklikten sonra gerekçeyi ve etkilediği yüzeyi kısa şekilde özetle.
7. Eklenen veya değişen davranış için gerekli testleri yaz veya güncelle; mümkün olan en dar kapsamlı doğrulamayı çalıştır.
8. `version.txt` dosyasını hedef sürüme güncelle.
9. `.memory-bank/state.md` ve gerekiyorsa `.memory-bank/decisions.md` dosyalarını yeni gerçekle senkronize et.
10. Son çıktıda kod değişiklikleri, testler, bellek güncellemeleri, doğrulama sonucu ve kalan manuel gereksinimleri ayrı başlıklar altında özetle.

## Decision Points
- Doküman eksikse: Uygulamayı durdur, eksik belgeyi belirt, kod yazma.
- Birden fazla belge çelişiyorsa: En kanonik belgeyi seç, çelişkiyi açıkça raporla.
- Yeni bağımlılık gerekiyorsa: Dosyayı güncelle, nedenini belirt, güvenlik ve sürüm etkisini not et.
- Validation başarısızsa: Aynı dar dilimde düzelt ve aynı kontrolü yeniden çalıştır.

## Completion Checks
- İlgili kod yüzeyi dokümandaki değişikliklerle hizalı
- Gerekli testler eklenmiş veya güncellenmiş
- Uygun doğrulama komutu çalıştırılmış
- `version.txt` hedef sürümü gösteriyor
- `.memory-bank/` güncel durumu yansıtıyor
- Çıktı, commit öncesi eksik manuel adımları açıkça listeliyor

## Output Format
- `KÜÇÜK SÜRÜM UYGULANDI: <eski> -> <yeni>` satırı
- Kod değişiklikleri özeti
- Test ve doğrulama özeti
- Bellek güncellemeleri özeti
- Eksik veya manuel gereksinimler