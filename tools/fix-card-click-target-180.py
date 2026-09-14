from pathlib import Path

css = Path('public_html/style.css')
text = css.read_text(encoding='utf-8')
block = '''\n\n/* MediaGallery 1.8 reliable card click target */\n.mg-album-default-grid .mg-card-media {\n  position: relative;\n}\n.mg-album-default-grid .mg-card-image-link,\n.mg-album-default-grid .mg_thumbnail_wrapper > a {\n  position: relative;\n  z-index: 2;\n  display: block;\n  width: 100%;\n  height: 100%;\n  cursor: pointer;\n  pointer-events: auto;\n}\n.mg-album-default-grid .mg-card-preview-stack,\n.mg-album-default-grid .mg-card-preview-image {\n  pointer-events: none;\n}\n'''
if 'MediaGallery 1.8 reliable card click target' not in text:
    text += block
css.write_text(text, encoding='utf-8')

workflow = Path('.github/workflows/build-dist.yml')
w = workflow.read_text(encoding='utf-8')
needle = """          ! unzip -Z1 \"dist/${ARCHIVE}\" | grep -q '^mediagallery/.gitignore$'\n\n          unzip -p \"dist/${ARCHIVE}\" mediagallery/include/config_180.php \\\n"""
replacement = """          ! unzip -Z1 \"dist/${ARCHIVE}\" | grep -q '^mediagallery/.gitignore$'\n\n          if unzip -Z1 \"dist/${ARCHIVE}\" | grep -E '\\.thtml$' | while read -r template; do unzip -p \"dist/${ARCHIVE}\" \"$template\"; done | grep -q 'audio-player\\.js'; then\n            echo 'Archive still contains a stale audio-player.js template reference' >&2\n            exit 1\n          fi\n\n          unzip -p \"dist/${ARCHIVE}\" mediagallery/include/config_180.php \\\n"""
if needle not in w:
    raise SystemExit('Expected archive verification insertion point not found')
w = w.replace(needle, replacement, 1)
workflow.write_text(w, encoding='utf-8')
