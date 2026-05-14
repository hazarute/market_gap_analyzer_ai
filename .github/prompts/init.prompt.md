---
description: "Use when bootstrapping or re-aligning an AI-Driven Development project from README and docs, then creating or updating memory-bank and technology-specific instruction files for review."
name: "Init Project"
argument-hint: "Bootstrap a new project from README and dependency files"
agent: "agent"
---

# BAŞLAT

Bu komut tetiklendiğinde bir AI-Driven Development projesi ilk kez kuruluyor ya da mevcut kurulum yeniden hizalanıyor olabilir. README okunduktan sonra tek geçişli bootstrap veya onarım akışı olarak çalıştırılır. Aşağıdaki akışı sırayla uygula.

## Amaç
- Projenin amacını ve teknoloji yığınını detaylıca çıkar.
- Önce kök `README.md` dosyasını birincil kaynak olarak oku; README'yi projenin kalbi ve ana yönlendirici kaynak olarak kabul et.
- README'den sonra `docs/` klasöründeki belgeleri adım adım incele ve hafıza bankasını bu belgelerle hizala.
- `.github/memory-blueprint.md` kılavuzunu okuyarak `.memory-bank/` klasörü için çekirdek dokümanları gerçekten oluştur.
- Projede kullanılan ana teknolojilere göre `.github/instructions/` altında birincil başlangıç kural dosyalarını gerçekten oluştur.
- Son aşamada oluşturulan gerçek dosyaları kullanıcıya inceleme ve onay için sun.

## 1. Proje Analizi
1. Workspace kökündeki `README.md` dosyasını birincil kaynak olarak incele.
2. README'de işaret edilen veya projede mevcut olan `docs/` klasörünü tarayarak belge hiyerarşisini çıkar; önce indeks ve giriş dosyalarını, sonra alt teknik dokümanları incele.
3. `package.json`, `pyproject.toml`, `requirements.txt`, `composer.json`, `Cargo.toml` veya benzeri bağımlılık dosyalarını README ve docs bulgularını doğrulamak ve tamamlamak için tara.
4. `.github/memory-blueprint.md` dosyasını oku; bellek bankası dosya kapsamı, şablon başlıkları ve başlangıç standardı için bu dosyayı kanonik rehber kabul et.
5. Projenin amacını, ana teknoloji yığınını ve mevcut çalışma modelini tespit et.
6. Eğer birden fazla teknoloji varsa ana katmanları ayır:
   - Uygulama çekirdeği
   - Test altyapısı
   - UI / frontend
   - API / backend
   - Operasyon / deploy araçları
7. README ile dependency dosyaları veya docs çelişirse README birincil yönlendirici olsun; çelişkiyi ayrıca kullanıcıya bildir.
8. Eğer `memory-blueprint.md` ile proje gerçekliği arasında gerilim varsa, proje gerçekliğini koru ama sapmayı kullanıcıya açıkça not et.

## 2. Hafıza İnşası
Aşağıdaki çekirdek dosyaları oluştur; dosyalar zaten varsa önce mevcut içeriklerini oku ve gerektiğinde güncelle:
- `.memory-bank/foundation.md`
- `.memory-bank/state.md`
- `.memory-bank/decisions.md`

Bu dosyaların içeriğini serbest biçimde uydurma. `.github/memory-blueprint.md` içindeki amaç, bölüm yapısı ve doldurma kurallarını takip et.

`codingStandards.md` için ayrı kural:
- Bu dosya zorunlu değildir.
- Blueprint içinde önerilen koşullar sağlanıyorsa oluştur.
- Oluşturulmazsa, proje standartlarının birincil evi `.github/instructions/` olsun.

Dosyalar mevcutsa:
- Var olan içeriği körlemesine ezme.
- Önce mevcut içeriği oku.
- Gerekirse oluşturmak yerine güncelleme önerisi ver.

## 3. Dinamik Kural Üretimi
1. Tespit edilen ve gerçekten ihtiyaç duyulan her ana teknoloji için `.github/instructions/` altında ayrı bir dosya oluştur.
2. Her dosya tek bir konuya odaklansın.
3. Örnek:
   - React ise component, hooks ve state yönetimi kuralları
   - FastAPI / Python ise yapı, validation, test ve import düzeni kuralları
   - Database katmanı varsa migration ve güvenli sorgu kuralları
4. Kural dosyaları mevcut repo vizyonuyla çelişmemeli; başka projelere kopyalanabilir olmalı.
5. `codingStandards.md` oluşturulduysa onunla da çelişmemeli.
6. Teknoloji tespiti zayıfsa minimum güvenli iskeleti oluştur ve belirsiz alanları kullanıcıya not et.

## 4. Oluşturma Sonrası İnceleme ve Onay
Dosyaları oluşturduktan sonra şu formatta kullanıcıya sun:
- Oluşturulan klasörler
- Oluşturulan veya güncellenen dosyalar
- Her dosyanın kısa amacı
- Kritik çıkarımlar ve varsa README ile çelişen noktalar
- Kullanıcının isteyebileceği olası revizyon alanları

Kullanıcı bu aşamada:
- dosyaları inceleyip revize isteyebilir
- dosyaları doğrudan onaylayabilir

## 5. Çalışma Prensibi
- Tahmin yapma; bulguları önce README'ye, sonra dependency dosyalarına dayandır.
- Gereksiz dosya üretme; yalnızca gerçekten ihtiyaç duyulan başlangıç iskeletini oluştur.
- Çıktıyı kısa, düzenli ve başka projelere uyarlanabilir tut.
- Bu komutu normal geliştirme döngüsünde tekrar tekrar kullanma; bu bootstrap promptudur.

## Beklenen Sonuç
Bu prompt çalıştırıldığında proje için başlangıç klasör ve dosyaları gerçekten oluşturulur; ardından kullanıcıya oluşturulan dosyalar inceleme ve onay için sunulur. Bu akış, kök `README.md` ve `docs/` hiyerarşisi değişse bile başka projelerde de aynı mantıkla uygulanabilir.
