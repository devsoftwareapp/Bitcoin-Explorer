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

## v1.1 ek özellikler
- Durum renkleri (yeşil onaylı, turuncu bekleyen, kırmızı değiştirilmiş/bulunamadı), kopyalama ikonları
- Geri tuşu / kenardan kaydırma, aşağı çekip yenileme, çevrimdışı şeridi
- Blok numarasıyla arama, adres checksum doğrulaması, "daha fazla yükle"
- Favoriler, son aramalar, işlem takibi (onay bildirimi), QR kod, paylaş
- Ayarlar: tema, para birimi (USD/EUR/GBP), BTC/sat
- Blockstream yedek API

## İmzalı release APK
Actions → "Android Release APK (imzali)". Kalıcı imza için repo secret'ları: `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`.
Secret yoksa geçici anahtarla imzalanır (her sürümde farklı, güncelleme olarak kurulmaz).
Not: Takip bildirimleri uygulama açıkken/arka planda canlıyken çalışır; Android uygulamayı tamamen uyutursa bildirim gecikebilir.
