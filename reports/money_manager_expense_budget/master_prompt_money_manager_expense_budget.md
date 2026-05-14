# Master LLM Prompt: Money Manager Expense & Budget

> Bu belge frontier modellere (Claude Opus, Gemini Pro, GPT-5) doğrudan yapıştırılmak üzere otomatik sentezlenmiştir.

---

Mükemmel bir analiz ve sentez çalışması. İşte, **frontier AI modeline doğrudan verilebilecek, tek seferde çalışan, kapsamlı master prompt**:

---

## MASTER PROMPT: KIŞISEL FİNANS ALANINDAKİ PASİF ASİSTAN BOŞLUĞUNA YÖNELİK ÜRÜN STRATEJİSİ

---

### 1. GÖREV ÇERÇEVESİ

Sen, **Kıdemli AI Ürün Stratejisti** ve **SaaS Growth Uzmanı** olarak görev yapıyorsun. Aşağıdaki pazar analizi (RAPOR) ve fırsat haritası (FIRSAT HARİTASI) belgelerini sentezleyerek, bir sonraki frontier AI modeli (Claude Opus/Gemini Pro/GPT-5) için **tek seferde çalıştırılabilir, doğrudan eyleme geçirilebilir** bir **Ürün Stratejisi ve MVP Planı** oluşturacaksın.

**Temel Görevin:** Mevcut rakip analizinde tespit edilen "Pasif Finansal Asistan" boşluğunu doldurmak için, **3 ay içinde test edilebilir, minimum kaynakla (1-2 kişilik ekip) inşa edilebilecek** bir AI-first kişisel finans uygulamasının stratejisini, MVP yol haritasını ve GTM (Go-To-Market) planını çıkarmak.

---

### 2. BAĞLAM PAKETİ

#### 2.1 Pazar Özeti

- **Rakip:** Money Manager Expense & Budget (Realbyte Inc.) – Apple App Store'da 4.81 puan, 2839 değerlendirme.
- **Mevcut Güçlü Yönleri:** Yüksek kullanıcı bağlılığı, "double entry" muhasebe sistemi, niş (finans okuryazarı) kitle.
- **Kritik Zayıf Noktaları:**
  - Tamamen manuel veri girişi
  - Kategorizasyon katılığı (akıllı öneri yok)
  - Geçmişe odaklı, proaktif/öngörücü özellik yok
  - Öğrenme eğrisi yüksek (yeni kullanıcıyı kaybeder)
  - AI tabanlı harcama içgörüsü/öneri sıfır

#### 2.2 Fırsat Alanları (4 Öncelikli)

1. **Proaktif AI Asistan (Agentic AI)** – Kullanıcı adına düşünen, uyaran, öneren sistem
2. **Otomatik Veri Girişi + Doğal Dil Kategorizasyonu** – Sıfır manuel giriş hedefi
3. **Tahmine Dayalı Bütçe ve Nakit Akışı Yönetimi** – Geleceği öngören, eyleme dönüşen uyarılar
4. **Karma-Denge Kullanıcı Arayüzü** – Aynı üründe "basit mod" ↔ "double entry mod" geçişi

#### 2.3 Rekabet Kör Noktaları

- **Hiçbir rakip** pasif, sürekli yanında olan bir AI asistanı sunmuyor.
- **Hiçbir rakip** "neden çok harcıyorsun, şu aboneliği iptal et" gibi akıllı öneri yapmıyor.
- **Hiçbir rakip** "önümüzdeki hafta bütçen aşılacak, şu harcamayı ertele" gibi proaktif uyarı vermiyor.
- **Muhasebe bilenler** ile **sadece harcamasını görmek isteyenler** arasındaki orta yol boş.

#### 2.4 Hedef ICP (İdeal Müşteri Profili)

