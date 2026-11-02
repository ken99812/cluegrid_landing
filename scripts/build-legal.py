#!/usr/bin/env python3
"""Builds the legal pages of the website: /privacy/ (with /privacy/es/, /privacy/tr/,
/privacy/ru/), /terms/ and /eula/. Run from the repository root after changing anything here:

    python3 scripts/build-legal.py

The privacy policy text comes from scripts/privacy.json, exported from the backend
(src/platform/legal/privacy-text.ts) so the app's link and the website say the same.
"""
import html
import json
from pathlib import Path

# Who provides ClueGrid and how to reach them, per page language. Change here, then rebuild.
OPERATOR = {
    'en': 'the ClueGrid team',
    'es': 'el equipo de ClueGrid',
    'tr': 'ClueGrid ekibi',
    'ru': 'разработчик ClueGrid',
}
EMAIL = 'privacy@playcluegrid.app'
UPDATED = {
    'en': '2 November 2026',
    'es': '2 de noviembre de 2026',
    'tr': '2 Kasım 2026',
    'ru': '2 ноября 2026 г.',
}

ROOT = Path(__file__).resolve().parent.parent
LANG_NAMES = {'en': 'English', 'es': 'Español', 'tr': 'Türkçe', 'ru': 'Русский'}

TERMS = {
    'title': 'Terms of Service',
    'intro': 'These terms apply when you use ClueGrid, the crossword game for iPhone and Android, and this website. ClueGrid is provided by {operator} (“we”, “us”). By playing, you accept these terms. Last updated: {date}.',
    'sections': [
        ('Who can play', [
            'You must be at least 13 years old, or older where your country requires it, to use ClueGrid. If you are under 18, a parent or guardian should read these terms with you.',
        ]),
        ('Your account', [
            'When you first open the app we create a guest account for you. You can link it to Apple or Google sign-in to keep your progress across devices. Keep your device and sign-in secure: you are responsible for what happens on your account.',
            'Choose a display name that is not offensive, does not impersonate anyone and does not include personal contact details. We may change or remove names that break these rules.',
        ]),
        ('Coins and purchases', [
            'Coins are a virtual currency for use in ClueGrid only. You earn them by playing and watching rewarded videos, or buy them in the app. Coins have no cash value, cannot be exchanged for money and cannot be transferred to another player.',
            'Purchases are made through the App Store or Google Play and follow their terms, including their refund rules. A refunded purchase may be removed from your account, including the coins or benefits it gave.',
            '“Remove ads” turns off interstitial ads between puzzles. Optional rewarded videos, which you choose to watch for coins, stay available.',
            'We may change prices, rewards and the items on offer. Changes never take away coins you already have, except to correct a clear error or after a refund.',
        ]),
        ('Ads', [
            'The free game shows ads from our advertising partners. Rewards for watching a video are given only when our server receives confirmation from the ad network, and there is a daily limit.',
        ]),
        ('Fair play', [
            'Do not cheat, use bots, scripts or modified versions of the app, exploit bugs, or interfere with leaderboards, other players or our servers. Do not try to access accounts or data that are not yours.',
            'If you break these rules we may reset scores or coins, remove you from leaderboards, or suspend or close your account.',
        ]),
        ('Puzzles and content', [
            'Puzzles, clues, pictures, sounds, the ClueGrid name and logo, and the app itself belong to us or our licensors. Many puzzles and clues are created with the help of artificial intelligence and checked automatically; if you find a mistake, please use “Report an error” in the app.',
            'We grant you a personal, non-exclusive, non-transferable right to use the app for your own entertainment, as set out in the End User License Agreement.',
        ]),
        ('Reports and feedback', [
            'When you send a report or feedback, you allow us to use it to improve ClueGrid, without payment to you.',
        ]),
        ('Changes and availability', [
            'We keep improving ClueGrid and may add, change or remove features, puzzles, languages or the service as a whole. We are not liable if the game is unavailable for a time, for example during maintenance.',
            'We may update these terms. For important changes we will tell you in the app before they apply; if you keep playing afterwards, you accept the new terms.',
        ]),
        ('Ending your account', [
            'You can delete your account at any time in the app: Settings, Account, Delete account. Coins and purchases on a deleted account are lost and cannot be restored.',
            'We may close an account that breaks these terms or the law, or that has been inactive for a long time, after notice where we can give it.',
        ]),
        ('Our responsibility', [
            'ClueGrid is provided “as is”. To the extent the law allows, we do not guarantee that the game is free of errors or always available, and we are not liable for indirect or consequential losses. Our total liability to you is limited to the amount you paid us in the 12 months before the claim.',
            'Nothing in these terms limits rights you have as a consumer that cannot be limited by contract, or our liability for death or personal injury caused by negligence, or for fraud.',
        ]),
        ('Law and disputes', [
            'These terms are governed by the laws of the country where the operator of ClueGrid is established, without taking away the protection of mandatory consumer laws of the country where you live. You may bring a claim in the courts of the country where you live.',
            'If any part of these terms is found invalid, the rest stays in force.',
        ]),
        ('Contact', ['{operator}, {email}']),
    ],
}

