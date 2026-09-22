# EuroScope v3

Installable PWA for iPhone, Samsung/Android and desktop. Tracks AÇA/EEA, Copernicus Land, Copernicus Data Space and Eionet; provides a daily learning card; ranks content using interests stored locally on each device.

## Privacy
- No Telegram token.
- No account data is collected by the app.
- Interests/name are stored only in that browser/device via localStorage.
- Each phone has its own independent profile.
- Source monitoring runs in GitHub Actions.

## GitHub
Keep these at repository root: `.github`, `docs`, `scripts`, `requirements.txt`.
Actions runs daily at 06:00 UTC (09:00 Türkiye time).

## Hosting
A PWA needs an HTTPS web address. GitHub Pages from a private repository may depend on the GitHub plan/account settings and does not by itself make the published site private. If strict private access is required, deploy behind an authentication layer instead of relying on an obscure URL.

## Install
- iPhone: open the HTTPS app URL in Safari > Share > Add to Home Screen.
- Samsung: open in Chrome/Samsung Internet > Install app / Add to Home screen.

## Notifications
This package intentionally does not pretend to provide background push notifications. Reliable iPhone/Android push requires a push backend/provider plus user permission. The dashboard itself updates from GitHub Actions. Push can be added as a separate secure deployment step.
