---
description: "Use when performing version sync commit and push process after changing release version files."
name: "Commit & Push"
argument-hint: "Follow release commit and push workflow"
agent: "memory-bank-librarian"
---

# COMMIT & PUSH İŞ AKIŞI

1. Sürüm tespiti:
   - `VERSION=$(awk 'NR==1{print $1}' version.txt)`
   - Yeni sürüm belirlendiğinde (örn. v0.2.1), `version.txt` ana kaynak olarak kullanın.
   - Sürüm değişikliğini yansıtmak için aynı zamanda `docs/api/openapi.yaml`, `mobile/app.json`, `mobile/package.json`, `mobile/package-lock.json`, `mobile/README.md` ve `mobile/screens/ScaffoldOverviewScreen.tsx` dosyalarını kontrol edin.

2. Dosya senkronizasyonu:
   - `version.txt` -> `${VERSION} - <kısa açıklama>` ile güncelle ve iş/tarih notu ekle.
   - `mobile/app.json` -> gerekli alanları `VERSION` ile uyumlu hale getir.
   - `mobile/package.json` -> `"version": "${VERSION}"`.
   - `mobile/package-lock.json` -> `"version": "${VERSION}"` ve varsa lockfile sürüm alanlarını güncelle.
   - `docs/api/openapi.yaml` -> release sürümü ve contract değişikliklerini yansıtacak şekilde güncelle.
   - `mobile/README.md` -> sürüm notlarını ve mobil runtime parity durumunu güncelle.
   - `mobile/screens/ScaffoldOverviewScreen.tsx` -> ilgili sürüm/amiral notlarını güncelle.

3. Git adımları:
   - `git add version.txt docs/api/openapi.yaml mobile/app.json mobile/package.json mobile/package-lock.json mobile/README.md mobile/screens/ScaffoldOverviewScreen.tsx .memory-bank/state.md .memory-bank/decisions.md`
   - `git commit -m "release: v${VERSION} version sync + docs"`
   - `git push origin main`

4. Tag ve release:
   - `git tag -a "v${VERSION}" -m "Release v${VERSION}"`
   - `git push origin "v${VERSION}"`

5. CI önerisi:
   - Pipeline içinde `VERSION` değerini `version.txt`'den okuyun.
   - Docker image `halalinvest:${VERSION}` şeklinde tagleyin.
   - `semantic-release`/changelog otomasyonu için commit mesajı formatını takip edin.
