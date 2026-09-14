from pathlib import Path

# classMedia.php is historical latin-1; preserve encoding byte-for-byte outside edits.
media = Path('include/classMedia.php')
text = media.read_text(encoding='latin-1')
old = """        // MediaGallery 1.8: use the display derivative for the sharp square cover
        // and the uncropped original for the mini-lightbox whenever it exists.
        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $card_cover_source = $direct_url;
            $card_full_source = $direct_url;
            $orig_preview_path = self::getFilePath('orig', $this->filename, $this->mime_ext);
            if (file_exists($orig_preview_path)) {
                $card_full_source = self::getFileUrl('orig', $this->filename, $this->mime_ext);
            }
"""
new = """        // MediaGallery 1.8: default album cards need one reliable, uncropped source.
        // Use the local original for both layers when available: CSS alone creates the
        // square crop at rest and reveals the same complete image on hover/focus.
        // The browser reuses the identical resource for both <img> elements.
        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $card_cover_source = $direct_url;
            $card_full_source = $direct_url;
            $orig_preview_path = self::getFilePath('orig', $this->filename, $this->mime_ext);
            if (file_exists($orig_preview_path)) {
                $original_card_url = self::getFileUrl('orig', $this->filename, $this->mime_ext);
                $card_cover_source = $original_card_url;
                $card_full_source = $original_card_url;
            }
"""
if old not in text:
    raise SystemExit('Expected classMedia card source block not found')
text = text.replace(old, new, 1)
media.write_text(text, encoding='latin-1')

css = Path('public_html/style.css')
s = css.read_text(encoding='utf-8')
s = s.replace(""".mg-album-default-grid .mg-card-square .mg-card-preview-cover {
  object-fit: cover;
  opacity: 1;
  transform: scale(1.015);
""", """.mg-album-default-grid .mg-card-square .mg-card-preview-cover {
  object-fit: cover;
  opacity: 1;
  transform: none;
""", 1)
s = s.replace(""".mg-album-default-grid .mg-card-square:hover .mg-card-preview-full,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-preview-full {
  opacity: 1;
  transform: scale(.965);
}
""", """.mg-album-default-grid .mg-card-square:hover .mg-card-preview-full,
.mg-album-default-grid .mg-card-square:focus-within .mg-card-preview-full {
  opacity: 1;
  transform: none;
}
""", 1)
css.write_text(s, encoding='utf-8')
