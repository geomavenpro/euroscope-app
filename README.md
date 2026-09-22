# EuroScope v3.1 — Learning Radar

EuroScope, AÇA/EEA + Copernicus + Eionet ekosistemini takip eden ve aynı zamanda sistematik mini dersler sunan kişisel PWA'dır.

## v3.1
- Radar günde 3 kez çalışır: yaklaşık 09:00, 15:00, 21:00 Türkiye saati.
- Yeni haber olmasa da öğrenme içeriği üretir/döndürür.
- Öğrenme kartları artık 3–5 dakikalık anlamlı mini ders formatındadır: nedir, neden önemli, erişim/kullanım, kişisel bağlantı, çalışma fikri ve temel kavramlar.
- Copernicus Land Products, CDSE API dokümantasyonu ve Eionet Dataflows kaynakları radar kapsamına eklendi.
- Öğren sekmesinde müfredat görünür.
- İlgi profili cihazda saklanmaya devam eder; iPhone ve Samsung ayrı profillere sahip olabilir.

## Kurulum / güncelleme
Bu paketin içindeki `.github`, `docs`, `scripts`, `README.md`, `requirements.txt` öğelerini repository köküne kopyala. GitHub Desktop'ta commit + push yap. Ardından Actions > EuroScope Radar > Run workflow ile ilk v3.1 verisini üret.

> Not: Gerçek iOS/Android push notification altyapısı bu pakette henüz yoktur. GitHub Actions günde üç kez radarı günceller; uygulama açıldığında güncel içerik görünür.
