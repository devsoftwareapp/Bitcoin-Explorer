# Google Play Console - English store listing (Bitcoin Explorer)

Package: `com.devsoftware.bitcoinexplorer` · Version name 1.3 · Default language: English (United States)

## 1. App name (max 30)
Bitcoin Explorer

## 2. Short description (max 80)
Live Bitcoin fees, mempool, blocks and transactions. Track txs and wallets.

## 3. Full description (max 4000)
Bitcoin Explorer is a simple, fast viewer for the Bitcoin network. Check the fees you should pay right now, watch the mempool, and look up any transaction, address or block in seconds.

FEATURES
• Live fee estimates in sat/vB: fastest, about 30 minutes and about 1 hour
• Upcoming blocks map, colored by fee level, so you can see how busy the next blocks are
• Recent blocks with fill level, transaction count, size and mining pool
• Mining pool distribution for the latest blocks
• 3-month hashrate chart and difficulty adjustment progress
• Next halving countdown
• Transaction pages: inputs, outputs, fee, status, replacement (RBF) detection and an animated flow view
• Address pages: balance, total received and sent, and full transaction history with "load more"
• Block pages with all transactions, paginated
• Search by address, transaction ID or block height. Addresses are checked for a valid checksum before searching
• Favorites and recent searches
• Transaction tracking: get a notification when your transaction is confirmed and when it reaches 6 confirmations
• Wallet tracking: follow up to 10 addresses and get notified about new activity
• QR code for any address, with copy and share buttons
• Light, dark or system theme. Show amounts in BTC or sats, with prices in USD
• Pull to refresh, automatic refresh every 30 seconds, offline notice and an automatic backup data source

PRIVACY AND SAFETY
• This is not a wallet. It never asks for or stores private keys, seed phrases or passwords
• Read-only: it only displays public blockchain data
• No account, no sign-up, no ads and no analytics
• Favorites, history, tracked items and settings stay on your device. You can clear them in Settings

DATA
Data comes from public Bitcoin network APIs (mempool.space, with Blockstream as a backup). Prices are shown in USD and may be delayed.

NOTIFICATIONS
Tracking alerts are delivered while the app is open or running in the background. Android may delay them if it fully suspends the app.

This app is for information only and is not financial advice. Fees and prices change quickly.

## 4. Release notes - "What's new" (max 500)
Version 1.3 (new build)
• Whole interface is now in English
• New side menu: Favorites, tracked transactions and wallets, recent searches, Settings, About
• Wallet tracking: alerts for new activity on up to 10 addresses
• Paginated transaction lists on home and block pages
• Visual polish: compact header, theme-matched system bars, clearer dark theme
• Fixed double minus sign on negative amounts in address history
• New launcher icon with black background

## 5. Category, tags, contact
- Category: Finance (alternative: Tools)
- Tags (suggested): Bitcoin, crypto, blockchain, mempool, transaction tracker
- Content rating: complete the IARC questionnaire. No violence, no user-generated content, no ads, no in-app purchases.
- Contact email, website and privacy policy URL: required by Play. Fill with your own values (not in the repo).

## 6. Data safety form (suggested answers)
- Does the app collect or share user data? No
- Data sent off the device: none by the app itself. It only requests public data from Bitcoin APIs using the addresses/IDs the user types.
- Data stored on the device: favorites, recent searches, tracked items, settings (local storage only, can be cleared in Settings)
- Permissions: INTERNET, POST_NOTIFICATIONS (for tracking alerts)
- Encryption in transit: yes (HTTPS)
- Users can request data deletion: yes, via Settings > "Clear local data" (no server-side data exists)

Ad ID: not used. Apps with no ads and no analytics can answer "No" to advertising ID usage.

## 7. Graphics and screenshots

| Asset | Size | File |
|---|---|---|
| App icon (hi-res) | 512 x 512 PNG, no alpha | `graphics/app_icon_512.png` |
| Feature graphic | 1024 x 500 | `graphics/feature_graphic_1024x500.png` |
| Phone screenshots (4) | 1080 x 1920 | `screenshots/phone/*.png` |
| 7-inch tablet screenshots (4) | 1200 x 1920 | `screenshots/tablet7/*.png` |
| 10-inch tablet screenshots (4) | 1600 x 2560 | `screenshots/tablet10/*.png` |

Screenshot order and captions (use the same captions for all device types):
1. Live Bitcoin fees and mempool at a glance
2. Track any transaction, step by step
3. Check balances and history for any address
4. Favorites, tracking and wallet alerts

Screenshots are rendered from the real app UI (`www/index.html`). They use sample data because the app's live APIs are not reachable from the build environment. Before publishing, you may replace them with captures from a real device (Play rejects screenshots that do not show the app accurately, so either option is fine as long as the UI is the same).

Regenerate: `python3 play-store/capture_screenshots.py` and `python3 play-store/make_graphics.py`.

## 8. ASO notes
- Play does not use a keyword field. Put the important keywords in the title and short description, then repeat them naturally in the full description.
- Primary keywords: bitcoin explorer, bitcoin fees, mempool, bitcoin transaction, bitcoin block, bitcoin address, btc fee calculator.
- Secondary keywords: sat/vB, halving, hashrate, RBF, wallet tracker, transaction tracker.
- Localization: the store listing is English only (as requested). Add translations later under "Store listing > Translations" if needed.
- Test a Google Play Internal testing track first, then promote to Production.
