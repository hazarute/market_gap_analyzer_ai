---
description: "Use when test-app found failures. Analyze failing tests, propose and apply fixes, and update memory bank with resolution notes."
name: "Fix Test Failures"
argument-hint: "Resolve failing tests and sync state/decisions"
agent: "senior-test-engineer"
---

# TEST HATALARINI DÜZELT

Bu komut tetiklendiğinde test çalıştırması sırasında tespit edilen hataları çözmen ve hafıza bankasını uyarlaman gerekir.

## 0. Kullanılacak Agent
- Bu prompt `senior-test-engineer` agentını kullanır. 
- Alternatif olarak "@senior-test-engineer rolünü çağır" yaklaşımı üzerinden de uygulanabilir.

## 1. Hata Analizi
1. `test-app` çıktısından başarısız testleri ve hata mesajlarını al.
2. İlgili kod, test ve talimat dosyalarını (`.github/instructions/`) incele.
3. Hatanın kök nedenini belirle (sınır koşulu, yan etkili çalışma, eksik koşul, yanlış varsayım, vs.).

## 2. Düzeltme Önerisi
1. En az müdahaleyle hatayı gideren çözümü öner.
2. Gerekirse yeni veya mevcut testleri genişlet, boylece hatanın tekrar ortaya çıkması engelle.
3. Değişiklikler çok büyükse önce yönetici onayı iste.

## 3. Uygulama
1. Onay alındıysa kod/test güncellemelerini uygula.
2. Uygulamayı local testler ile doğrula.
3. Başarısız testler artık geçiyorsa, güncellenen test sonuçlarını raporla.

## 4. Hafıza Bankası Senkronu
1. `.memory-bank/state.md` üzerinde ilgili görevleri güncelle:
   - tamamlanan görevi `[x]` yap
   - gerekirse `Mevcut Odak` ve `Aktif Faz` ile hizala
2. `.memory-bank/decisions.md` içine hata kaynağı ve çözüm yaklaşımı ile kısa karar notu ekle.
3. Gerekliyse `.github/instructions/` içinde yeni kural/uygulama maddesi eklemeyi öner.

## 5. Kısa Sonuç
Yöneticiye bildir:
- Hata tipi ve neden
- Uygulanan düzeltme
- Güncellenen test sonuçları
- Hafıza bankası ve instruction değişiklikleri

## Beklenen Sonuç
Testler geçti, memory banka senkronize oldu, ve proje devam etmeye hazır hale geldi.
