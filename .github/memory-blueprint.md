---
title: "Memory Blueprint"
description: "Canonical guide for bootstrapping .memory-bank files during the BAŞLAT flow. Defines the minimum memory-bank file set, required sections, and how GitHub Copilot should derive content from README and project manifests."
---

# Geliştirici Bellek Bankası İnşa Kılavuzu (Memory Blueprint)

**⚠️ DİKKAT (COPILOT İÇİN SİSTEM TALİMATI):**
Bu dosya `BAŞLAT` komutu verildiğinde, projenin `.memory-bank/` klasörünü ve ilişkili `.github/` özelleştirme yapısını ilk kez kurmak için okunmalıdır. Ayrıca proje ilerledikçe hafıza bankası veya `.github/` yapısı bozulur, eksilir ya da anlamını kaybederse; bu rehber yeniden hizalama, onarım ve yeniden inşa için de kanonik referans olarak kullanılmalıdır. Bu rehberi kullanarak bellek bankasının asgari dosya setini `README.md`, bağımlılık dosyaları ve mevcut klasör yapısı ile uyumlu biçimde oluştur veya onar. Dosyaları oluşturduktan sonra kullanıcıya gerçek dosyaları göster ve inceleme/onay iste.

## Temel İlkeler
- `README.md` birincil kaynaktır; proje amacı, ürün vizyonu ve yüksek seviye mimari önce buradan türetilir.
- Kök `README.md` projenin kalbi kabul edilir; bootstrap sırasında önce bu dosya okunur, ardından `docs/` klasöründeki belgeler adım adım incelenir ve hafıza bankası bu sıralamaya göre oluşturulur.
- `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `composer.json`, `Dockerfile`, CI dosyaları ve klasör yapısı yalnızca README bulgularını doğrulamak, detaylandırmak veya eksikleri tamamlamak için kullanılır.
- `docs/` klasörü, README'den sonra gelen ikinci ana doğrulama katmanıdır; indeks dosyaları önce, detay belgeleri sonra okunur.
- README ile diğer kaynaklar çelişirse README önceliklidir; ancak çelişki kullanıcıya açıkça not edilir.
- İçerik uydurulmaz. Yeterli sinyal yoksa minimum güvenli iskelet oluşturulur ve eksik alanlar "doğrulanacak" olarak işaretlenir.
- Var olan `.memory-bank/` dosyaları körlemesine ezilmez; mevcut içerik okunur, gerekiyorsa güncelleme önerilir.
- Copilot standardında birincil operasyonel kurallar `.github/instructions/` altında yaşar.
- `.memory-bank/codingStandards.md` varsa yardımcı ve denetlenebilir proje standardı özeti olarak kullanılır; yoksa teknolojiye özel instruction dosyaları ana kaynak kabul edilir.
- Bu rehber, proje özelinde kullanılmakla birlikte başka projelere de taşınabilecek sade ve tekrar kullanılabilir bir şablon olmalıdır.

## Oluşturulacak Asgari Dosyalar
`BAŞLAT` akışında aşağıdaki çekirdek dosyalar hedeflenir:

1. `.memory-bank/foundation.md`
2. `.memory-bank/state.md`
3. `.memory-bank/decisions.md`

Bu üç dosya, AI-Driven Development akışının zorunlu çekirdeği kabul edilir.

## Önerilen Yardımcı Dosya
İhtiyaca göre aşağıdaki yardımcı dosya da üretilebilir:

1. `.memory-bank/codingStandards.md`

Bu dosya zorunlu değildir. Şu durumlarda önerilir:
- Projede birden fazla teknoloji veya katman varsa
- Takımın tek dosyada okunabilir bir standart özeti ihtiyacı varsa
- Review, scaffold veya test ajanlarının tek bir proje standardı özetine referans vermesi isteniyorsa

Küçük veya açık seçik projelerde bu bilgi tamamen `.github/instructions/` içine dağıtılabilir.

---

## DOSYA 1: `foundation.md`
**Amacı:** Projenin ne olduğunu, hangi teknoloji yığınıyla kurulduğunu ve sistemin yüksek seviye mimarisini tanımlar.

**Nasıl Doldurulacak:**
- Önce `README.md` analiz edilir.
- Ardından bağımlılık dosyaları ve klasör yapısıyla teknik doğrulama yapılır.
- Önce `README.md` analiz edilir.
- Ardından `docs/` klasöründeki belgeler adım adım okunur: önce indeks ve giriş dosyaları, sonra detay belgeleri.
- Ürün dili ile teknik dil gerekiyorsa ayrı ayrı not edilir.

**Zorunlu Bölümler:**
- `# Foundation`
- `## Proje Ozeti`
- `## Teknoloji Yigini`
- `## Sistem Mimarisi`
- `## Klasor Yapisi`
- `## Urun ve Mimari Odaklar`

