# Fırsat Haritası: Money Tracker by Spendee

Harika bir rapor. Spendee’nin zayıflıklarını ve pazar boşluklarını net bir şekilde ortaya koyuyorsun. Aşağıda, bu analize dayanarak **gerçekten boş olan ve yeni bir SaaS ile doldurulabilecek** fırsat alanlarını haritalandırıyorum.

---

### 1. Öncelikli Fırsat Alanları (Kanıta Dayalı 4 Madde)

1.  **Düzensiz Gelir + Proje Bazlı Karlılık Takibi (Freelance/Gig Ekonomisi)**
    - **Kanıt:** Raporda, Spendee’nin “sabit aylık gelir modeli” üzerine kurulu olduğu ve serbest çalışanlar için nakit akışı tahmini, “kötü ay” tamponlaması gibi özelliklerin olmadığı belirtiliyor. Ayrıca “Gelir-gider dengesini gerçek zamanlı görmek” ve “proje bazlı karlılık analizi” ana ihtiyaç olarak sıralanıyor.
    - **Fırsat:** Bu segment hızla büyüyor (gig ekonomisi) ve mevcut oyuncular (Mint, YNAB, PocketGuard) bu özel ihtiyacı karşılamıyor.

2.  **Bağlamsal, Proaktif AI Finans Koçluğu (Pasif Bildirimden Ajan’a Geçiş)**
    - **Kanıt:** Spendee’nin bildirimleri yüzeysel: “Harcamalarını optimize et” der ama *nasıl* yapılacağını söylemez. Kullanıcıya kişiselleştirilmiş, adım adım plan sunmaz. “Yüksek churn” ve “motivasyon eksikliği” buradan kaynaklanıyor.
    - **Fırsat:** RAG tabanlı asistan (ör. “Bu ay neden market harcamam arttı?” sorusuna veriyle cevap vermek) ve Agentic AI (abonelik iptali önerme, bakiye uyarısı yapma) pazarın görmezden geldiği bir katman.

3.  **Karmaşık Paylaşımlı Finans / Grup Bütçeleme (Aile, Ekip, Ortak İş)**
    - **Kanıt:** Spendee sadece “partner veya ev arkadaşı” senaryosunu destekliyor. “Karmaşık bölüşüm, ödeme hatırlatma, ortak bütçe” gibi grup finansı ihtiyaçları raporda açıkça boşluk olarak işaretlenmiş.
    - **Fırsat:** Özellikle aile içi okul harcamaları, tatil birikimi veya küçük ekip içi ortak masrafların yönetimi – çok kullanıcılı, hiyerarşik rollü bir yapı mevcut çözümlerde neredeyse yok.

4.  **Manuel Veri Girişini Sıfıra İndiren Otonom Veri Toplama (AI + Banka/API)**
    - **Kanıt:** Spendee’nin “AI fatura tarayıcı” olsa da kullanıcı hâlâ sık sık manuel giriş yapmak zorunda. Kullanıcı bir hafta sonra bunu “güncelleme yükü” olarak görmeye başlıyor. Banka bağlantısı yanlış kategorize ediyor.
    - **Fırsat:** Kullanıcının e-posta, WhatsApp, banka ekstrelerinden otomatik veri çeken ve bunları RAG ile sorgulanabilir hale getiren bir sistem – hatta “tek dokunuşla” çalışan.

---

### 2. Hedef Müşteri Segmenti (2 Spesifik Segment)

| Segment | Tanım | Temel İhtiyaç | Ödeme İsteği |
|---------|-------|---------------|--------------|
| **Freelance & Yan İş Yapan Bağımsız Profesyonel** | 25-45 yaş, düzensiz gelir (40k-120k USD/yıl), vergi sorumluluklarının farkında, QuickBooks gibi araçlara para harcıyor ama sadece kişisel finans için ayrı bir uygulama istiyor. | Gerçek zamanlı nakit akışı, proje bazlı kar marjı, vergi dilimi hazırlığı, otonom abonelik yönetimi. | Ayda 5-10$ (rapor: “abonelik ücreti ödemeye istekli”) |
| **Aile Finansı Yöneticisi (Evli, 2+ çocuklu, ortak hesap kullanan)** | 30-45 yaş, çift maaşlı, sabit giderleri (okul, fatura, tatil) yöneten, eşiyle birlikte bütçe yapmak isteyen ancak ayrı ayrı harcamaları da takip edebilen. | Çok kullanıcılı ortak bütçeler, anlık ödeme hatırlatmaları, hedef bazlı birikim (ör: “Tatil fonu”), çocuk harçlığı takibi. | Ayda 8-12$ (aile paketi) |

---

### 3. Rekabet Kör Noktaları

| Kör Nokta | Açıklama | Mevcut Oyuncularda Durum |
|-----------|----------|---------------------------|
| **Düzensiz Gelir Tahmin & “Kötü Ay” Tamponu** | Nakit akışının düzensiz olduğu durumlarda “en kötü ay” için uyarı ve tampon bütçe önerisi. | Hiçbir uygulama (Spendee, YNAB, PocketGuard) dalgalı geliri modellemez: ya sabit gelir varsayar ya da “ortalama” hesaplar. |
| **Proje Bazlı Tam Bütçe & Kar Analizi** | Freelance bir projenin giderlerini (malzeme, alt yüklenici, saatlik işçilik) ayrı ayrı takip edip net karı gösteren modül. | Ya sadece kişisel kategorilere (ör: Yemek, Ulaşım) sahipler ya da muhasebe yazılımlarına (QuickBooks) çok karmaşık. |
| **Otonom Abonelik & Tekrarlayan Ödeme Yönetimi** | Kullanıcı adına abonelikleri tarama, kullanılmayanları iptal teklif etme, artan fiyatları uyarma (Agentic AI). | Sadece pasif liste sunarlar (“abonelikleriniz”), iptal işlemini kullanıcıya bırakırlar. |
| **Vergi Dilimi Tahmini & Kesinti Planlaması** | Gelir-gider verisine dayanarak “yaklaşık vergi borcunuz” diyen ve “bu ay şu kadar kesinti yap” öneren AI. | Kişisel finans uygulamaları vergi konusuna girmez; muhasebe yazılımları ise pahalı ve karmaşıktır. |

---

### 4. Hızlı Kazanım (0-3 Ay)

**MVP: Freelance Nakit Akışı & Proje Karlılık Paneli**
- **Ne yapılır?**
  - Kullanıcının banka hesabını (Plaid/Finicity üzerinden) bağla.
  - Basit bir algoritma ile **öngörülen nakit akışı** çiz: “Önümüzdeki 2 hafta bakiye şu seviyeye düşebilir.”
  - Kullanıcıya “Yeni Proje Ekle” butonu ver: Proje adı, tahmini bütçe, başlangıç/bitiş. Uygulama bancadan çekilen işlemleri proje kategorisine otomatik ata.
  - **Push bildirimi:** “Freelance projeniz ‘Web Tasarımı’ %15 bütçe aşımına uğradı. Harcamaları kısıyor musunuz?”
- **Neden hızlı?** AI gerektir