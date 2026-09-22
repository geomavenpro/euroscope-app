# EuroScope v4 — Personal Earth Intelligence Academy

**Bu paket v3.2 çalışan deponun üstüne kopyalanır.** `docs/data/items.json` bu ZIP içinde **yoktur**: GitHub Actions tarafından üretilen mevcut dosyanı koru; eski sürümdeki conflict tekrar etmesin.

- Öğren sekmesinde tam metinli 12 ders, günlük 45 dakikalık plan, cihazda saklanan ilerleme, AÇA/SNE hazırlık listesi, araştırma/uygulama fikirleri.
- Ana sayfada günlük akademi kartı. Radar başlıkları mevcut kaynak metnini kesmeden gösterir.
- Radar günlük 3 kez çalışır; ilk 12 uygun HTML sayfasından daha uzun açıklama almaya çalışır. Kaynak içeriği alınamazsa uydurma özet üretmez.
- Bildirim eklenmedi; OneSignal/API anahtarı gerekmiyor.
- **Gerçek otomatik AI özetleyici değil:** statik doğrulanmış dersler + kaynak sayfa metinleri. Yeni derslerin kendiliğinden yazılması için daha sonra güvenli bir AI backend gerekir.

Kurulum: ZIP'i açıp içindeki `docs`, `scripts`, `.github` klasörlerini mevcut `euroscope-app` deposuna kopyala. GitHub Desktop'ta `EuroScope v4 Academy` commit → Push origin. Actions'ta EuroScope Radar çalıştır. iPhone'da gerekirse sayfayı yenile.
