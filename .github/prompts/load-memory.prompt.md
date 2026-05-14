---
description: "Use when loading the project's current mental context before continuing work. Reads memory-bank files and relevant technology instructions, then returns a short readiness summary."
name: "Load Memory"
argument-hint: "Load project memory and summarize current context"
agent: "agent"
---

# BELLEĞİ YÜKLE

Bu komut tetiklendiğinde projenin zihinsel bağlamını yüklemen gerekir. Aşağıdaki adımları uygula.

## 1. Okuma
1. `.memory-bank/foundation.md` dosyasını oku.
2. `.memory-bank/state.md` dosyasını oku.
3. `.memory-bank/decisions.md` dosyasını oku.
4. `.memory-bank/codingStandards.md` varsa oku; yoksa bunu hata olarak değerlendirme.

## 2. Kuralları Tara
1. `.github/instructions/` altındaki teknoloji bazlı kural dosyalarını gözden geçir.
2. Yalnızca mevcut görev veya repo yapısıyla ilgili kuralları zihinsel bağlama al.
3. Eğer `instructions/` klasörü henüz yoksa bunu kısa bir not olarak belirt, ancak bağlam yükleme akışını durdurma.

## 3. Özet Rapor
Yöneticiye şu formatta çok kısa bir rapor ver:
- **Mevcut Durum:** `state.md` içindeki `Mevcut Odak`
- **Sıradaki Görev:** öncelikle `Mevcut Odak` ile en uyumlu aktif `[ ]` görevi seç; böyle bir eşleşme net değilse `Aktif Faz` altındaki ilk `[ ]` görevi kullan. Kullanıcı mevcut sohbette farklı bir görevden ilerlemek istediğini açıkça belirtirse onu esas al.
- **Hazırım:** `Hafıza yüklendi, komutlarınızı bekliyorum.`

## Çalışma Prensibi
- Rapor kısa olsun; uzun özet üretme.
- Bilgi uydurma; bulunamayan alanları kısa ve açık şekilde belirt.
- `.memory-bank/` ile `.github/instructions/` arasında çelişki görürsen bunu kısa bir risk notu olarak ekle.
