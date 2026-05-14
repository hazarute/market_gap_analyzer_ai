# Master LLM Prompt: Habit Tracker - HabitKit

> Bu belge frontier modellere (Claude Opus, Gemini Pro, GPT-5) doğrudan yapıştırılmak üzere otomatik sentezlenmiştir.

---

# Master Prompt: Frontier AI için Habit Tracker SaaS Stratejisi

**Hedef Model:** Claude Opus / Gemini Pro / GPT-5  
**Çalışma Modu:** Tek seferlik analiz ve strateji çıktısı

---

## 1. Görev Çerçevesi

Sen bir AI Ürün Stratejisti olarak, bir habit tracker pazar analizi ve fırsat haritasını sentezleyerek aşağıdaki çıktıyı üreteceksin:

**Çıktı Hedefi:** Mevcut oyuncuların (özellikle HabitKit’in 4.43 puan, 10.677 değerlendirme) kör noktalarına dayanan, yeni bir habit tracker SaaS için **“0-12 aylık Strateji Dokümanı”** oluştur. Bu doküman şunları kapsamalı:
- MVP Planı (0-3 ay)
- GTM Stratejisi (0-6 ay)
- Orta Vadeli Yol Haritası (3-12 ay)
- Yönetici Özeti (yatırımcı pitch hazırlığı için)

**Önemli Kısıt:** Bu çıktı, tek bir frontier modele verildiğinde tek seferde çalışmalıdır. Hiçbir ek girdi veya düzeltme gerekmemelidir.

---

## 2. Bağlam Paketi

### 2.1 Pazar Özeti

| Boyut | Değer |
|-------|-------|
| Mevcut lider uygulama | Habit Kit (Sebastian Röhl) |
| Puan | 4.43 / 5 |
| Değerlendirme sayısı | 10,677 |
| Konumlandırma | Genel kitle, “herkese uygun” habit tracker |
| Zayıf noktalar | Kişiselleştirme sığ, sosyal hesap verebilirlik yok, nüks (relapse) yönetimi zayıf |

### 2.2 Öncelikli Fırsat Alanları (Kanıta Dayalı)

1. **Relapse (Nüks) Yönetimi & Motivasyon Bilimi** – Streak kaybını cezalandırmak yerine öğrenme fırsatına çeviren, kişiselleştirilmiş “yeniden başlatma” protokolleri. 1-2 haftada churn olan kullanıcıların ana nedeni.

2. **Bağlamsal & Akıllı Öneriler** – Kullanıcının enerji seviyesi, lokasyonu, takvim yoğunluğu ve geçmiş verilerine dayalı AI katmanı. Mevcut uygulamalar sadece “ne zaman” ve “ne” hatırlatır.

3. **Sosyal Hesap Verebilirlik Ekosistemi** – Gerçek zamanlı, küçük grup challenge’ları (3-5 kişi) ve profesyonel koç entegrasyonu. Mevcut çözümler ya tam bireysel ya da yüzeysel arkadaş ekleme.

4. **Niş Segmentasyon** – “Herkese uygun” yerine spesifik gruplar için özel kalıplar: DEHB bireyleri, yeni ebeveynler, dil öğrenenler.

### 2.3 Hedef Müşteri Segmentleri

| Segment | Profil | Ağrı Noktası | Fırsat |
|---------|--------|--------------|--------|
| Kaçınılmaz Dönüş (Relapse-Prone Professionals) | 25-45, yoğun iş temposu, en az 3 tracker denemiş, 2 haftada bırakmış | Streak kırılınca motivasyon kaybı, kendini başarısız hissetme, uygulamayı silme | Kaybı normalleştiren esnek metrikler (haftalık tamamlama yüzdesi) |
| DEHB’li Yetişkinler (Executive Dysfunction Warriors) | Dikkat dağınıklığı, başlatma güçlüğü | Arayüz görev listesi gibi hissettirir, “vücut çiftleme”, düşük bilişsel yük yok | Görsel/işitsel ipuçları, gevşek zaman çizelgesi, hiper odak sonrası tükenmişlik yönetimi |

### 2.4 Rekabet Kör Noktaları (Görmezden Gelinenler)

- **Başarısızlığı Keşfe Çevirmek:** Tüm rakipler streak’i kutsar. “Neden kaçırdın?” analizi + data-driven öneriler yok.
- **Gerçek Zamanlı Hesap Verebilirlik:** Anonim, canlı (live) küçük gruplar. “Ali şu anda egzersiz yapıyor” sosyal baskısı, mahremiyet endişeleri aşılmamış.
- **Habit Chaining Grafiği:** Alışkanlıkların birbirini nasıl tetiklediğini gösteren neden-sonuç ağı. “Sabah su içersen meditasyon olasılığı %70 artar” – hiçbir oyuncu sunmuyor.

### 2.5 Zamanlama Fırsatları

