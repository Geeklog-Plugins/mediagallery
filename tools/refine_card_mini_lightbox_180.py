from pathlib import Path

# 1) Media cards: render two image layers from the same full display preview.
p = Path('include/classMedia.php')
s = p.read_text(encoding='utf-8')
old = '''        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $media_card_preview = $media_start_link
                . '<img class="mg-card-preview-image" src="' . MG_escapeHTML($direct_url)
                . '" alt="' . $caption . '" loading="lazy" decoding="async">'
                . '</a>';
        }
'''
new = '''        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $card_preview_url = MG_escapeHTML($direct_url);
            $media_card_preview = $media_start_link
                . '<span class="mg-card-preview-stack">'
                . '<img class="mg-card-preview-image mg-card-preview-cover" src="' . $card_preview_url
                . '" alt="' . $caption . '" loading="lazy" decoding="async">'
                . '<img class="mg-card-preview-image mg-card-preview-full" src="' . $card_preview_url
                . '" alt="" aria-hidden="true" loading="lazy" decoding="async">'
                . '</span></a>';
        }
'''
if old not in s:
    raise SystemExit('classMedia preview block not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# 2) Album/root cards: same two-layer structure, using the full album cover preview.
p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
old = '''      <div class="mg_thumbnail_wrapper"><a class="mg-card-image-link" href="{u_viewalbum}"><img class="mg-card-preview-image" src="{album_last_image}" alt="{album_title}" loading="lazy" decoding="async"></a></div>'''
new = '''      <div class="mg_thumbnail_wrapper"><a class="mg-card-image-link" href="{u_viewalbum}"><span class="mg-card-preview-stack"><img class="mg-card-preview-image mg-card-preview-cover" src="{album_last_image}" alt="{album_title}" loading="lazy" decoding="async"><img class="mg-card-preview-image mg-card-preview-full" src="{album_last_image}" alt="" aria-hidden="true" loading="lazy" decoding="async"></span></a></div>'''
if old not in s:
    raise SystemExit('album card image block not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# 3) Replace the abrupt cover->contain hover with a two-layer crossfade mini-lightbox.
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 square crop with full-image hover */'
pos = s.find(marker)
if pos < 0:
    raise SystemExit('square hover CSS marker not found')
# This block is the last block in the stylesheet at present; replace through EOF.
new_css = r'''/* MediaGallery 1.8 square crop with mini-lightbox hover */
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
.mg-album-default-grid .mg-card-square .mg_thumbnail_wrapper > a,
.mg-album-default-grid .mg-card-square .mg-card-preview-stack {
  display: block;
  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
}
.mg-album-default-grid .mg-card-square .mg-card-preview-stack {
  position: relative;
  overflow: hidden;
  border-radius: .45rem;
  background: rgba(127,127,127,.055);
}
.mg-album-default-grid .mg-card-square .mg-card-preview-image {
  position: absolute;
  inset: 0;
  display: block;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  max-height: none !important;
  object-position: center center;
  border-radius: inherit;
  will-change: opacity, transform;
}
.mg-album-default-grid .mg-card-square .mg-card-preview-cover {
  object-fit: cover;
  opacity: 1;
  transform: scale(1.015);
  filter: brightness(1) saturate(1);
  transition: opacity .32s ease, transform .38s cubic-bezier(.2,.7,.2,1), filter .32s ease;
}
.mg-album-default-grid .mg-card-square .mg-card-preview-full {
  object-fit: contain;
  box-sizing: border-box;
  padding: .35rem;
  opacity: 0;
  transform: scale(.91);
  transition: opacity .32s ease, transform .38s cubic-bezier(.2,.7,.2,1);
}
.mg-album-default-grid .mg-card-square:hover .mg-card-preview-cover,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-preview-cover {
  opacity: .20;
  transform: scale(1.045);
  filter: brightness(.68) saturate(.78);
}
.mg-album-default-grid .mg-card-square:hover .mg-card-preview-full,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-preview-full {
  opacity: 1;
  transform: scale(.965);
}
.mg-album-default-grid .mg-card-square:hover .mg-card-media,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-media {
  background: rgba(127,127,127,.065);
}
@media (max-width: 38rem) {
  .mg-album-default-grid .mg-card-square .mg-card-preview-full {
    padding: .25rem;
  }
}
@media (prefers-reduced-motion: reduce) {
  .mg-album-default-grid .mg-card-square .mg-card-preview-cover,
  .mg-album-default-grid .mg-card-square .mg-card-preview-full {
    transition: none !important;
  }
}
'''
s = s[:pos] + new_css
p.write_text(s, encoding='utf-8')
