# Master LLM Prompt: Money Tracker by Spendee

> Bu belge frontier modellere (Claude Opus, Gemini Pro, GPT-5) doğrudan yapıştırılmak üzere otomatik sentezlenmiştir.

---

Aşağıda, talimatlarınıza uygun olarak hazırlanmış **tek seferde çalışan, kapsamlı master prompt** bulunmaktadır. Bu prompt, bir frontier AI modeline (Claude Opus / Gemini Pro / GPT-5 seviyesi) verilmek üzere tasarlanmıştır ve yukarıdaki iki kaynak belgenin sentezini içermektedir.

---

## MASTER PROMPT

### 1. GÖREV ÇERÇEVESİ

Sen bir AI ürün stratejisti ve girişim danışmanısın. Görevin, aşağıda verilen **pazar analizi raporu** ve **fırsat haritası** belgelerini kullanarak, yeni bir **kişisel finans yönetimi SaaS ürünü** için eksiksiz bir stratejik plan oluşturmaktır. Plan, **MVP (Minimum Viable Product) özellik seti**, **Go-to-Market (GTM) stratejisi** ve **yatırımcı sunumu taslağını** içermelidir.

Bu plan, mevcut oyuncuların (Spendee, Mint, YNAB, PocketGuard) zayıflıklarından yararlanacak, **yapay zekâ (RAG + Agentic AI) ile 10x değer yaratacak** ve **freelance/gig ekonomisi çalışanları ile aile finansı yöneticileri** segmentlerine odaklanacak şekilde tasarlanmalıdır.

### 2. BAĞLAM PAKETİ

#### Pazar Özeti
- Mevcut uygulama **Spendee (Money Tracker)**, geniş kitleye hitap eden, “one-size-fits-all” bir bütçeleme uygulamasıdır. Puanı 4.65, 566 değerlendirme.
- **Temel zayıflıkları:** Manuel veri girişi yorgunluğu, yüzeysel bildirimler, düzensiz gelir yönetimi eksikliği, paylaşımlı finans kısıtlılığı, yüksek churn.
- **Pazar boşluğu:** Hiçbir rakip, **düzensiz gelirli bağımsız profesyoneller** ve **aile finansı yöneticileri** segmentlerini uçtan uca çözmüyor.

#### Fırsat Alanları (Öncelikli 4 Madde)
1. **Düzensiz Gelir + Proje Bazlı Karlılık Takibi** (Freelance/Gig Ekonomisi) – Büyüyen segment, mevcut uygulamalar sabit gelir varsayıyor.
2. **Bağlamsal, Proaktif AI Finans Koçluğu** – RAG tabanlı asistan ve Agentic AI (abonelik dedektifi, nakit akışı koruyucusu, proje karlılık ajanı).
3. **Karmaşık Paylaşımlı Finans / Grup Bütçeleme** – Aile, ekip, ortak iş için çok kullanıcılı yapı.
4. **Otonom Veri Toplama** – E-posta, WhatsApp, banka ekstrelerinden otomatik veri çekerek manuel girişi sıfıra indirme.

#### Rekabet Kör Noktaları
- Düzensiz gelir tahmini ve “kötü ay” tamponu.
- Proje bazlı tam bütçe & kar analizi.
- Otonom abonelik & tekrarlayan ödeme yönetimi (iptal teklifi).
- Vergi dilimi tahmini & kesinti planlaması.

#### Hedef ICP (İdeal Müşteri Profili)
- **Segment 1:** Freelance & yan iş yapan bağımsız profesyonel (25-45 yaş, 40k-120k USD/yıl dalgalı gelir, ayda 5-10$ ödemeye istekli).
- **Segment 2:** Aile finansı yöneticisi (30-45 yaş, çift maaşlı, 2+ çocuklu, ayda 8-12$ aile paketi).

#### AI Çözüm Stratejisi (Rapordan)
- **RAG Asistanı:** Kullanıcının finansal verilerini çekerek doğal dilde sorulara yanıt verir (ör: “Bu ay neden harcamam arttı?”).
- **Agentic AI:** Otonom ajanlar (Abonelik Dedektifi, Nakit Akışı Koruyucusu, Proje Karlılık Ajanı) kullanıcı onayıyla görev yürütür.

#### Hızlı Kazanım (0-3 Ay MVP)
- **Freelance Nakit Akışı & Proje Karlılık Paneli:** Banka bağlantısı (Plaid/Finicity), nakit akışı tahmini, “Yeni Proje Ekle” butonu, otomatik harcama atama, push bildirimleri.

### 3. KISITLAR VE VARSAYIMLAR

#### Kısıtlar
- **Bütçe:** Tohum öncesi/başlangıç aşaması (500k–1 Milyon USD).
- **Timeline:** MVP 3 ay içinde geliştirilmeli; beta 6 ay; tam lansman 9 ay.
- **Minimum Ekip Büyüklüğü:** 1 Product Manager, 2 Full-Stack Geliştirici, 1 AI/ML Mühendisi, 1 UX/UI Tasarımcısı. (Opsiyonel: 1 veri bilimci)
- **Teknoloji Yığını:** Web + Mobile (React Native veya Flutter), Bulut (AWS/GCP), LLM API (GPT-4 / Claude 3.5), Vektör DB (Pinecone/Weaviate), Banka API (Plaid/Finicity).

