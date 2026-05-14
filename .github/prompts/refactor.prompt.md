---
description: "Use when evaluating a file against complexity thresholds or when the user explicitly requests to refactor / clean up code. Applies DRY principles, structural improvements, module extraction, and better variable naming while preserving existing business logic and ensuring tests pass. Involves the architectural agent for large file separations."
name: "Refactor Code"
argument-hint: "Specify the file or component to refactor"
agent: "senior-refactor-engineer"
---

# REFAKTÖR ET (REFACTOR CODE)

Bu komut tetiklendiğinde veya "Eşikler ve Kabul Kriterleri" ihlal edildiğinde, mevcut kodun kalitesini, okunabilirliğini, performansını ve güvenliğini sağlamak için yapısal bir refactoring (iyileştirme) süreci başlatılır. İş kuralları (business logic) kesinlikle değiştirilmez, sadece teknik yapı daha iyi hale getirilir.

## 1. Analiz ve Eşik Değerlendirmesi
1. Hedef dosyanın veya modülün tamamını (`read_file`) veya ilgili bölümlerini analiz et.
2. Aşağıdaki eşiklerin aşılıp aşılmadığını kontrol et:
    - **Dosya uzunluğu:** > 500 satır (Modül bölünmeli mi?)
    - **Fonksiyon/metot uzunluğu:** > 120 satır (Yardımcı fonksiyonlara ayrılmalı mı?)
    - **Sınıf boyutu:** > 300 satır (Tek Sorumluluk Prensibi ihlali var mı?)
    - **Siklomatik karmaşıklık:** > 20 (İç içe if-else blokları azaltılabilir mi?)
    - **Fonksiyon argüman sayısı:** > 7 (Veri sınıfları / Pydantic modelleri / DTO'lar kullanılmalı mı?)
3. Belirlenen yapısal sorunları (örneğin: Singleton kalabalığı, gereksiz global state, tekrarlayan kodlar - spaghetti code) listele.

## 2. Planlama ve İzin (Mimari Değişiklikler ve Dosya Bölme İçin)
1. Eğer refaktörizasyon yalnızca bir fonksiyon içindeyse ve dış API'yi/imzayı bozmuyorsa doğrudan uygulayabilirsin.
2. Eğer kodun dosyalar/modüller halinde bölünmesi gerekiyorsa (örneğin >500 satır sınırı aşıldıysa veya sorumluluklar ayrılacaksa), projeye en uygun temiz mimariyi kurmak için **derhal `@senior-architect` ajanını (`runSubagent` ile `senior-architect` olarak) devreye sok**. Mimar ajandan fonksiyon, sınıf ve modüllerin nasıl bir dosya ağacına ayrıştırılacağına dair kesin bir plan oluşturmasını iste.
3. Eğer dışa aktarılan (exported) fonksiyon imzaları değişecekse, ortak sınıflar silinip yeni modüllere taşınacaksa, önce yöneticiye (kullanıcıya) hem yapılacak değişiklikleri hem de mimarın modül/dosya bölme planını madde madde listele ve adım atmadan önce **onay iste**.
4. Değişiklik kodlarda farklı modülleri kıracaksa (örneğin bir model adının veya kütüphane yolunun değişmesi) oraları da düzeltmekle sorumlu olacağını planında belirt.

## 3. Standartlara Uygunluk
Aşağıdaki mimari/python kurallarını göz önünde bulundurarak refaktör işlemini uygula:
1. **DRY (Don't Repeat Yourself):** Tekrar eden mantıkları yardımcı fonksiyonlar içine çek.
2. **KISS (Keep It Simple, Stupid):** Olabildiğince düz mantık kullan, çok dallanmış `if/else` veya `try/except` zincirlerinden kaçın. Uzun döngüleri (loop comprehension), gereksiz döngüleri (`any`, `all`) kullanarak kısalt.
3. **Singleton ve Cache Yönetimi:** Eski tarz `global` değişkenler yerine Python'da `functools.lru_cache` gibi hazır dekoratörlerle temiz kalıplar kullan. 
4. **Tip İpuçları (Type Hints):** Fonksiyonların dönüş tiplerini (`-> Dict[str, Any]` gibi) ve varsa Pydantic model tanımlarını zorunlu olarak ekle.
5. **Oluşturulan Kodu Yorumla (Google / Numpy Style):** Refaktör edilmiş koda detaylı Docstring ekle.

## 4. Uygulama
1. Kodu güvenli parçalar (hunks) halinde `replace_string_in_file` kullanarak yenisiyle değiştir. Tüm modülü sıfırdan yazma zahmetine girme; eğer dosya çok karışıksa ve `replace` imkansızsa sadece o zaman blok olarak yaz.
2. İş mantığını (business logic) değiştirmemeye (%100 garanti olmalı) özen göster.
3. Modül içinde kullanımdan kalkmış (unused) kütüphane içe aktarmalarını (imports) sil.

## 5. Doğrulama (Testler)
1. Testlerin bozulup bozulmadığını kontrol et. Terminal'de (`run_in_terminal`) ilgili unit testleri koştur (`pytest tests/ilgili_test_dosyasi.py`).
2. Testler kırılırsa sorunu tespit edip kendin düzelt. Eğer test kapsamı çok dar ise, bu refactoring için test eklemesini de kendi inisiyatifinle öner/yap.

## Beklenen Sonuç
Sürdürülebilirlik ilkelerine (Eşiklere) uygun, tertemiz donanımla bezenmiş ve testleri geçen yenilenmiş bir kod bloğu (ve referans edilecek `.github/prompts/refactor.prompt.md` dosyası) ortaya çıkar.