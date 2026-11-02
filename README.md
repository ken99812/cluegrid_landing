# ClueGrid landing page

A static website (plain HTML, CSS and JavaScript, no build step) in the game's own look:
sky background with drifting letter tiles, chunky 3D buttons, cream panels, and a small
playable arrowword in the hero.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page |
| `styles.css` | All styles (colours taken from the app's `AppColors`) |
| `app.js` | The playable mini puzzle and the drifting tiles |
| `privacy/`, `terms/`, `eula/`, `legal.css` | Legal pages (generated, see below) |
| `vercel.json` | Clean addresses (`/privacy`, not `/privacy/index.html`) and aliases such as `/terms-and-conditions` |
| `assets/logo.png`, `assets/logo.webp` | The ClueGrid logo |
| `assets/pictures/` | Picture clues (Noto Emoji, Apache License 2.0) |
| `assets/fonts/` | Nunito and Jost, the app's fonts (SIL Open Font License, licences included) |

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
npx serve .
```

## Publish

Any static host works. With Vercel: import the repository, framework preset "Other",
no build command, output directory `.`. Then point `playcluegrid.app` (and `www`) at it.

## Before launch

- The store buttons link to `https://apps.apple.com/app/id6819964219` and
  `https://play.google.com/store/apps/details?id=app.playcluegrid`; they work once the app
  is live in each store.
- Legal pages: `/privacy` (also `/privacy/es`, `/privacy/tr`, `/privacy/ru`), `/terms` and `/eula`, built by `python3 scripts/build-legal.py` (company name, email and date are set at the top of that script). The privacy text comes from the backend (`scripts/privacy.json`, exported from `src/platform/legal/privacy-text.ts`), so it matches `https://api.playcluegrid.app/privacy`. Use `https://playcluegrid.app/privacy`, `/terms` and `/eula` in App Store Connect and Google Play.
- The footer shows `privacy@playcluegrid.app`; make sure that mailbox exists.
