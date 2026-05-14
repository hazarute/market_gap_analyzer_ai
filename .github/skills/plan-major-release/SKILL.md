---
name: plan-major-release
description: "Skill to orchestrate a major-release planning workflow. Runs the `plan-major-release` prompt, generates proposed `.memory-bank` and `.github/instructions` changes, runs `memory-sync` to create diffs, and manages approval flow for committing the updates."
argument-hint: "Plan and produce vetted diffs for a major version upgrade; coordinate memory-sync and commit flow"
user-invocable: true
disable-model-invocation: false
---

# Plan Major Release Skill

Kullanım: Bu skill, büyük sürüm planlamasını otomatikleştirmek ve plan sonucu oluşan hafıza/instruction değişikliklerini `memory-sync` ile doğrulayıp onaylı bir şekilde commit sürecine taşımak için tasarlanmıştır.

Özet akış:

1. `plan-major-release.prompt.md`'i çalıştır ve kapsam, riskler, migration adımları, önerilen `decisions.md` girdileri ile rollout checklist üret.
2. Üretilen `decisions.md`/`state.md`/`.github/instructions` değişikliklerini taslak olarak bir branch/çalışma alanı içinde oluştur (draft files veya PR önerisi).
3. `memory-sync` (ya da `memory-sync` skill) çağrısı yaparak bu taslak değişikliklerin `.memory-bank` üzerindeki etkisini analiz et ve kısa difflar üret.
4. `docs/<hedef-sürüm>/<hedef-sürüm>.md` içinde oluşturulan inceleme dokümanını onay paketine ekle ve yöneticinin gözden geçirmesini sağla.
5. Yöneticiye/operatöre kısa bir onay paketi sun: difflar, etkilenebilecek alanlar, rollback planı, önerilen PR başlığı.
6. Yönetici onayı alındığında `commit-changes.prompt.md` veya doğrudan `memory-sync` onaylı çıktıları kullanarak `.memory-bank` ve ilgili `instructions` güncellemelerini uygulayın; aksi halde taslağı kapatın ve geri bildirim toplayın.

Procedure (detaylı):

- Adım A — Başlatma:
  - Kullanıcıdan hedef sürümü ve kısa açıklamayı al.
  - `plan-major-release` prompt'unu çağır ve çıktıyı topla.

- Adım B — Taslak Oluşturma:
  - Prompt çıktılarını kullanarak önerilen `decisions.md` maddelerini ve `state.md` görevlerini taslak olarak oluştur (workspace içinde `release-plan/` altına dosyalar bırakmak önerilir).
  - Önerilen `.github/instructions/` değişikliklerini kısa maddeler halinde hazırla.

- Adım C — Memory Sync İncelemesi:
  - `memory-sync` skill'ini çağır ve taslak dosyaların `.memory-bank` üzerindeki etkisini analiz etmesini iste.
  - `memory-sync` çıktısından açıkça hangi dosyaların değişeceğini ve kısa diffları al.

- Adım D — Onay İstemek:
  - Yöneticiye tek satırlık özet ve link/diff sun.
  - Onay yoksa: değişiklikleri geri al veya taslağı güncelle—tekrar Adım C.

- Adım E — Uygulama:
  - Onay verildikten sonra `commit-changes` prompt'unu çağırarak `.memory-bank` değişikliklerini uygulayın (ve/veya PR oluşturup merge sürecini takip edin).

## Output Format

- `summary.md` — kısa özet (kapsam, riskler, rollback planı)
- `diffs/` — taslak vs mevcut `.memory-bank`/instructions diffları
- `docs/<hedef-sürüm>/<hedef-sürüm>.md` — yöneticinin gözden geçirmesi için sürüm notu dokümanı
- `proposed_decisions.md` — PR için kullanılacak `decisions.md` taslağı
- `approval_package` — onay için gerekli kısa diff özetleri, etkilenen dosyalar ve risk notları

## Success Criteria

- Plan, hedef sürüm ve geriye dönük uyumluluk argümanını açıkça içerir.
- `.memory-bank` etkileri `memory-sync` tarafından analiz edilmiştir.
- Etkilenen dosyalar ve nedenleri net bir şekilde listelenmiştir.
- Yönetici onayına sunulmak üzere bir diff/özet paketi hazırlanmıştır.
- Onay alındığında `.memory-bank` ve varsa `.github/instructions/` güncellemeleri uygulanmak üzere hazır hale getirilmiştir.

Önerilen agent: `senior-architect` (strateji + planlama) ile `memory-bank-librarian` (senkron onay akışı) birlikte kullanılmalıdır. Test/düzeltme adımları `senior-test-engineer` ile ayrı prompt/skill'lerde yürütülmelidir.

Güvenlik & Onay ilkeleri:

- Bu skill doğrudan kalıcı değişiklik uygulamaz; her durumda yönetici onayı gerektirir.
- Gizli bilgiler `decisions.md` vb. içine yazılmamalıdır; hassas veriler `.env` veya güvenli vault'larda saklanmalı, referansları only (not values) yazılmalıdır.

Not: `memory-sync` skill'i mevcutsa bu skill onu çağırarak diffları üretmelidir. Eğer `memory-sync` yoksa, alternatif olarak `commit-changes` prompt'una çıkarılacak kısa diff özetleri hazırlanabilir.
