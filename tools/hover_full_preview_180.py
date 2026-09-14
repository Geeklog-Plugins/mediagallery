from pathlib import Path
import re

# classMedia.php contains historical latin-1 bytes.
p = Path('include/classMedia.php')
s = p.read_text(encoding='latin-1')
pattern = re.compile(r"\n        // MediaGallery 1\.8 default album cards use a square crop.*?\n        if \(\$mode == 1\) \{", re.S)
replacement = r'''\n        // MediaGallery 1.8: default album cards use the full display preview.\n        // CSS crops it to a square at rest and reveals the complete image on hover/focus.\n        $media_card_preview = $media_item_thumbnail;\n        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {\n            $media_card_preview = $media_start_link\n                . '<img class="mg-card-preview-image" src="' . MG_escapeHTML($direct_url)\n                . '" alt="' . $caption . '" loading="lazy" decoding="async">'\n                . '</a>';\n        }\n\n        if ($mode == 1) {'''
s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('classMedia preview block not found')
p.write_text(s2, encoding='latin-1')

# common.php: keep the larger display derivative; remove the native square override
# so hover/focus can reveal the whole cover.
p = Path('include/common.php')
s = p.read_text(encoding='latin-1')
pattern = re.compile(r"\n    // MediaGallery 1\.8: album cards use a square cover\..*?\n    \$children = MG_getAlbumChildren\(\$album_id\);", re.S)
replacement = "\n\n    // Keep the complete display cover; CSS handles square cropping non-destructively.\n    $children = MG_getAlbumChildren($album_id);"
s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('common.php square cover override not found')
p.write_text(s2, encoding='latin-1')

# Root/sub-album cards: bypass the legacy framed-image markup and use the same
# direct-image structure as media cards.
p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
old = '<div class="mg_thumbnail_wrapper">{media_item_thumbnail}</div>'
new = '<div class="mg_thumbnail_wrapper"><a class="mg-card-image-link" href="{u_viewalbum}"><img class="mg-card-preview-image" src="{album_last_image}" alt="{album_title}" loading="lazy" decoding="async"></a></div>'
if old not in s:
    raise SystemExit('album card image wrapper not found')
p.write_text(s.replace(old, new, 1), encoding='utf-8')

# Append a final authoritative square-card interaction layer.
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 square crop with full-image hover */'
if marker not in s:
    s += r'''

/* MediaGallery 1.8 square crop with full-image hover */
.mg-album-default-grid .mg-card-square .mg-card-media {
  aspect-ratio: 1 / 1;
  height: auto;
  min-height: 0;
  padding: .7rem;
  overflow: hidden;
  background: rgba(127,127,127,.045);
}
.mg-album-default-grid .mg-card-square .mg_thumbnail,
.mg-album-default-grid .mg-card-square .mg_thumbnail_wrapper,
.mg-album-default-grid .mg-card-square .mg-card-image-link,
.mg-album-default-grid .mg-card-square .mg_thumbnail_wrapper > a {
  display: block;
  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
}
.mg-album-default-grid .mg-card-square .mg-card-media img {
  display: block;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  max-height: none !important;
  object-fit: cover;
  object-position: center center;
  border-radius: .45rem;
  transform: scale(1);
  transition: transform .28s ease, filter .28s ease;
}
.mg-album-default-grid .mg-card-square:hover .mg-card-media img,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-media img {
  object-fit: contain;
  transform: scale(.94);
}
.mg-album-default-grid .mg-card-square:hover .mg-card-media,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-media {
  background: rgba(127,127,127,.075);
}
@media (prefers-reduced-motion: reduce) {
  .mg-album-default-grid .mg-card-square .mg-card-media img {
    transition: none !important;
  }
}
'''
p.write_text(s, encoding='utf-8')