#### Varsayımlar
- Kullanıcı izni ile finansal verilere (banka, e-posta, mesaj) erişim mümkündür.
- LLM API maliyetleri kullanıcı başına aylık ~0.50–1.00 USD’dir ve abonelik fiyatına yedirilebilir.
- Hedef segmentler aylık 5–12 USD ödemeye isteklidir (rapordan).
- MVP sonrası kullanıcı geri bildirimi ile yinelemeli geliştirme yapılacaktır.

### 4. İSTENEN ÇIKTI FORMATI

Çıktı aşağıdaki yapıda, **bölüm başlıkları net olacak şekilde** düzenlenmelidir. Her bölüm somut, uygulanabilir ve veriye dayalı olmalıdır.

**I. Executive Summary** (1 paragraf)  
- Ürünün adı (yaratıcı olabilir, örn: “FlowFin”), vizyon, hedef pazar, temel farklılaştırıcı.

**II. Ürün Vizyonu ve ICP**  
- Net ICP tanımı (iki segment için ayrı ayrı).  
- Kullanıcı problemleri ve ürünün çözüm vaadi.  
- Rekabet avantajı (kör noktalara atıf).

**III. MVP Özellik Seti (0-3 Ay)**  
- En fazla 5–7 temel özellik. Her özellik için:  
  - Açıklama  
  - Kullanıcı faydası  
  - Teknik gereksinim (AI/API/entegrasyon)  
  - Geliştirme süresi tahmini (gün/hafta)

**IV. AI Mimarisi (RAG + Agentic AI)**  
- Yüksek seviyeli sistem tasarımı (veri akışı, LLM kullanımı, ajanlar).  
- Hangi ajanlar MVP’de yer alacak? (en az 2: Abonelik Dedektifi, Nakit Akışı Koruyucusu).  
- Kullanıcı onay mekanizması nasıl işleyecek?

**V. GTM Stratejisi**  
- **Kanallar:** Product Hunt, Reddit (r/freelance, r/personalfinance), LinkedIn (freelance toplulukları), niş bloglar, influencer iş birlikleri.  
- **Fiyatlandırma:** Freelance bireysel (5$/ay), Aile paketi (10$/ay), Yıllık %20 indirim.  
- **Büyüme Taktikleri:** Referans programı, ücretsiz deneme (14 gün), içerik pazarlaması (vergi ipuçları, proje karlılık rehberi).  
- **İlk 1000 kullanıcı hedefi:** Lansman sonrası 3 ayda 1000 ödeme yapan kullanıcı.

**VI. Yatırımcı Sunumu Taslağı (10 Slayt)**  
- Her slayt için başlık ve 2–3 bullet anahtar mesaj.  
- Slayt sırası: Kapak → Problem → Çözüm → Pazar Büyüklüğü → Ürün → AI Farklılaştırıcı → İş Modeli → MVP Yol Haritası → Ekip → Yatırım İsteği & Kullanım.

**VII. Riskler ve Azaltma Planı**  
- En az 3 risk (ör: veri gizliliği endişesi, LLM halüsinasyonu, düşük kullanıcı benimsemesi) ve her biri için azaltma stratejisi.

### 5. KALİTE EŞİĞİ

Çıktının kabul edilebilmesi için aşağıdaki standartları karşılaması zorunludur:

1. **Spesifiklik:** Genel geçer ifadeler (ör: “kullanıcı deneyimini iyileştir”) yerine somut özellikler, rakamlar ve teknik detaylar kullanılmalı.
2. **Nedensellik:** Her öneri (özellik, kanal, fiyat) rapordan veya fırsat haritasından bir kanıta dayandırılmalı.
3. **Uygulanabilirlik:** MVP özellik seti, 3 ay ve 4-5 kişilik ekip ile gerçekçi olarak geliştirilebilir olmalı.
4. **AI Entegrasyonu:** AI bileşenleri (RAG, ajanlar) teknik olarak açıklanmalı ve hangi sorunu çözdükleri belirtilmeli.
5. **Veri Odaklılık:** Fiyatlandırma, segment büyüklüğü, kullanıcı ödeme isteği gibi kararlar sayısal verilere dayanmalı.
6. **Tutarlılık:** Tüm bölümler birbiriyle uyumlu olmalı (ör: GTM’de hedeflenen segment, MV’deki özelliklerle örtüşmeli).

### 6. ÖRNEK GİRİŞ / BEKLENEN ÇIKTI FORMATI

**Örnek Giriş (bu prompt zaten giriş niteliğindedir)**  
Yukarıdaki tüm talimatlar, bağlam belgeleri ve kısıtlar tek bir girdi olarak verilmiştir.

**Beklenen Çıktı Formatı (ilk bölüm örneği):**

**I. EXECUTIVE SUMMARY**

FlowFin, freelancer’lar ve aileler için tasarlanmış, yapay zekâ destekli bir kişisel finans yönetimi SaaS’tir. Mevcut uygulamaların (Spendee, YNAB) düzensiz geliri modelleyememesi ve pasif bildirimlerle sınırlı kalmasından yararlanır. RAG tabanlı bir asistan ve otonom finans ajanları sayesinde kullanıcıların nakit akışını gerçek zamanlı yönetmelerini, proje bazlı karlılık görmelerini ve aboneliklerini otomatik optimize etmelerini sağlar. MVP 3 ayda pazara çıkacak, ilk yıl 10.000 ödeme yapan kullanıcı hedeflenmektedir.

... (devamı)

---

Not: Lütfen çıktıyı **doğrudan bu formatta** ve **yukarıdaki tüm bölümleri kapsayacak** şekilde üret. Her bölümün başlığını net bir şekilde belirt. Çıktıyı bir iş planı dokümanı gibi düşün; yatırımcıya sunulmaya hazır, profesyonel