**İçerik Kuralları:**
- Ürün vizyonu tek ve net bir paragrafla açıklanır.
- Teknoloji yığını kategori bazlı listelenir: frontend, backend, veritabanı, test, operasyon.
- Sürüm bilgisi kesin olarak biliniyorsa eklenir; bilinmiyorsa spekülasyon yapılmaz.
- Klasör yapısı yalnızca gerçekten mevcut veya açıkça hedeflenen klasörleri içerir.

---

## DOSYA 2: `codingStandards.md` (Opsiyonel ama Önerilen)
**Amacı:** Projede üretilecek kodun isimlendirme, dosya yapısı, mimari katman, test ve hata yönetimi açısından tutarlı kalmasını sağlar.

**Nasıl Doldurulacak:**
- Teknoloji yığınına göre dil ve framework bazlı en uygun best practice'ler seçilir.
- Standartlar soyut ve faydasız değil, uygulanabilir ve denetlenebilir olmalıdır.
- `agents/` ve `skills/` tarafından referans alınabilecek kadar açık yazılmalıdır.
- Bu dosya, `.github/instructions/` altındaki kuralların yerine geçmez; onları özetleyen ve proje bağlamında bir araya getiren yardımcı kaynaktır.

**Zorunlu Bölümler:**
- `# Coding Standards`
- `## Isimlendirme Kurallari`
- `## Dosya ve Klasor Kurallari`
- `## Mimari Kurallar`
- `## Hata Yonetimi`
- `## Test Yaklasimi`
- `## Teknolojiye Ozel Notlar`

**İçerik Kuralları:**
- İsimlendirme kuralları dil bazında açık olmalıdır: `camelCase`, `snake_case`, `PascalCase`, `kebab-case`.
- API katmanı, servis katmanı, veri erişim katmanı ve UI katmanı ayrımları net belirtilmelidir.
- Hata yönetiminde beklenen yaklaşım teknolojiye uygun örüntülerle tanımlanmalıdır.
- Tip güvenliği varsa belirtilir; yoksa zorla uydurulmaz.

**Ne zaman atlanabilir:**
- Proje çok küçükse
- Teknoloji kuralları tamamen `.github/instructions/` altında net biçimde ayrıştırılmışsa
- Tekrar üretilecek içerik düşük değer sağlıyorsa

---

## DOSYA 3: `state.md`
**Amacı:** O anki zihinsel odağı, aktif fazı ve yapılacak işleri yaşayan bir görev listesi olarak takip eder.

**Nasıl Doldurulacak:**
- Proje başlangıcında ilk fazlar ve ilk yapılacaklar `README.md` kapsamına göre türetilir.
- `Mevcut Odak` bolumu yalnizca en yakin aktif isi ve bir sonraki adimi anlatir; tamamlananlar burada uzun backlog olarak biriktirilmez.
- `Aktif Faz` bolumunde fazlar tek satirlik checklist formatinda (`[x]`, `[ ]`) listelenir; aktif faz acikca `AKTIF`, bekleyen fazlar gerekiyorsa `BEKLEMEDE` etiketi alir.
- `Gorev Listesi` bolumu mutlaka aktif faz odaqli yazilir; uzak gelecek detaylari ayni fazin icine dagitilmaz.
- Her aktif faz icin sirayla: `Referans dokumanlar`, `Faz amaci`, `Faz cikis kriterleri`, `Numarali gorev bloklari` yazilir.
- Numarali gorev bloklarinda ust gorevler (`#### 1. ...`) ve alt checklist maddeleri birlikte kullanilir; gerekirse altinda `Ref:` satiri ile kisa baglam verilir.
- Aktif faz disina tasinan maddeler `Faz X ve sonrasina tasinanlar` benzeri ayri bir alt baslikta toplanir.
- `Durum Notlari` bolumu operasyonel gercekligi, kapsam sinirlarini ve kapanan bosluklari maddeler halinde canli tutar.

**Zorunlu Bölümler:**
- `# State`
- `## Mevcut Odak`
- `## Aktif Faz`
- `## Gorev Listesi`
- `### <Aktif Faz Adi>`
- `Referans dokumanlar:` (madde listesi)
- `#### <Faz> amaci`
- `#### <Faz> cikis kriterleri`
- `#### 1. ...`, `#### 2. ...` seklinde numarali gorev bloklari
- `### Faz X ve sonrasina tasinanlar` (gerektiginde)
- `## Durum Notlari`

**İçerik Kuralları:**
- Görevler markdown checkbox formatında yazılır: `[ ]`, `[x]`.
- Fazlar mantikli is paketlerine ayrilir; her fazin amaci ve cikis kriteri yazilmadan alt gorevlere gecilmez.
- Gorev metinleri uygulanabilir fiillerle yazilir (`olustur`, `uygula`, `dogrula`, `hizala`) ve belirsiz ifade kullanilmaz.
- Her gorev blogunda mümkün oldugunca ilgili dokuman referanslari belirtilir.
- Cok uzak gelecek backlog maddeleri aktif odakla karistirilmaz; gerekiyorsa `Faz X ve sonrasina tasinanlar` altina alinir.
- Ilk bos kutu normalde siradaki oncelikli isi temsil eder ve `Mevcut Odak` ile celismez.
- `Durum Notlari` yalnizca kalici degeri olan durum bilgisini tutar; gecerli olmayan notlar duzenli temizlenir.

