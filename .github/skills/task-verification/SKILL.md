---
name: task-verification
description: "A multi-step workflow to verify that a claimed completed task block is fully implemented and documented. Use this when a release task is marked done and needs cross-cutting validation."
argument-hint: "Verify a task such as 14.2 Asset lifecycle schema"
user-invocable: true
disable-model-invocation: false
---

# Task Verification

## When to Use
- Bir görevin gerçekten tamamlandığı iddia edildiğinde
- Tamamlanan görevin dokümantasyon, kod, test ve state ile uyumunu kontrol etmek gerektiğinde
- Hala açık bir şüphe varsa veya görevin kapsamı belirsizse

## Procedure
1. Hedef task bloğunu `.memory-bank/state.md` içinde tanımla.
2. Görev tanımındaki maddeleri çıkar ve hangi değişikliklerin beklendiğini belirle.
3. Görevin referans verdiği dokümanlar varsa bunları ek kanıt olarak kullan.
4. Gerekli kod, schema ve test maddelerini tespit et.
5. Her bir gereksinimin karşılığını projede doğrula.
6. Bulduğun eksiklikleri açıkça listele.
7. Eğer görev gerçekten tamamlanmışsa, `state.md` içindeki ilgili satırı onayla.
8. Bu skill çalıştırıldığında `verify-task.prompt.md` tarafından kullanılması gereken agent ve prompt akışıyla uyumlu çalış.

## Output Format
- Kontrol edilen task bloğu
- Doğrulanan gereksinimler
- Eksik veya yanlış olan noktalar
- Gerekli düzeltme veya güncelleme önerisi
- Eğer `state.md` güncellemesi gerekiyorsa bunu belirt
