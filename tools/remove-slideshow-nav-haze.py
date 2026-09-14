from pathlib import Path
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 clean slideshow navigation */'
if marker not in s:
    s += '''\n\n/* MediaGallery 1.8 clean slideshow navigation */\n.mg-slideshow-prev,\n.mg-slideshow-next {\n  background: transparent;\n}\n.mg-slideshow-nav {\n  backdrop-filter: none;\n  -webkit-backdrop-filter: none;\n  box-shadow: none;\n}\n.mg-slideshow-nav:hover,\n.mg-slideshow-nav:focus-visible {\n  background: rgba(255,255,255,.08);\n}\n'''
p.write_text(s, encoding='utf-8')