**Onerilen Gorev Iskeleti (Sablon):**

```markdown
# State

## Mevcut Odak

<aktif isin 1-2 paragraflik ozeti ve bir sonraki adim>

## Aktif Faz

- Faz 0 - ... : [x]
- Faz 1 - ... : [ ] AKTIF
- Faz 2 - ... : [ ]

## Gorev Listesi

### Faz 1 - <faz adi>

Referans dokumanlar:
- `../docs/...`
- `../docs/...`

#### Faz 1 amaci
- ...

#### Faz 1 cikis kriterleri
- ...

#### 1. <is paketi>
Ref: `../docs/...`
- [ ] ...
	- [ ] ...
	- [ ] ...

#### 2. <is paketi>
- [ ] ...

### Faz 2 ve sonrasina tasinanlar
- ...

## Durum Notlari
- ...
```

---

## DOSYA 4: `decisions.md`
**Amacı:** Kritik mimari kararları, değişmez iş kurallarını ve geçici çözümleri kayıt altında tutar.

**Nasıl Doldurulacak:**
- Başlangıçta README'den çıkarılabilen temel kurallar yazılır.
- Karar net değilse boş bırakmak yerine "henüz netleşmedi" yaklaşımıyla minimal kayıt düşülebilir.
- Zamanla `DEĞİŞİKLİKLERİ İŞLE` ve `memory-sync` akışlarıyla genişletilir.

**Zorunlu Bölümler:**
- `# Decisions`
- `## Is Kurallari`
- `## Mimari Kararlar (ADR)`
- `## Gecici Cozumler ve Operasyonel Notlar`
- `## Mevcut Risk Kaydi`

**İçerik Kuralları:**
- İş kuralları değişmez ürün gerçeklerini taşımalıdır.
- Mimari kararlar, "neden bu yol seçildi" sorusuna cevap vermelidir.
- Geçici çözümler kalıcı çözüm gibi sunulmamalıdır.
- Risk kaydı canlı tutulabilecek kadar kısa ve net olmalıdır.

---

## Teknolojiye Özel Instruction Üretimi
`BAŞLAT` akışı, `.memory-bank/` dosyalarını oluşturduktan sonra teknolojiye özel `.github/instructions/*.instructions.md` dosyalarını da üretir. Bunlar Copilot için birincil operasyonel kural kaynağıdır.

**Kural:**
- Her instruction dosyası tek bir konuya odaklanır.
- İçerik `foundation.md` ile çelişmez.
- `codingStandards.md` varsa onunla da çelişmez.
- Evrensel ama uygulanabilir best practice'ler içerir.
- Aşırı geniş `applyTo: "**"` kullanımından kaçınılır; mümkün olduğunda teknoloji veya klasör bazlı globs tercih edilir.

**Örnek eşlemeler:**
- React / Vue / frontend UI teknolojileri -> component, hooks/composables, state, styling kuralları
- Python / FastAPI -> modül yapısı, validation, dependency injection, test ve import düzeni
- Database / Prisma / ORM -> migration, naming, güvenli sorgu ve schema değişikliği kuralları

## Onarım ve Yeniden Hizalama
Bu rehber yalnızca ilk kurulum için değil, şu durumlarda da tekrar kullanılmalıdır:

- `.memory-bank/` dosyaları anlamsız, eksik veya çelişkili hale geldiyse
- `.github/instructions/`, `prompts/`, `agents/` veya `skills/` yapısı zamanla bozulduysa
- Ajanlar proje bağlamını kaçırmaya başladıysa
- Yeni proje şablonuna kopyalama sonrası temel dosyalar yeniden kurulacaksa

Bu durumda amaç mevcut sistemi silmek değil, mevcut gerçekliği koruyarak yapıyı blueprint standardına geri hizalamaktır.

---

## `BAŞLAT` Protokolü Son Adımı
Yukarıdaki dosyaları oluşturduktan sonra kullanıcıya dön ve şu mantıkla özet ver:

- Oluşturulan klasörler
- Oluşturulan veya güncellenen dosyalar
- Her dosyanın kısa amacı
- Tespit edilen teknoloji yığını
- Varsa belirsiz, eksik veya doğrulanması gereken noktalar

Son cümle şu niyeti taşımalıdır:
"Bellek Bankası altyapısının taslağını oluşturdum. İnceleme ardından revize isteklerin varsa belirtmeni, eğer yoksa taslağın nihai bellek bankası dosyaları olmasını onaylamanı bekliyorum."
