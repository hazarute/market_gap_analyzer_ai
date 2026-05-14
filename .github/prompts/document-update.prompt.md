---
description: "Use when documenting a new request, updating existing docs, or deciding whether a new document should be created before release planning."
name: "Document Add/Update"
argument-hint: "Update existing docs or create a new document before release planning"
agent: "documentation-specialist"
---

# DOKÜMAN EKLE/GÜNCELLE

Bu komut, kullanıcı isteğini önce doküman düzeyinde netleştirmek için kullanılır. Amaç, mevcut dokümanlar arasında doğru yeri bulmak, eksikse yeni bir belge açmak ve ardından sürüm planı için sağlam bir bağlam oluşturmaktır.

Bu komut tek bir hedef dosyayı mekanik olarak düzenleme komutu değildir. Kullanıcı talebinin doküman etkisini belirlemek, ilgili belge ailesini taramak, çapraz belge drift riskini tespit etmek ve gerekiyorsa birden fazla belgeyi birlikte güncellemek için kullanılır.

## 1) Girdi
- Kullanıcının talebi veya yeni iş fikri
- Etkilenen alanlar: ürün davranışı, UX, API, backend, veritabanı, güvenlik veya AI akışı
- Varsa mevcut ilgili dokümanlar ve çelişebilecek notlar

## 2) Öncelik Sırası
1. Önce kök `README.md` ve `docs/README.md` üzerinden ilgili belge ailesini belirle.
2. Talebin doğrudan dokunduğu belgeyi belirle; sonra bu belgenin bağlı olduğu kanonik komşu dokümanları da tara.
3. Gerekirse alan bazlı dokümanları oku ve mevcut yapı içinde uygun yer olup olmadığını değerlendir.
4. Mevcut bir belge yeterliyse onu güncelle.
5. Uygun belge yoksa yeni bir doküman oluştur; belgeyi doğru klasöre yerleştir.
6. Eğer talep bir ekran, API, backend servis, veri modeli, güvenlik kuralı veya iş akışını etkiliyorsa, bu değişikliğin başka hangi dokümanlarda kanonik karşılığı olması gerektiğini açıkça kontrol et.
7. Eğer kararın `.memory-bank` etkisi varsa bunu ayrıca işaretle; ancak bu komutun ana görevi hafıza senkronu değil, doküman mimarisidir.

## 2.1) Zorunlu Çapraz Kontrol

Bu komut, kullanıcının adını verdiği tek dosyayla sınırlı yorumlanmamalıdır. Hedef belge güncellenmeden önce veya güncelleme ile birlikte, en az aşağıdaki çapraz kontrol mantığı uygulanır:

- Ekran / UX dokümanı güncelleniyorsa: ilgili frontend belge ailesi ile birlikte API contract, backend surface ve gerekiyorsa auth / security / subscription / payment belgeleri kontrol edilir.
- API contract dokümanı güncelleniyorsa: ilgili backend surface, OpenAPI, frontend tüketici belgeleri ve test / release notları kontrol edilir.
- Backend surface dokümanı güncelleniyorsa: ilgili API contract, veri modeli, operasyon veya frontend tüketici dokümanları kontrol edilir.
- Veri modeli / migration dokümanı güncelleniyorsa: API, backend, test ve operasyon belgeleri kontrol edilir.
- Güvenlik, auth, quota, payment veya AI akışı dokümanı güncelleniyorsa: bu davranışın tüketicisi olan tüm yakın belge aileleri çapraz kontrol edilir.

Amaç tüm `docs/` ağacını körlemesine okumak değil, değişikliğin kanonik etkisini taşıyan belge ailesini eksiksiz belirlemektir.

## 2.2) Tamamlama Karar Kapisi

Aşağıdaki durumlardan biri varsa görev yalnızca tek dosya güncellemesiyle tamamlanmış sayılmaz:

- Hedef doküman, başka bir kanonik belgeyi ilgilendiren eksik API/backend/data/security yüzeyi tespit ediyor ama o belge hiç kontrol edilmemiş.
- Bir dokümanda `şu an API'de yok`, `backend endpoint'i tanımlı değil`, `ayrı contract gerekli` benzeri gap notu varsa, bunun etkilediği kanonik belge ailesi de değerlendirilmeden görev kapatılamaz.
- Kullanıcı talebi `ihtiyaçları karşılaması`, `tamamlanması`, `uyumlu hale gelmesi`, `eksiklerin kapatılması` gibi kapsayıcı bir ifade içeriyorsa yalnızca yerel düzeltme yeterli kabul edilmez.
- Hedef dosyadaki değişiklik, komşu belgelerde drift riski üretiyor veya var olan drift'i sadece not edip bırakıyorsa görev eksik sayılır.