EULA = {
    'title': 'End User License Agreement',
    'intro': 'This End User License Agreement (“Agreement”) is between you and {operator} (“Licensor”) and covers the ClueGrid app (the “App”) for iPhone and Android. By installing or using the App you agree to it. Last updated: {date}.',
    'sections': [
        ('1. License', [
            'Licensor grants you a limited, non-exclusive, non-transferable, revocable license to install and use the App on devices you own or control, for your personal, non-commercial entertainment. On Apple devices, this is limited to Apple-branded products that you own or control, as permitted by the Usage Rules in the Apple Media Services Terms and Conditions, except that the App may be used by other accounts associated with you through Family Sharing or volume purchasing.',
        ]),
        ('2. Restrictions', [
            'You may not copy, modify, translate, reverse engineer, decompile or disassemble the App except where the law expressly allows it; rent, lease, lend, sell, redistribute or sublicense the App; remove notices of ownership; use the App to build a competing product; or use bots, scripts or modified versions of the App.',
        ]),
        ('3. Ownership', [
            'The App, its puzzles, clues, pictures, sounds and code are licensed, not sold. Licensor and its licensors keep all rights not expressly granted. Picture clues use Noto Emoji under the Apache License 2.0; the fonts are used under the SIL Open Font License.',
        ]),
        ('4. In-app purchases and virtual items', [
            'Coins and other virtual items are licensed for use in the App only, have no cash value and are not your property. They are governed by the Terms of Service.',
        ]),
        ('5. Updates and data', [
            'Licensor may provide updates, which may be required to keep using the App. The App connects to Licensor’s servers to save progress, show leaderboards and check purchases. How your data is handled is described in the Privacy Policy.',
        ]),
        ('6. Acknowledgement', [
            'You and Licensor acknowledge that this Agreement is concluded between you and Licensor only, and not with Apple Inc. or Google LLC. Licensor, not Apple or Google, is solely responsible for the App and its content.',
        ]),
        ('7. Maintenance and support', [
            'Licensor is solely responsible for any maintenance and support of the App, as described in this Agreement or required by law. Apple and Google have no obligation whatsoever to provide maintenance or support for the App. For support, contact {email}.',
        ]),
        ('8. Warranty', [
            'To the extent the law allows, the App is provided “as is” and without warranties of any kind. If the App fails to conform to any warranty that applies by law, you may notify Apple, and Apple will refund the purchase price of the App to you, if any. To the maximum extent permitted by law, Apple has no other warranty obligation whatsoever with respect to the App, and any other claims, losses, liabilities, damages, costs or expenses attributable to any failure to conform to any warranty are Licensor’s responsibility, as far as the law places them on Licensor.',
        ]),
        ('9. Product claims', [
            'Licensor, not Apple or Google, is responsible for addressing any claims by you or any third party relating to the App or your possession and use of it, including product liability claims, claims that the App fails to conform to any applicable legal or regulatory requirement, and claims arising under consumer protection, privacy or similar laws.',
        ]),
        ('10. Intellectual property claims', [
            'If a third party claims that the App or your possession and use of it infringes that party’s intellectual property rights, Licensor, not Apple or Google, is solely responsible for the investigation, defense, settlement and discharge of that claim.',
        ]),
        ('11. Legal compliance', [
            'You represent and warrant that you are not located in a country that is subject to a U.S. Government embargo, or that has been designated by the U.S. Government as a “terrorist supporting” country, and that you are not listed on any U.S. Government list of prohibited or restricted parties.',
        ]),
        ('12. Third-party terms', [
            'You must comply with applicable third-party terms when using the App, such as the terms of your mobile network, the App Store and Google Play.',
        ]),
        ('13. Third-party beneficiary', [
            'You and Licensor acknowledge and agree that Apple, and Apple’s subsidiaries, are third-party beneficiaries of this Agreement, and that, upon your acceptance of this Agreement, Apple will have the right (and will be deemed to have accepted the right) to enforce this Agreement against you as a third-party beneficiary.',
        ]),
        ('14. Limitation of liability', [
            'To the extent the law allows, Licensor is not liable for indirect, incidental or consequential damages arising from the use of, or inability to use, the App, and its total liability is limited to the amount you paid for the App and in-app purchases in the 12 months before the claim. Mandatory consumer rights are not affected.',
        ]),
        ('15. Termination', [
            'This Agreement applies until ended by you or Licensor. It ends automatically if you break it. You can end it by deleting the App and your account. On termination you must stop using the App.',
        ]),
        ('16. Law', [
            'This Agreement is governed by the same law as the Terms of Service, without taking away the protection of mandatory consumer laws of the country where you live.',
        ]),
        ('17. Contact', ['{operator}, {email}']),
    ],
}

