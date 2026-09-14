from pathlib import Path

# The mini-lightbox originally used absolutely positioned images. That removes
# them from normal layout and can collapse the percentage-height link/stack to
# zero. Use a square CSS Grid stack instead: both images occupy the same cell,
# while the stack itself keeps a real aspect-ratio and clickable area.
css_path = Path('public_html/style.css')
css = css_path.read_text(encoding='utf-8')
old_stack = '''.mg-album-default-grid .mg-card-square .mg-card-preview-stack {
  position: relative;
  overflow: hidden;
  border-radius: .45rem;
  background: rgba(127,127,127,.055);
}
'''
new_stack = '''.mg-album-default-grid .mg-card-square .mg-card-preview-stack {
  position: relative;
  display: grid;
  width: 100%;
  height: auto;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: .45rem;
  background: rgba(127,127,127,.055);
}
'''
old_img = '''.mg-album-default-grid .mg-card-square .mg-card-preview-image {
  position: absolute;
  inset: 0;
  display: block;
'''
new_img = '''.mg-album-default-grid .mg-card-square .mg-card-preview-image {
  position: relative;
  inset: auto;
  grid-area: 1 / 1;
  display: block;
'''
if old_stack not in css or old_img not in css:
    raise SystemExit('Expected mini-lightbox CSS block not found')
css = css.replace(old_stack, new_stack, 1).replace(old_img, new_img, 1)
css_path.write_text(css, encoding='utf-8')

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
