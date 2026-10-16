"""Encon site builder: wraps src/*.html bodies with shared head/header/footer -> site/*.html.
Run:  python build.py
Each src page starts with a comment holding one `key: value` per line (title, desc).
Placeholders inside bodies: <!-- @projects -->, <!-- @clients -->, <!-- @cta -->
"""
import re, pathlib, html

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / 'src', ROOT / 'site'
DOMAIN = 'https://www.enconengineeringsolutions.com'
PHONE1, PHONE1_T = '+91 94481 11405', '+919448111405'
PHONE2, PHONE2_T = '+91 98862 55888', '+919886255888'
PHONE3, PHONE3_T = '+91 91485 20004', '+919148520004'
EMAIL1, EMAIL2 = 'encon417@gmail.com', 'adenpro4563@gmail.com'
ADDR = 'No. 315, Anantha Shukapuri, Ground Floor, 14th Cross, 7th Main, Vyalikaval, Malleshwaram, Bengaluru 560003'
MAPS = 'https://www.google.com/maps?q=13.004465103149414,77.57625579833984&z=17&hl=en'

I = lambda name, cls='icon': f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

ICONS = {
 'phone':'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 'pin':'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 'clock':'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'down':'<path d="m6 9 6 6 6-6"/>','left':'<path d="m15 18-6-6 6-6"/>','right':'<path d="m9 18 6-6-6-6"/>','up':'<path d="m18 15-6-6-6 6"/>',
 'x':'<path d="M18 6 6 18M6 6l12 12"/>','check':'<path d="M20 6 9 17l-5-5"/>',
 'drop':'<path d="M12 2.7s-6.5 7.1-6.5 11.8a6.5 6.5 0 0 0 13 0C18.5 9.8 12 2.7 12 2.7z"/>',
 'droplets':'<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
 'recycle':'<path d="M7 19H4.82a1.83 1.83 0 0 1-1.57-.88 1.79 1.79 0 0 1 0-1.78L7.2 9.5"/><path d="M11 19h8.2a1.83 1.83 0 0 0 1.56-.89 1.78 1.78 0 0 0 0-1.78l-1.23-2.12"/><path d="m14 16-3 3 3 3"/><path d="M8.29 13.6 7.2 9.5 3.1 10.6"/><path d="m9.34 5.81 1.1-1.89A1.83 1.83 0 0 1 11.99 3a1.78 1.78 0 0 1 1.54.89l3.94 6.84"/><path d="m13.38 9.63 4.1 1.1 1.1-4.1"/>',
 'factory':'<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
 'filter':'<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
 'building':'<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
 'box':'<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
 'ruler':'<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
 'wrench':'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 'truck':'<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2M15 18H9M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 'hardhat':'<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5M4 15v-3a6 6 0 0 1 6-6M14 6a6 6 0 0 1 6 6v3"/>',
 'power':'<path d="M12 2v10"/><path d="M18.4 6.6a9 9 0 1 1-12.77.04"/>',
 'search':'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 'target':'<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 'flag':'<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7"/>',
 'shield':'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 'users':'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 'award':'<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
 'gauge':'<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
 'layers':'<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65M22 12.65l-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 'briefcase':'<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 'flask':'<path d="M9 3h6M10 9V3M14 9V3"/><path d="M10 9 4.5 19a1.5 1.5 0 0 0 1.3 2.2h12.4a1.5 1.5 0 0 0 1.3-2.2L14 9"/><path d="M7 15h10"/>',
 'shirt':'<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>',
 'wheat':'<path d="M2 22 16 8M3.47 12.53 5 11l1.53 1.53a3.5 3.5 0 0 1 0 4.94L5 19l-1.53-1.53a3.5 3.5 0 0 1 0-4.94ZM7.47 8.53 9 7l1.53 1.53a3.5 3.5 0 0 1 0 4.94L9 15l-1.53-1.53a3.5 3.5 0 0 1 0-4.94ZM11.47 4.53 13 3l1.53 1.53a3.5 3.5 0 0 1 0 4.94L13 11l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M20 2h2v2a4 4 0 0 1-4 4h-2V6a4 4 0 0 1 4-4Z"/>',
 'utensils':'<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
 'car':'<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 'cpu':'<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
 'wine':'<path d="M8 22h8M7 10h10M12 15v7M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/>',
 'zap':'<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 'wind':'<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
 'quote':'<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.76-2.02-2-2H4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 0-1 1.03V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.76-2.02-2-2h-4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>',
 'star':'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
 'download':'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
 'home':'<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 'umbrella':'<path d="M22 12a10 10 0 0 0-20 0Z"/><path d="M12 12v8a2 2 0 0 0 4 0M12 2v1"/>',
 'hammer':'<path d="m15 12-8.37 8.37a1 1 0 1 1-3-3L12 9M18 15l4-4M21.5 11.5l-1.91-1.91A2 2 0 0 1 19 8.17V7l-2.26-2.26a6 6 0 0 0-4.2-1.76L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.17a2 2 0 0 1 1.41.59L18.5 14.5"/>',
 'file':'<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>',
 'bulb':'<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5M9 18h6M10 22h4"/>',
 'leaf':'<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
 'coins':'<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18M7 6h1v4M16.71 13.88l.7.71-2.82 2.82"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + ''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + '</svg>'
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.05 21.5a9.4 9.4 0 0 1-4.8-1.31l-.34-.2-3.57.93.95-3.48-.22-.36a9.4 9.4 0 0 1-1.45-5.02c0-5.2 4.24-9.44 9.45-9.44a9.4 9.4 0 0 1 9.44 9.45c0 5.21-4.24 9.44-9.45 9.44zm8.03-17.47A11.3 11.3 0 0 0 12.05.7C5.8.7.72 5.78.72 12.03c0 2 .52 3.95 1.52 5.66L.62 23.7l6.15-1.61a11.3 11.3 0 0 0 5.27 1.34c6.25 0 11.33-5.08 11.33-11.33 0-3.03-1.18-5.87-3.32-8.01z"/></svg>'

SERVICES = [  # (anchor, icon, label)
 ('design','ruler','Design & Detailed Engineering'),
 ('wtp','droplets','Water Treatment Plants'), ('stp','recycle','Sewage Treatment & Recycle'),
 ('etp','factory','Effluent Treatment, Recycle & ZLD'), ('uf-ro','filter','UF & RO Systems'),
 ('prefab','box','Prefabricated Plants'), ('johkasou','home','Johkasou Packaged STPs'),
 ('clarification','layers','Clarifiers & Filters'), ('aeration','wind','Aeration Systems'),
 ('chemicals','flask','Chemical Treatment Program'), ('civil','building','Civil & Structural Works'),
 ('om','wrench','Augmentation, O&M & Consultancy'),
]
NAV = [('index.html','Home'),('about.html','About'),('services.html','Services'),('projects.html','Projects'),('contact.html','Contact')]

def header(page):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ''
        if href == 'services.html':
            drop = ''.join(f'<li><a href="services.html#{a}">{I(ic)}{l}</a></li>' for a, ic, l in SERVICES)
            items.append(f'<li class="has-drop"><a href="{href}"{cur}>{label}{I("down","icon caret")}</a><ul class="dropdown">{drop}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
<div class="topbar">
  <div class="wrap">
    <ul>
      <li>{I('phone')}<a href="tel:{PHONE1_T}">{PHONE1}</a></li>
      <li class="hide-xs">{I('mail')}<a href="mailto:{EMAIL1}">{EMAIL1}</a></li>
      <li class="hide-sm">{I('pin')}Malleshwaram, Bengaluru</li>
    </ul>
    <ul class="hide-sm"><li>{I('clock')}Mon – Sat: 9:30 AM – 6:30 PM</li></ul>
  </div>
</div>
<header class="header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Encon Engineering Solutions home">
      <img src="assets/img/logo-emblem.png" alt="" width="221" height="171">
      <span class="brand-text"><b>ENCON</b><small>Engineering Solutions</small></span>
    </a>
    <nav class="nav" aria-label="Main">
      <ul>{''.join(items)}</ul>
      <a class="btn btn-primary header-cta" href="contact.html#enquiry">Get a Quote {I('arrow')}</a>
    </nav>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span></button>
  </div>
</header>'''

def footer():
    svc = ''.join(f'<li><a href="services.html#{a}">{I("right")}{l}</a></li>' for a, _, l in SERVICES[:7])
    return f'''<footer class="footer">
  <div class="wave-top"><svg viewBox="0 0 1440 60" preserveAspectRatio="none"><path fill="#fff" d="M0,0H1440V22C1200,58 960,6 720,30C480,54 240,8 0,32Z"/></svg></div>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/logo-emblem.png" alt="" width="221" height="171"><span class="brand-text"><b>ENCON</b><small>Engineering Solutions</small></span></a>
        <p>An experienced turnkey solution provider for water, sewage and wastewater treatment &amp; recycle systems including ZLD. Project execution by Encon, with consultancy by our sister wing, ADENPRO Environmental Consultants.</p>
        <a class="btn btn-aqua" style="margin-top:24px" href="assets/docs/encon-company-profile.pdf" download>{I('download')} Company Profile</a>
      </div>
      <div><h4>Quick Links</h4><ul class="foot-links">{''.join(f'<li><a href="{h}">{I("right")}{l}</a></li>' for h, l in NAV)}<li><a href="contact.html#enquiry">{I("right")}Request a Quote</a></li></ul></div>
      <div><h4>Our Services</h4><ul class="foot-links">{svc}</ul></div>
      <div><h4>Get in Touch</h4>
        <ul class="foot-contact">
          <li>{I('pin')}<a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a></li>
          <li>{I('phone')}<span><a href="tel:{PHONE1_T}">{PHONE1}</a><br><a href="tel:{PHONE2_T}">{PHONE2}</a><br><a href="tel:{PHONE3_T}">{PHONE3}</a></span></li>
          <li>{I('mail')}<span><a href="mailto:{EMAIL1}">{EMAIL1}</a><br><a href="mailto:{EMAIL2}">{EMAIL2}</a></span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <span>&copy; <span data-year>2026</span> Encon Engineering Solutions, Bengaluru. All rights reserved.</span>
    <span>Water &middot; Wastewater &middot; Recycle &middot; Civil</span>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{PHONE1_T[1:]}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}</a>
<button class="to-top" aria-label="Back to top">{I('up')}</button>'''

CTA = f'''<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta reveal">
      <img src="assets/img/cta-water.webp" alt="" loading="lazy">
      <div>
        <h2>Planning an STP, ETP or water project?</h2>
        <p>Share your flow rate, site and discharge norms. Our engineers will come back with a practical, economical scheme.</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-aqua" href="contact.html#enquiry">Request a Quote {I('arrow')}</a>
        <a class="btn btn-ghost" href="tel:{PHONE1_T}">{I('phone')} {PHONE1}</a>
      </div>
    </div>
  </div>
</section>'''

# Customer list from the client's company profile (8.9.25), plus project-list clients without a logo file
LOGOS = [('bial','Bengaluru International Airport'),('tata-projects','Tata Projects'),('tata-electronics','Tata Electronics'),
         ('mhi','Mitsubishi Heavy Industries'),('itc','ITC Limited'),('parle','Parle'),('nalco','NALCO, an Ecolab company'),
         ('sobha','Sobha'),('hiranandani','House of Hiranandani'),('ncc','NCC'),('salarpuria-sattva','Salarpuria Sattva'),
         ('bagmane','Bagmane'),('raymond','Raymond'),('himatsingka','Himatsingka'),('plansee','Plansee'),('solenis','Solenis'),
         ('id','Indian Design Exports'),('filtrex','Filtrex Technologies'),('cwd','Clear Water Dynamics'),('eit','EIT'),
         ('manipal','Manipal Global'),('narayana','The Narayana Group'),('elixer','Elixer'),('century-club','Century Club')]
WORDS = ['Thermax','CIPLA','Murugappa Water Technology','Gradient India','Dakshina Pinakini']
def clients():
    tiles = ''.join(f'<div class="logo-tile"><img src="assets/img/clients/{f}.webp" alt="{n}" loading="lazy"></div>' for f, n in LOGOS)
    tiles += ''.join(f'<div class="logo-tile word">{html.escape(w)}</div>' for w in WORDS)
    return f'''<section class="clients" aria-labelledby="clients-h">
  <h2 id="clients-h">Trusted by <b>leading industries, institutions &amp; infrastructure</b> across India</h2>
  <div class="marquee"><div class="marquee-track">{tiles}<span aria-hidden="true" style="display:contents">{tiles.replace('alt="', 'alt="" data-alt="')}</span></div></div>
</section>'''

# From "List of completed & Ongoing Projects Encon.docx" (client, type, description, year, filter cats)
PROJECTS = [
 ('Silver Spark – A Raymond Initiative','Civil works','Dismantling &amp; concrete works','2020','civil'),
 ('Silver Spark – A Raymond Initiative','Civil works','Providing and fixing ceramic wall tiles','2020','civil'),
 ('Milan Clothing','STP','SITC of 20 KLD Daiki Axis packaged STP','2020','stp'),
 ('Himatsingka Linens','ETP','SITC of diffused aeration system for biological treatment section','2021','etp'),
 ('Himatsingka Linens','ETP','Installation work for homogenization tank','2021','etp'),
 ('Indian Design Exports Pvt. Ltd.','STP','SITC of STP for IDEPL (Unit 5), 5 KLD','2021','stp'),
 ('Himatsingka Linens','ETP','Electro-mechanical installation — SITC of oxidation tank (biological treatment)','2021','etp'),
 ('Himatsingka Linens','ETP','Supply &amp; installation of fittings','2021','etp'),
 ('Himatsingka Linens','ETP','SITC of disc diffusers — SSI make EPDM 9 inch','2021','etp'),
 ('Himatsingka Linens','STP · Civil','MBR tank civil works','2021','stp civil'),
 ('Himatsingka Linens','ETP','Installation &amp; commissioning of oxidation tank 2','2021','etp'),
 ('Himatsingka Linens','ETP · Civil','Construction of ETP tank works','2021','etp civil'),
 ('Himatsingka Linens','ETP','SITC of tube packs — media for settler','2021','etp'),
 ('Himatsingka Linens','STP · Civil','Construction of foundation for equipment','2021','stp civil'),
 ('Himatsingka Linens','STP · Civil','Construction of RCC tanks','2022','stp civil'),
 ('Gradient India Pvt. Ltd.','Civil works','Construction of compound wall &amp; drain network revamping','2022','civil'),
 ('Silver Spark – A Raymond Initiative','STP','SITC of filter media','2022','stp'),
 ('Gradient India Pvt. Ltd.','CETP · Civil','Plumbing &amp; civil works','2022','etp civil'),
 ('Silver Spark – A Raymond Initiative','STP','SITC of diffusers','2022','stp'),
 ('Murugappa Water Technology &amp; Solutions','ETP','Installation &amp; commissioning','2022','etp'),
 ('Gradient India Pvt. Ltd.','Civil works','Civil works','2022','civil'),
 ('Himatsingka Linens','STP','SITC of electro-mechanical equipment','2022','stp'),
 ('Gradient India Pvt. Ltd.','CETP · Civil','Sludge removal in all tanks','2022','etp civil'),
 ('Gradient India Pvt. Ltd.','CETP · Civil','Civil works','2022','etp civil'),
 ('NJK Enterprises, Unit I','STP','SITC of 20 KLD Daiki Axis prefabricated STP with civil works','2022','stp'),
 ('Ballari Municipal Corporation','WTP','Preparation &amp; submission of DPR for 15 MLD water treatment plant','2022','wtp consult'),
 ('Ballari Water Treatment Plant (Govt.)','WTP','15 MLD water treatment plant: process design &amp; flow scheme','Ongoing','wtp consult ongoing'),
 ('Raichur Water Supply Scheme (Govt.)','WTP','Preliminary design engineering at tendering stage: drinking water to 1,406 rural habitations &amp; treated bulk water to 7 urban local bodies','Ongoing','wtp consult ongoing'),
 ('NJK Enterprises, Unit II','STP','SITC of 20 KLD Daiki Axis prefabricated STP with civil works','2023','stp'),
 ('Century Club','STP','SITC of 50 KLD Daiki Axis prefabricated STP with civil works','2023','stp'),
 ('Filtrex Technologies Pvt. Ltd.','CETP','Construction of civil tanks &amp; SITC of electro-mechanical equipment','2023','etp civil'),
 ('Bangalore International Airport Ltd.','STP','Augmentation and refurbishment of 1.5 MLD STP','2024','stp'),
 ('Thermax Ltd.','STP','Installation &amp; commissioning of STP','2024','stp'),
 ('Bangalore International Airport Ltd.','WTP','Design consultancy for 5 MLD water pumping system','2024','wtp consult'),
 ('Plansee High Performance India Ltd.','CETP','DSITC of 75 KLD CETP','2025','etp'),
 ('Bangalore International Airport Ltd.','STP','Augmentation and refurbishment of 1.0 MLD STP','2025','stp'),
 ('Seshadri Developers','STP','SITC of 150 KLD Daiki Axis prefabricated STP','2025','stp'),
 ('Indian Design Exports Pvt. Ltd. — Unit 9','STP','DSITC of 80 KLD STP','2025','stp'),
 ('Mitsubishi Heavy Industries VST Diesel Engines','STP · ETP','DSITC of 40 KLD STP &amp; 10 KLD ETP','Ongoing','stp etp ongoing'),
 ('Food Creations Pvt. Ltd. (ITC)','ETP','Augmentation of 120 KLD ETP','Ongoing','etp ongoing'),
 ('Indian Design Exports Pvt. Ltd. — Unit 9','STP','DSITC of 200 KLD STP','Ongoing','stp ongoing'),
 ('Indian Design Exports Pvt. Ltd. — Unit 12','STP','DSITC of 100 KLD STP','Ongoing','stp ongoing'),
 ('Bangalore International Airport Ltd.','STP · O&amp;M','Operation &amp; maintenance of STP','Ongoing','stp ongoing'),
 ('Parle Group','ETP','Design &amp; detailed engineering of ETPs for sugar, distillery, biscuit &amp; confectionery units across India (Chittoor, Pant Nagar, Kaiser Ganj, etc.)','Ongoing','etp consult ongoing'),
 ('Tata Electronics — Hosur','WTP','Consultation / technical services for preparing BOQ for WTP','Ongoing','wtp consult ongoing'),
 ('Tata Electronics — Narasapura','Total water mgmt.','Process management consultancy for entire total water management','Ongoing','wtp consult ongoing'),
 ('CIPLA','ETP','ETP assessment study','Ongoing','etp consult ongoing'),
]
def projects_table():
    rows = []
    for c, t, d, y, cat in sorted(PROJECTS, key=lambda p: ('0' if p[3] == 'Ongoing' else '1' + str(9999 - int(p[3])))):
        st = '<span class="status live">Ongoing</span>' if y == 'Ongoing' else f'<span class="status done">{y}</span>'
        rows.append(f'<tr data-cat="{cat} {"" if y == "Ongoing" else "done"}"><td>{c}</td><td><span class="type">{t}</span></td><td>{d}</td><td>{st}</td></tr>')
    return '\n'.join(rows)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{domain}/assets/img/hero-campus.webp">
<meta name="theme-color" content="#0a2540">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
<script>document.documentElement.classList.add('js')</script>
{extra}
</head>
<body>
'''
SCHEMA = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Encon Engineering Solutions","description":"Turnkey water, sewage and wastewater treatment & recycle systems, and civil & structural works.","url":"{DOMAIN}/","telephone":"{PHONE1_T}","email":"{EMAIL1}","image":"{DOMAIN}/assets/img/hero-campus.webp","address":{{"@type":"PostalAddress","streetAddress":"#315, Anantha Shukapuri, 7th Main Road, 14th Cross, Vyalikaval, Malleshwaram","addressLocality":"Bengaluru","addressRegion":"Karnataka","postalCode":"560003","addressCountry":"IN"}},"geo":{{"@type":"GeoCoordinates","latitude":13.004465,"longitude":77.576256}},"areaServed":"IN"}}</script>'''

def build():
    pages = []
    for f in sorted(SRC.glob('*.html')):
        raw = f.read_text(encoding='utf-8')
        meta = dict(l.split(':', 1) for l in re.match(r'<!--(.*?)-->', raw, re.S).group(1).strip().splitlines())
        meta = {k.strip(): html.escape(v.strip()) for k, v in meta.items()}
        body = raw.split('-->', 1)[1]
        body = (body.replace('<!-- @projects -->', projects_table()).replace('<!-- @clients -->', clients())
                    .replace('<!-- @cta -->', CTA).replace('{PHONE1}', PHONE1).replace('{PHONE1_T}', PHONE1_T)
                    .replace('{PHONE2}', PHONE2).replace('{PHONE2_T}', PHONE2_T)
                    .replace('{PHONE3}', PHONE3).replace('{PHONE3_T}', PHONE3_T).replace('{EMAIL1}', EMAIL1)
                    .replace('{EMAIL2}', EMAIL2).replace('{ADDR}', ADDR).replace('{MAPS}', MAPS)
                    .replace('{WA}', WA_SVG).replace('{PROJECT_COUNT}', str(len(PROJECTS))))
        body = re.sub(r'\{I:([a-z-]+)\}', lambda m: I(m.group(1)), body)
        url = DOMAIN + '/' + ('' if f.name == 'index.html' else f.name)
        out = HEAD.format(title=meta['title'], desc=meta['desc'], url=url, domain=DOMAIN,
                          extra=SCHEMA if f.name in ('index.html', 'contact.html') else '')
        out += header(f.name) + '\n<main id="main">' + body + '</main>\n' + footer() + '\n<script src="assets/js/main.js" defer></script>\n</body>\n</html>\n'
        (OUT / f.name).write_text(out, encoding='utf-8')
        if f.name != '404.html': pages.append(url)
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in pages) + '</urlset>\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n', encoding='utf-8')
    print('built', len(pages) + 1, 'pages;', len(PROJECTS), 'projects')

if __name__ == '__main__':
    build()