CSS = """:root{--sky:#2D7BF0;--outline:#1B3F8A;--panel:#FFF7E8;--panel-ink:#7A4A1E;--ink:#1d2433;--muted:#5b647a;--line:#E2C9A0;
--display:'Nunito','Arial Rounded MT Bold',system-ui,sans-serif;--body:'Jost','Avenir Next','Segoe UI',system-ui,sans-serif;color-scheme:light}
@font-face{font-family:'Nunito';src:url('/assets/fonts/Nunito-Variable.ttf') format('truetype');font-weight:200 1000;font-display:swap}
@font-face{font-family:'Jost';src:url('/assets/fonts/Jost-Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:'Jost';src:url('/assets/fonts/Jost-Medium.ttf') format('truetype');font-weight:500;font-display:swap}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#2D7BF0,#6CC3FF) fixed;color:var(--ink);font:500 17px/1.65 var(--body)}
a{color:#1F5FCC}a:focus-visible{outline:3px solid #FFC83D;outline-offset:2px;border-radius:4px}
.bar{display:flex;align-items:center;gap:16px;padding:10px max(16px,calc((100% - 860px)/2));background:rgba(31,95,204,.9)}
.bar a.brand{display:flex;align-items:center;gap:8px;color:#fff;text-decoration:none;font:900 21px/1 var(--display)}.bar img{width:44px}
.bar nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}.bar nav a{color:#fff;font:800 14px/1 var(--display);text-decoration:none}
.bar nav a[aria-current]{text-decoration:underline;text-underline-offset:5px}
main{max-width:860px;margin:28px auto 48px;padding:32px clamp(18px,4vw,48px);background:var(--panel);border-radius:28px;box-shadow:0 0 0 6px rgba(45,123,240,.9),0 10px 0 6px #1F5FCC;width:calc(100% - 32px)}
h1{font:900 clamp(28px,4.5vw,40px)/1.15 var(--display);color:#fff;-webkit-text-stroke:.14em var(--outline);paint-order:stroke fill;text-shadow:0 .08em 0 var(--outline);margin:0 0 14px;text-wrap:balance}
h2{font:900 20px/1.3 var(--display);color:var(--panel-ink);margin:28px 0 6px}p{margin:8px 0;max-width:70ch}
.langs{font:700 14px/1 var(--display);color:var(--muted);margin-bottom:14px;display:flex;gap:12px;flex-wrap:wrap}.langs b{color:var(--outline)}
.intro{font-size:18px}footer{text-align:center;color:#fff;padding:0 16px 36px;font-size:14px}footer a{color:#fff}"""


def page(title, lang, body, nav_current, langs_html=''):
    current = ' aria-current="page"'
    nav = ''.join(
        f'<a href="{href}"{current if key == nav_current else ""}>{label}</a>'
        for key, href, label in [('privacy', '/privacy/', 'Privacy'), ('terms', '/terms/', 'Terms'), ('eula', '/eula/', 'EULA')]
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ClueGrid · {html.escape(title)}</title>
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="stylesheet" href="/legal.css">
</head>
<body>
<header class="bar"><a class="brand" href="/"><img src="/assets/logo.webp" alt="" width="44" height="37">ClueGrid</a><nav aria-label="Legal">{nav}</nav></header>
<main>
{langs_html}<h1>{html.escape(title)}</h1>
{body}
</main>
<footer><a href="/">playcluegrid.app</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</body>
</html>
"""


def render(doc, fill):
    out = [f'<p class="intro">{fill(doc["intro"])}</p>']
    for heading, paras in doc['sections']:
        out.append(f'<h2>{html.escape(heading)}</h2>')
        out.extend(f'<p>{fill(p)}</p>' for p in paras)
    return '\n'.join(out)


def filler(lang):
    def fill(text):
        s = html.escape(text, quote=False)
        operator = html.escape(OPERATOR[lang])
        s = s.replace('{controller}', operator).replace('{operator}', operator)
        s = s.replace('{date}', html.escape(UPDATED[lang]))
        return s.replace('{email}', f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return fill


def write(rel, content):
    path = ROOT / rel / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print('wrote', path.relative_to(ROOT))


def main():
    (ROOT / 'legal.css').write_text(CSS + '\n', encoding='utf-8')
    privacy = json.loads((ROOT / 'scripts' / 'privacy.json').read_text(encoding='utf-8'))
    for code, text in privacy.items():
        links = ' '.join(
            f'<b>{LANG_NAMES[c]}</b>' if c == code else f'<a href="/privacy/{"" if c == "en" else c + "/"}">{LANG_NAMES[c]}</a>'
            for c in privacy
        )
        body = render(text, filler(code))
        write('privacy' if code == 'en' else f'privacy/{code}', page(text['title'], code, body, 'privacy', f'<div class="langs">{links}</div>\n'))
    write('terms', page(TERMS['title'], 'en', render(TERMS, filler('en')), 'terms'))
    write('eula', page(EULA['title'], 'en', render(EULA, filler('en')), 'eula'))


if __name__ == '__main__':
    main()
