# Proje AI Asistanı Yapılandırması

> **Bu dosya nedir?** Her Copilot Chat oturumunda otomatik olarak yüklenir. Projenin tüm yapay zeka asistanları (Copilot, özel ajanlar) için ortak bağlam, kurallar ve iş akışlarını tanımlar.
>
> **⚠️ Karakter Sınırı:** Eğer bu dosya bir GitHub organizasyonu genelinde şablon olarak kullanılıyorsa **4000 karakter** sınırına tabidir. Repo bazında kullanımda bu sınır geçerli değildir.

---

## 1. Roller ve Çalışma Protokolü

| Rol | Kim | Sorumluluk |
|-----|-----|------------|
| **Yönetici** | Kullanıcı | Ne yapılacağını, iş kurallarını ve vizyonu belirler. |
| **Copilot / Ajanlar** | Yapay Zeka | Nasıl yapılacağını çözer, kod yazar, ajanları yönetir, Memory Bank'i günceller. |

### Çalışma Kuralları

1. **Herhangi bir kod üretmeden önce** `.memory-bank/` durumunu ve varsa `.github/instructions/` altındaki ilgili dosya bazlı kuralları **kontrol etmek zorunludur**.
2. **İletişim dili Türkçe'dir.** Kullanıcı farklı bir dilde yazmadığı sürece tüm yanıtlar Türkçe verilir.
3. **Pseudo-code (sözde kod) YASAKTIR.** Tüm kod örnekleri çalıştırılabilir, tip güvenlikli ve eksiksiz olmalıdır.
4. **Tahmin YASAKTIR.** Memory Bank ve `.github/instructions/` kuralları proje gerçekliğinin birincil kaynağıdır; kurallar uydurulmaz.
5. Öncelikle çalışma alanındaki `.github/` ve `.memory-bank/` dizinleri taranır.
   - `.github/instructions/` altındaki dosyalar, `applyTo` frontmatter'ına göre hedef dosya desenleriyle eşleşenler öncelikli olarak okunur.
   - Gerekirse ilgili ajan tanımları (`.agent.md`) ve prompt şablonları (`.prompt.md`) da taranır.
6. Aynı repo kökünde `AGENTS.md` veya `CLAUDE.md` dosyaları varsa, bunlar da otomatik talimat dosyası olarak değerlendirilir.

---

## 2. Proje Hafıza Sistemi (Memory Bank)

Projenin kalıcı hafızası `.memory-bank/` dizininde yaşar:

| Dosya | Amaç | Güncelleme Sıklığı |
|-------|------|-------------------|
| `foundation.md` | Projenin amacı, teknoloji yığını ve sistem mimarisi. | Başlangıçta oluşturulur, büyük değişikliklerde güncellenir. |
| `state.md` | Anlık odak, ilerleme durumu, `[ ]` / `[x]` görev listesi. | Her oturum sonunda güncellenir. |
| `decisions.md` | Projeye özel iş kuralları ve alınan kritik mimari kararlar. | Yeni karar alındığında ekleme yapılır. |
| `codingStandards.md` | **(Opsiyonel)** Proje kod standartlarının tek yerde özeti. | İhtiyaca göre. |

### Bellek Hiyerarşisi

- Birincil operasyonel kurallar: `.github/instructions/` > `.memory-bank/`
- Yardımcı standart kaynağı: `.memory-bank/codingStandards.md` (varsa)
- Çelişki durumunda: proje gerçekliği > `.github/instructions/` > `codingStandards.md`

---

## 3. Statik Yapılandırma (`.github/`)

| Dizin / Dosya | Amaç |
|---------------|------|
| `.github/instructions/` | Dosya/teknoloji bazlı kurallar (örn: `frontend.instructions.md`). `applyTo` frontmatter ile hedef dosya deseni belirtilir. `excludeAgent` ile belirli ajanlar hariç tutulabilir. |
| `.github/prompts/` | Tekrarlayan görevler için prompt şablonları. Komutlar tarafından referans alınır. |
| `.github/agents/` | Özel ajan tanımları (`.agent.md`). VS Code ajan seçicisinde görünür. |
| `.github/skills/` | **(Önizleme/Deneysel)** Ajan yetenek tanımları. |
| `.github/memory-blueprint.md` | Yeni proje başlatıldığında Memory Bank iskeletini kuran ana taslak. |

---

## 4. İş Akışları ve Komutlar (Router)

Aşağıdaki komutlar verildiğinde, ilgili prompt dosyası veya ajan **doğrudan çağrılır**. Prompt içeriği ezberden değil, belirtilen dosyadan okunur.

