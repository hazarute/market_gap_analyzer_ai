# Master LLM Prompt: Expenses: Spending Tracker

> Bu belge frontier modellere (Claude Opus, Gemini Pro, GPT-5) doğrudan yapıştırılmak üzere otomatik sentezlenmiştir.

---

Harika bir görev. Verilen [RAPOR] belgesi oldukça bozuk ve anlamsız metinler içerse de (muhtemelen bir işleme hatası), [FIRSAT HARİTASI] belgesi son derece net, analitik ve aksiyon odaklıdır. Bu iki kaynağı sentezleyerek, bir frontier AI modelinin **tek seferde** kapsamlı bir ürün stratejisi üretebilmesi için aşağıdaki master prompt'u oluşturdum.

---

## MASTER PROMPT: SaaS Ürün Stratejisi Oluşturma

---

### 1. Görev Çerçevesi

Sen, bir **AI Ürün Stratejisti ve Prompt Mimarısın**. Aşağıda verilen pazar analizi verilerini ve fırsat haritasını kullanarak, **sıfırdan bir finansal takip SaaS ürünü** için kapsamlı bir **MVP Planı ve Go-to-Market (GTM) Stratejisi** oluşturmalısın.

Amacın, mevcut bir rakip uygulamanın (Expenses: Spending Tracker) pazar boşluklarını ve rekabet kör noktalarını analiz ederek, **3-6 ay içinde piyasaya sürülebilecek, niş bir hedef kitleye hitap eden, yapay zeka destekli** bir ürün konsepti geliştirmektir. Çıktı, bir yatırımcıya veya üst yönetime sunulabilecek profesyonellikte olmalıdır.

---

### 2. Bağlam Paketi

**Mevcut Pazar Durumu:**
- **Rakip Uygulama:** Expenses: Spending Tracker (BLUE COMET LABS LLC, iOS only)
- **Puan / Değerlendirme:** 4.66 / 173 değerlendirme
- **Konumlandırma:** "Basit ve özel" harcama takibi. Kişisel kullanıma odaklı, paylaşımsız, yalnızca iOS.
- **Çıkarım:** Uygulama niş bir kitlede çok seviliyor (yüksek puan), ancak pazar erişimi son derece sınırlı (düşük değerlendirme sayısı). **Büyüme potansiyeli var.**

**Fırsat Alanları (Kanıta Dayalı):**
1.  **Çok Platformlu Eksiklik:** Android ve web arayüzü yok. Masaüstü ve Android kullanıcıları boşlukta.
2.  **Küçük İşletme / Serbest Çalışan Boşluğu:** Uygulama tamamen kişisel. Freelance çalışanların kişisel-iş giderlerini ayırma ihtiyacı karşılanmıyor.
3.  **Proaktif Zeka Eksikliği:** Uygulama sadece "takip ediyor". Otomatik bütçe önerisi, anomali uyarısı, "ne olurdu" senaryoları gibi AI katmanları tamamen yok.

**Rekabet Kör Noktaları:**
- Otomatik harcama alışkanlığı öğrenme ve hedef oluşturma.
- Zaman serisi tahmini ve senaryo simülasyonu ("Harcamanı %20 azaltırsan 3 ayda X biriktirirsin").
- E-posta/fatura taraması ile abonelik yönetimi ve iptal önerisi.
- Paylaşımlı abonelik takibi (Splitwise benzeri).

**Hedef Müşteri Segmentleri (Öncelikli):**
- **Segment A (Freelance Creator):** Düzensiz gelir, iş-kişisel gider karmaşası, vergi raporu ihtiyacı.
- **Segment B (Aile Yöneticisi):** Ortak harcama yönetimi, mahremiyet, ortak hedef koyma.

**Risk Faktörleri:**
- Veri gizliliği endişesi (Uçtan uca şifreleme ile azaltılabilir).
- Rakibin (Expenses) beklenmedik büyümesi (Hızlı kazanım ile sadık taban oluşturarak azaltılabilir).

---

### 3. Kısıtlar ve Varsayımlar

**Sert Kısıtlar:**
- **Bütçe:** İlk 6 ay için toplam $150,000 (geliştirme, pazarlama, operasyon dahil).
- **Timeline:**
  - 0-3 Ay: MVP geliştirme ve kapalı beta.
  - 3-6 Ay: Halka açık lansman ve ilk 1000 kullanıcıya ulaşma.
- **Ekip Büyüklüğü:** Çekirdek ekip en fazla **3 kişi** (1 Full-stack geliştirici, 1 UI/UX tasarımcı, 1 Ürün/Pazarlama sorumlusu). Gerektiğinde freelance destek alınabilir.

