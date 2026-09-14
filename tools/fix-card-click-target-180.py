from pathlib import Path

css = Path('public_html/style.css')
text = css.read_text(encoding='utf-8')
block = '''\n\n/* MediaGallery 1.8 reliable card click target */\n.mg-album-default-grid .mg-card-media {\n  position: relative;\n}\n.mg-album-default-grid .mg-card-image-link,\n.mg-album-default-grid .mg_thumbnail_wrapper > a {\n  position: relative;\n  z-index: 2;\n  display: block;\n  width: 100%;\n  height: 100%;\n  cursor: pointer;\n  pointer-events: auto;\n}\n.mg-album-default-grid .mg-card-preview-stack,\n.mg-album-default-grid .mg-card-preview-image {\n  pointer-events: none;\n}\n'''
if 'MediaGallery 1.8 reliable card click target' not in text:
    text += block
css.write_text(text, encoding='utf-8')