## 3) Çıktılar
- İncelenen dosyaların listesi
- Etkilenecek dosyaların listesi
- Güncellenen veya oluşturulan dosyaların listesi
- Bilinçli olarak güncellenmeyen ama gap / risk taşıyan dosyaların listesi
- Neden o dosyaların seçildiğine dair kısa gerekçe
- Yeni belge gerekiyorsa önerilen dosya yolu ve başlık
- Dokümanda yer alması gereken ana maddeler
- Yeni bir doküman oluştururken veya güncellerken, değişen özellik için mutlaka Given-When-Then (Diyelim ki - Olduğunda - Beklenen) formatında veya net maddeler halinde Kabul Kriterleri ekle; test ajanı bu kriterleri baz alacaktır.
- Sonraki adım olarak hangi sürüm planının çalıştırılması gerektiği (`KÜÇÜK SÜRÜM REVİZYONU` veya `BÜYÜK SÜRÜM PLANI`)
- Eğer sonraki adım `KÜÇÜK SÜRÜM REVİZYONU` ise, chat çıktısının en sonuna kodlama ajanının doğrudan kopyalayıp kullanabileceği, Markdown formatında bir `[Uygulama Özeti Bloğu]` ekle; bu blokta eklenecek/değişecek dosyalar ve fonksiyonların tam listesi hap bilgi olarak yer alsın.

Bu çıktı seti yalnızca zihinsel not olarak tutulmaz; kullanıcıya sonuç raporunda açıkça belirtilir.

## 4) Çalışma Prensibi
- Bu komut, planlama komutlarının önkoşuludur.
- Belge güncellemesi gerekiyorsa doğrudan uygula; yeni belge gerekiyorsa doğru konuma oluştur.
- Sürüm planı burada yapılmaz; sadece plan için gerekli doküman temeli hazırlanır.
- Doküman güncellemesi, işin kapsamını değiştiren yeni kararlar doğuruyorsa bunu açıkça not et.
- Hedef dokümanı mevcut eksikleri anlatarak pasif şekilde güncellemek yeterli olmayabilir; ihtiyaç başka kanonik belgelerde de değişiklik gerektiriyorsa bu değişiklikleri uygula veya neden bloke olduğunu açıkça yaz.
- Değişiklik birden fazla belge ailesini etkiliyorsa önce etki haritasını çıkar, sonra gerekli belgeleri aynı görev içinde birlikte güncelle.
- Kullanıcı tek bir dosya adı verse bile bunu otomatik olarak `yalnızca bu dosyayı değiştir` şeklinde yorumlama; önce bunun yerel mi yoksa çapraz belge etkili mi olduğuna karar ver.
- Yeni belge açmak ile mevcut belgeyi güncellemek arasında karar verirken yalnızca yer bulmayı değil, kanonik ownership ve gelecekteki bulunabilirliği esas al.

## 4.1) Minimum Son Kontrol

Görev kapatılmadan önce şu sorulara net cevap verilmiş olmalıdır:

1. Hangi belge ailesi incelendi?
2. Hangi dosyalar etkilendi?
3. Hangi dosyalar güncellendi veya oluşturuldu?
4. Güncellenmeyen ama halen açık gap taşıyan kanonik dosyalar var mı?
5. Bu iş yalnızca doküman güncellemesiyle kapanıyor mu, yoksa sonraki adımda bir küçük veya büyük sürüm planı mı gerektiriyor?

## 5) Beklenen Sonuç
Bu komut tamamlandığında ilgili bilgiler yalnızca tek bir dosyada değil, gerekiyorsa ilgili belge ailesi boyunca tutarlı hale getirilmiş olmalıdır. Hedef belge güncellenmiş, etkilenen diğer kanonik dokümanlar ya güncellenmiş ya da bilinçli gap olarak raporlanmış olmalıdır. Ardından sürüm kapsamı için `KÜÇÜK SÜRÜM REVİZYONU` veya `BÜYÜK SÜRÜM PLANI` akışı güvenle çalıştırılabilir.