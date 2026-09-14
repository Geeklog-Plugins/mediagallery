from pathlib import Path

# Fix the mini-lightbox HTML emitted by classMedia.php. The affected PHP
# fragments are single-quoted strings, so \" was emitted literally into HTML.
path = Path('include/classMedia.php')
lines = path.read_text(encoding='utf-8').splitlines(True)
changed = 0
fixed = []
for line in lines:
    if 'mg-card-preview' in line and '\\"' in line:
        line = line.replace('\\"', '"')
        changed += 1
    fixed.append(line)
if changed < 4:
    raise SystemExit('Expected broken mini-lightbox quote sequences not found')
path.write_text(''.join(fixed), encoding='utf-8')

# audio-player.js was a Flash-era helper removed from 1.8, but seven templates
# still referenced it and generated a 404 on every affected public page.
script = '<script type="text/javascript" src="{site_url}/players/audio-player.js"></script>\n'
templates = [
    Path('templates/album_page.thtml'),
    Path('templates/search_page.thtml'),
    Path('templates/themes/filelist/album_page.thtml'),
    Path('templates/themes/simpleviewer/album_page.thtml'),
    Path('templates/themes/jquery_colorbox/album_page.thtml'),
    Path('templates/themes/jquery_ad-gallery/album_page.thtml'),
    Path('templates/themes/podcast/album_page.thtml'),
]
removed = 0
for tpl in templates:
    text = tpl.read_text(encoding='utf-8')
    if script in text:
        text = text.replace(script, '', 1)
        tpl.write_text(text, encoding='utf-8')
        removed += 1
if removed != len(templates):
    raise SystemExit('Expected audio-player.js include missing from one or more templates')
