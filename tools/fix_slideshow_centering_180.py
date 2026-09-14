from pathlib import Path

path = Path('public_html/style.css')
text = path.read_text(encoding='utf-8')
old = """.mg-slideshow-stage {\n  overflow: hidden;\n}\n.mg-slideshow-image {\n  width: calc(100vw - 2rem);\n  height: calc(100vh - 2rem);\n  max-width: none;\n  max-height: none;\n  object-fit: contain;\n  object-position: center center;\n}\n\n@media (max-width: 42rem) {\n  .mg-slideshow-image {\n    width: calc(100vw - 1rem);\n    height: calc(100vh - 1rem);\n  }\n}\n"""
new = """.mg-slideshow-stage {\n  box-sizing: border-box;\n  overflow: hidden;\n}\n.mg-slideshow-image {\n  width: 100%;\n  height: 100%;\n  max-width: 100%;\n  max-height: 100%;\n  margin: 0;\n  object-fit: contain;\n  object-position: center center;\n}\n"""
if old not in text:
    raise SystemExit('Expected immersive slideshow scaling block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