| Dönem | Fırsat | Somut MVP |
|-------|--------|-----------|
| 0-3 ay (Hızlı Kazanım) | Relapse Recovery Mode | API entegreli veya bağımsız mini SaaS: 3 adımlı toparlanma protokolü (anket + basitleştirme + mulligan jetons) |
| 3-12 ay (Orta Vade) | AI-Powered Suggestion Engine & Adaptive Scheduling | Google/Outlook takvim, Apple Health, ruh hali check-in verileri ile otomatik zaman ve zincir önerileri |

---

## 3. Kısıtlar ve Varsayımlar

### 3.1 Kısıtlar

| Alan | Kısıt |
|------|-------|
| **Bütçe** | Seed aşaması: $500K toplam (ilk 12 ay) |
| **Timeline** | MVP live: 3 ay içinde (H1 kullanıcı testi + pivot) |
| **Ekip** | Minimum: 1 PM, 2 mühendis (fullstack + AI/ML), 1 tasarımcı, yarı zamanlı domain expert (davranış bilimci/DEHB koçu) |
| **Teknik Altyapı** | GDPR uyumu zorunlu; Apple Health / Google Fit / Google Calendar API entegrasyonu baştan planlanmalı |
| **Platform** | Öncelik: Web + iOS (Avrupa ve ABD başlangıç pazarı) |

### 3.2 Varsayımlar

- Kullanıcıların habit tracker deneyiminde en kritik an “streak kırılması” sonrası ilk 24 saat.
- Mevcut uygulamaların çoğu (HabitKit dahil) sosyal hesap verebilirliği sadece “arkadaş ekleme” ile sınırlı tutuyor.
- DEHB segmenti, genel habit tracker pazarının %15-20’sini oluşturuyor (NIH verileri) ve sadakat oranı yüksek.
- API tabanlı bir “Relapse Recovery Mode” eklentisi, mevcut uygulamalardan kullanıcı çekmek için düşük engelli bir giriş stratejisi olabilir.

---

## 4. İstenen Çıktı Formatı

Her başlık aşağıdaki formatta yapılandırılmalıdır. Diğer ek formatlar serbesttir.

### 4.1 Yönetici Özeti (1 paragraf)
- Konsept, hedef pazar, temel farklılaştırıcı, beklenen KPI’lar.

### 4.2 MVP Planı (0-3 Ay)
- **Özellik Listesi** (tablo: özellik, açıklama, öncelik – P0/P1/P2)
- **Teknik Mimari** (kısa, API odaklı)
- **Kullanıcı Akışı** (relapse anından toparlanmaya: 3-5 adım)
- **Başarı Metrikleri** (ör: 7 günlük retention, relapse sonrası tekrar başlama oranı)

### 4.3 GTM Stratejisi (0-6 Ay)
- **Kanal Stratejisi** (topluluk odaklı: Reddit r/HabitTracker, DEHB forumları, Product Hunt)
- **Fiyatlandırma** (freemium + relapse recovery eklentisi ücretli)
- **Büyüme Hipotezi** (PLG + niş influencer iş birlikleri)

### 4.4 Orta Vadeli Yol Haritası (3-12 Ay)
- **AI Katmanı Entegrasyonu** (öneri motoru, habit chaining grafiği)
- **Segment Genişletme** (yeni ebeveynler, dil öğrenenler)
- **Gerçek Zamanlı Accountability** (anonim canlı gruplar – mahremiyet çözümü ile)

### 4.5 Yatırımcı Pitch Özeti (isteğe bağlı, 5 bullet)
- Problem, çözüm, TAM, iş modeli, ekip.

---

## 5. Kalite Eşiği

Çıktının kabul edilebilmesi için aşağıdaki 5 standart karşılanmalıdır:

| # | Standart | Açıklama |
|---|----------|----------|
| 1 | **Veriye Dayalı** | Her iddia ve öncelik, rapordan veya fırsat haritasından somut bir veri ile desteklenmeli (ör: “HabitKit 4.43 puan – 0.5 puanlık açık motivasyon düşüşü ve bırakma”) |
| 2 | **Uygulanabilirlik** | MVP özellikleri, verilen bütçe ($500K) ve timeline (3 ay) ile mühendislik takımı tarafından inşa edilebilir olmalı; “AI” lafı sadece pazarlama değil, somut girdi-çıktı tanımlı olmalı |
| 3 | **Rekabet Avantajı Net** | Fırsat haritasındaki 3 kör noktadan en az 2’sine doğrudan hitap edilmeli (başarısızlığı keşfe çevirme, gerçek zamanlı hesap verebilirlik, habit chaining) |
| 4 | **Hedef Kitle Tanımlı** | En az 2 spesifik segment (Relapse-Prone Professionals, DEHB’li Yetişkinler) için kişiselleştirilmiş özellikler belirtilmeli |
| 5 | **Metrik Odaklı** | Her aşamada başarıyı ölçmek için en az 1 nicel KPI tanımlanmalı (ör: “relapse sonrası 7 gün içinde tekrar başlay