- **Segment 1 – "Farkında Ama İlgisiz" (Birincil Hedef):** 25-40 yaş, beyaz yaka/freelancer, finans okuryazarlığı orta-düşük, manuel giriş yapmaz, haftada 1-2 kontrol eder.
- **Segment 2 – "Küçük İşletme Sahibi":** 30-50 yaş, freelance (tasarımcı/yazılımcı/danışman), iş ve kişisel finans iç içe, fatura takibi ister.
- **Ortak Payda:** "Kontrol duygusunu kaybetmek" acı noktasındalar; AI otomasyonu ile ikna edilebilirler.

#### 2.5 Varlık Anlayışı

- RAG (Retrieval Augmented Generation): Doğal dil ile harcama girişi ve kategorizasyon
- Agentic AI: Proaktif uyarılar, bütçe yönetimi, abonelik optimizasyonu
- Predictive ML: Zaman serisi tahmini, nakit akışı öngörüsü
- CV/NLP: Fatura tanıma (OCR ile)

---

### 3. KISITLAR VE VARSAYIMLAR

| Kısıt / Varsayım | Değer |
|------------------|-------|
| **Bütçe** | Ön tohum (Pre-Seed) aşaması – $50k-$100k (MVP için) |
| **Timeline** | MVP: 12 hafta (3 ay), ilk kullanıcı testi: 16. hafta |
| **Minimum Ekip** | 1 AI mühendisi (full-stack + ML), 1 product manager (yarı zamanlı, strateji + UX) |
| **Teknoloji Stack Varsayımı** | LLM API (GPT-4/Claude 3.5), OCR için AWS Textract, veritabanı için PostgreSQL + vector store (pgvector), zaman serisi için Prophet/ProphetNet |
| **Veri Girişi Varsayımı** | Başlangıçta manuel + OCR; banka API entegrasyonu Phase 2'ye bırakılacak (Plaid/Finicity tipi entegrasyon maliyetli) |
| **Monetizasyon Varsayımı** | Freemium model: temel özellikler ücretsiz, AI asistanı premium ($4.99/ay) |
| **Yasal Varsayım** | Veri gizliliği için SOC 2 Type I başlangıç seviyesi; GDPR uyumu (AB pazarı opsiyonel) |

---

### 4. İSTENEN ÇIKTI FORMATI

Aşağıdaki **4 bölümden** oluşan kapsamlı bir **Ürün Stratejisi ve MVP Planı** çıktısı üret:

#### Bölüm A: MVP Ürün Yol Haritası (90 Gün)

| Hafta | Faz | Çıktılar |
|-------|-----|----------|
| 1-3 | Foundation | Kullanıcı onboarding akışı, manuel harcama girişi (basit UI), temel kategorizasyon (statik) |
| 4-6 | AI Core | OCR fatura tanıma (fotoğraf çek → otomatik kayıt), RAG tabanlı doğal dil girişi (ör: "kahve 35 TL" → otomatik kategori) |
| 7-9 | Agentic Özellikler | Bütçe aşımı uyarıları (basit rule engine), "Bu ay aboneliklere 500 TL ödedin – kullanmadıklarını iptal et?" önerisi |
| 10-12 | Predictive & UI | Gelecek 2 hafta nakit akışı tahmini, "Basit Mod / Muhasebe Modu" geçişi, kullanıcı testi için hazır MVP |

**Her faz için spesifik çıktılar:**
- **Faz 1:** Onboarding ekranı + harcama giriş formu + 6 ana kategori (Yemek, Ulaşım, Fatura, Eğlence, Sağlık, Diğer)
- **Faz 2:** OCR (fatura fotoğrafı → metin → kayıt) + NLP input ("dün 3 kahve aldım 105 TL" → 3 kayıt)
- **Faz 3:** Kullanıcı tanımlı bütçe eşiği aşımında push bildirim + haftalık "AI raporu" (abonelik analizi)
- **Faz 4:** 30 günlük harcama verisine dayalı tahmin (basit Prophet model) + UI toggle (Basit/Double Entry)

#### Bölüm B: GTM (Go-To-Market) Stratejisi