| Komut | Hedef | Açıklama |
|-------|-------|----------|
| **BAŞLAT** | `.github/prompts/init.prompt.md` + `.github/memory-blueprint.md` | Projeyi analiz ederek `.memory-bank/` ve `.github/` yapısını ilk kez kurar. Önce `README.md`, sonra `docs/` incelenir. |
| **BELLEĞİ YÜKLE** | `.github/prompts/load-memory.prompt.md` | Mevcut Memory Bank dosyalarının tamamını yükleyerek oturumu başlatır. |
| **DEVAM ET** | `.github/prompts/continue.prompt.md` | Kaldığın yerden devam et. |
| **DOKÜMAN EKLE/GÜNCELLE** | `.github/prompts/document-update.prompt.md` | Mevcut dokümanları günceller veya yenilerini oluşturur. |
| **GÖREV KONTROL ET** | `.github/prompts/verify-task.prompt.md` veya `@task-verifier` | Tamamlanan görev bloklarını kod, test ve doküman bazında derinlemesine doğrular. |
| **REFAKTÖR ET** | `.github/prompts/refactor.prompt.md` veya `@senior-refactor-engineer` | Eşik aşımlarında mevcut yapıyı temizler, DRY prensiplerini uygular. |
| **DEĞİŞİKLİKLERİ İŞLE** | `.github/prompts/commit-changes.prompt.md` | Yapılan değişiklikleri commit'ler. |
| **UYGULAMAYI TEST ET** | `.github/prompts/test-app.prompt.md` | Uygulama testlerini çalıştırır. |
| **BÜYÜK SÜRÜM PLANI** | `.github/prompts/plan-major-release.prompt.md` | Büyük sürüm revizyonları, breaking change yönetimi. |
| **KÜÇÜK SÜRÜM REVİZYONU** | `.github/prompts/apply-minor-release.prompt.md` | Dokümante edilmiş değişiklikleri doğrudan koda uygular, testleri günceller, memory bank'i senkronize eder. |

Tanımlı olmayan bir komut verilirse önce `.github/prompts/` taranır. Eşleşen dosya yoksa kullanıcıya eksik protokol bildirilir.

---

## 5. Ajan Havuzu (Agent Mapping)

| Ajan Adı | Dosya | Ne Zaman Kullanılır? |
|----------|-------|---------------------|
| `@senior-code-writer` | `.github/agents/senior-code-writer.agent.md` | Kod yazma, tamamlama, yeni özellik geliştirme. |
| `@senior-code-reviewer` | `.github/agents/senior-code-reviewer.agent.md` | Kod inceleme, güvenlik/perf/temiz kod denetimi. |
| `@senior-test-engineer` | `.github/agents/senior-test-engineer.agent.md` | Test yazımı, kapsam genişletme, edge-case. |
| `@senior-refactor-engineer` | `.github/agents/senior-refactor-engineer.agent.md` | Refactoring, kod temizliği, DRY/KISS. |
| `@senior-architect` | `.github/agents/senior-architect.agent.md` | Mimari planlama, breaking change değerlendirme. |
| `@memory-bank-librarian` | `.github/agents/memory-bank-librarian.agent.md` | Memory Bank güncelleme ve senkronizasyon. |
| `@documentation-specialist` | `.github/agents/documentation-specialist.agent.md` | Dokümantasyon keşfi, güncelleme planlaması ve belge tutarlılığı. |
| `@task-verifier` | `.github/agents/task-verifier.agent.md` | Görev tamamlama doğrulaması. |

---

## 6. Güvenlik ve Gizlilik (Kritik Yasaklar)

1. **API anahtarları, parolalar veya token'lar** asla kod, talimat veya hafıza dosyalarına yazılmaz. Bu bilgiler yalnızca `.env` üzerinden yönetilir.
2. **MCP (Model Context Protocol)** sunucularına bağlanırken `.env` verileri dışarı sızdırılmaz.
3. **OWASP Top 10** güvenlik açıklarına karşı tüm kod çıktıları kontrol edilir.
4. **Kullanıcı onayı olmadan** dosya sistemi yapısını kökten değiştiren, veri migrasyonu içeren veya dış servisleri etkileyen işlemler yapılmaz.

---

## 7. Taşınabilirlik Notu

Bu dosya, farklı projelere kopyalandığında da çalışacak şekilde tasarlanmıştır:

- `.memory-bank/`, `.github/instructions/`, `.github/prompts/` gibi klasörler zorunlu değildir; mevcutlarsa referans alınır.
- Genel başlangıç sırası: `README.md` → `docs/` → bağımlılık dosyaları → klasör yapısı doğrulaması.
- Dosya adları projeye göre değişebilir; önemli olan rollerin ve iş akışlarının korunmasıdır.