---
name: memory-sync
description: "Projedeki son değişiklikleri analiz ederek .memory-bank dizinindeki state.md, decisions.md ve foundation.md dosyalarını senkronize eden çok adımlı iş akışı. Use when: project state needs syncing after code changes, git changes must be reflected in memory bank, or decisions/state/foundation documentation should be updated from recent work."
argument-hint: "Analyze recent changes and propose memory-bank sync updates"
user-invocable: true
disable-model-invocation: false
---

# Memory Sync

## When to Use
- Son kod değişikliklerini .memory-bank ile senkronize etmek gerektiğinde
- State, decisions ve foundation dosyalarında tutarlılık sağlamak gerektiğinde
- Git geçmişinden veya çalışma alanı değişikliklerinden proje hafızası üretmek gerektiğinde

## Procedure
1. Git geçmişini veya çalışma alanındaki son kaydedilmemiş değişiklikleri analiz et.
2. `.memory-bank/state.md` dosyasını aç.
3. Biten görevleri `[x]` olarak işaretle.
4. Sıradaki görevi "Anlık Odak" olarak ayarla.
5. Yeni eklenen modüller veya iş mantıkları varsa bunları `.memory-bank/decisions.md` dosyasına yeni bir mimari karar olarak ekle.
6. `.memory-bank/foundation.md` ile çelişki olup olmadığını kontrol et.
7. Dosyaları doğrudan değiştirmeden önce kullanıcıya güncellenecek dosyaları ve farkları göster.

## Output Format
- Güncellenecek dosyaları açıkça listele
- Değişikliklerin kısa diff özetini ver
- Sonra onay iste