**Varsayımlar:**
- Hedef kitle (Freelance Creator & Aile Yöneticisi) mobil önceliklidir, ancak web arayüzü takibi tamamlar.
- Kullanıcılar verilerinin güvenliği konusunda hassastır; yerel cihazda kalma seçeneği kritiktir.
- İlk MVP'de Open Banking API entegrasyonu yapılmayacak, manuel giriş ve akıllı kategorizasyon ile başlanacak.

---

### 4. İstenen Çıktı Formatı

Aşağıdaki bölümleri içeren, profesyonel, tek bir doküman oluştur. Çıktı, bir yatırımcı sunumunun giriş sayfası veya bir ürün yol haritası belgesi olarak kullanılabilir olmalıdır.

**Doküman Yapısı:**
1.  **Yönetici Özeti (1 Paragraf):** Ürünün adı, temel vaadi ve hedef pazarı.
2.  **MVP Özellik Seti (0-3 Ay):** "Hızlı Kazanım" odaklı, geliştirilecek en kritik 3-5 özellik.
3.  **GTM Stratejisi (3-6 Ay):** Kullanıcı edinme kanalları, konumlandırma mesajı, ilk 1000 kullanıcı hedefine ulaşma taktiği.
4.  **Monetizasyon Modeli:** Freemium yapısı, premium özelliklerin listesi ve fiyatlandırma önerisi.
5.  **Rekabetçi Farklılaşma Matrisi:** Expenses ve diğer 2 rakip (YNAB, MoneyLover) ile karşılaştırma tablosu.
6.  **Risk ve Risk Azaltma Planı (En fazla 3 madde).**

---

### 5. Kalite Eşiği

Çıktının kabul edilebilmesi için aşağıdaki standartları karşılaması zorunludur:
- **Somutluk:** Her özellik ve strateji, açıkça tanımlanmış ve gerekçelendirilmiş olmalıdır ("AI destekli akıllı kategorizasyon" yerine "Kullanıcının son 30 günlük harcama etiketlerini öğrenen ve yeni bir harcamayı %90 doğrulukla otomatik kategorize eden model").
- **Eyleme Dönüştürülebilirlik:** MVP özellikleri, 3 kişilik bir ekip tarafından 3 ayda geliştirilebilecek büyüklükte olmalıdır.
- **Veri Odaklılık:** Tüm iddialar, verilen [RAPOR] ve [FIRSAT HARİTASI]'ndaki kanıtlara dayandırılmalıdır (ör: "Expenses'in 173 değerlendirmesi ve 4.66 puanı, niş bir kitlede yüksek memnuniyet olduğunu ancak erişimin sınırlı kaldığını gösterir").
- **Rekabetçi Duruş:** Ürünün, mevcut oyunculardan (özellikle Expenses) en az 2 somut noktada net bir şekilde farklılaştığı belirtilmelidir.

---

### 6. Örnek Giriş / Beklenen Çıktı Formatı

**Giriş (Buraya herhangi bir kullanıcı girişi gerekmez; prompt bağımsız çalışır):**
```json
{ "task": "create_saas_strategy", "source_data": { "report": "...", "opportunity_map": "..." } }
```

**Beklenen Çıktı Formatı (Kısmi Örnek):**

```markdown
# Ürün Stratejisi: [Ürün Adı]

## 1. Yönetici Özeti
[Ürün Adı], freelance çalışanlar ve aileler için tasarlanmış, kişisel ve işletme giderlerini tek bir arayüzde yöneten, yapay zeka destekli bir finansal asistan uygulamasıdır. Mevcut oyuncuların (Expenses, YNAB) görmezden geldiği "proaktif bütçe önerisi" ve "paylaşımlı abonelik yönetimi" boşluklarını doldurarak, 6 ay içinde 1000 aktif kullanıcıya ulaşmayı hedefler.

## 2. MVP Özellik Seti (0-3 Ay)
- **Özellik 1: Paylaşımlı Abonelik Yöneticisi** - Kullanıcılar grup oluşturur, ortak abonelikleri (Netflix, Spotify) ekler ve her üyenin ne kadar ödemesi gerektiğini otomatik hesaplar.
- **Özellik 2: Akıllı Harcama Kategorizasyonu** - Kullanıcının geçmiş harcamalarını öğrenen ve yeni girişleri otomatik olarak doğru kategoriye atayan temel bir ML modeli.
- **Özellik 3: Çapraz Platform Senkronizasyonu** - iOS, Android ve Web MVP’si. Veriler uçtan uca şifrelenmiş bulutta saklanır.

## 3. GTM Stratejisi (3-6 Ay)
- **Konumlandırma Mesajı:** "Birlikte harcıyorsanız, birlikte takip edin."
- **Kanal 1:** Product Hunt lansmanı.
- **Kanal 2:** Freelance topluluklarında (Twitter, LinkedIn, Reddit r/freelance) "Harcama takibinin en büyük sorunu nedir?" anketi ile organik bü