1. **İlk Pazar:** Türkiye (İstanbul, Ankara, İzmir) – Hedef ICP'nin yoğun olduğu büyükşehir
2. **Kanallar:**
   - LinkedIn (freelancer/white-collar grupları)
   - Product Hunt (early adopter kitlesi)
   - Influencer iş birliği (finans okuryazarlığı hesabı👉 "tasarruf tüyoları")
   - Üniversite kariyer merkezleri (stajyer/fresh grad kitlesi)
3. **Dönüşüm Kaldıracı:** "3 dakikada kayıt, 0 manuel giriş" – onboarding akışında ilk harcamayı OCR ile yaptır
4. **Pricing:** Freemium + Premium ($4.99/ay): AI asistanı, tahminler, abonelik optimizasyonu premium'da

#### Bölüm C: Yatırımcı Sunumu İçin 10 Slayt Özeti (Ana Hatlar)

1. **Kapak – Vizyon:** "Pasif AI Finans Asistanı ile Herkesin Cebinde Bir Muhasebeci"
2. **Problem:** Rakip uygulamalar manuel, geçmişe odaklı, karmaşık (veri ve kanıt)
3. **Çözüm:** Proaktif, otomatik, tahmin eden AI katmanı
4. **Neden Şimdi?** LLM/RAG teknolojisi olgunlaştı, bankacılık API'leri yaygınlaştı
5. **Hedef Kitle:** 25-40 yaş "farkında ama ilgisiz" ICP (Türkiye'de 5M+ potansiyel)
6. **MVP Planı:** 12 haftada çalışan ürün
7. **AI Mimarisi:** RAG + Agentic + Predictive (nasıl çalıştığı)
8. **GTM:** Büyükşehir → Türkiye → AB (sıralı genişleme)
9. **Ekip:** 2 kişi, lean startup yaklaşımı
10. **Finansallar:** 6. ayda 1000 premium kullanıcı hedefi ($60k ARR), CAC < $15

#### Bölüm D: Riskler ve Mitigasyonlar (Zorunlu)

| Risk | Olasılık | Etki | Mitigasyon |
|------|----------|------|------------|
| OCR doğruluk düşük | Orta | Yüksek | MVP'de manuel düzeltme ekle; Phase 2'de fine-tuning |
| Kullanıcı veri mahremiyeti endişesi | Yüksek | Yüksek | Onboarding'de net veri politikası; on-device processing opsiyonu |
| Banka API entegrasyonu gecikmesi | Düşük | Orta | MVP'de OCR + manuel ile başla; API'yi premium özellik yap |
| LLM maliyeti (scale'de) | Orta | Orta | Prompt compression; batch processing; küçük model fine-tuning |

---

### 5. KALİTE EŞİĞİ (KABUL EDİLEBİLİR MİNİMUM STANDARTLAR)

Çıktı aşağıdaki kriterleri KESİNLİKLE karşılamalıdır:

1. **Uygulanabilirlik:** Her özellik, hafta bazında, hangi ekiple inşa edileceği net olmalı. "AI ile yapacağız" soyutlaması kabul edilmez; hangi LLM, hangi teknik yaklaşım (RAG/Agent/ML) belirtilmeli.
2. **Kantitatif Hedef:** MVP sonunda en az 1 **ölçülebilir kullanıcı testi metriği** tanımlanmalı (ör: "OCR hata oranı < %10" veya "kullanıcı onboarding tamamlama > %70").
3. **Finansal Fizibilite:** Verilen bütçe ($50k-$100k) ve ekip (1+1) ile 12 haftada yapılabilir olmalı. Cloud maliyeti, LLM token maliyeti minimumda tutulmalı.
4. **Rekabet Farklılaşması:** Çıktıda en az 1 özellik, rapor ve fırsat haritasında tespit edilen **hiçbir rakibin yapmadığı** bir şey olmalı (ör: proaktif abonelik optimizasyonu).
5. **Kapsayıcılık:** Hem "finans okuryazarı" hem "finans okuryazar