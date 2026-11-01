# Bitcoin Explorer

Sade, Türkçe Bitcoin explorer. Veri kaynağı: mempool.space herkese açık API'si (anahtarsız).

## APK alma
Her `main` push'unda GitHub Actions debug APK üretir:
Actions → son çalışma → Artifacts → `bitcoin-explorer-debug-apk`.

## Geliştirme
```
npm install
npx cap sync android
```
Web arayüzü `www/` klasöründedir.
