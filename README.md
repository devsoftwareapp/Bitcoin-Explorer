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

## Özellikler
- Renkli, koyu/açık tema uyumlu arayüz
- Mempool haritası (sıradaki bloklar, ücrete göre renkli)
- Son bloklar (doluluk seviyesi + ücret rengi), havuz dağılımı
- Hashrate grafiği, zorluk ayarı, halving sayacı
- Adres / işlem / blok detayları, giriş-çıkış listesi
- 30 sn'de bir otomatik yenileme
