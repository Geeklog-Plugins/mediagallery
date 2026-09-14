from pathlib import Path

# Media cards: prefer native 200x200 crop when it exists, otherwise use display image.
p = Path('include/classMedia.php')
s = p.read_text(encoding='utf-8')
old = '''        // MediaGallery 1.8: use the larger display image for default album cards when available.\n        // This avoids visibly upscaling 100/150/200px thumbnails while preserving the\n        // historical framed thumbnail for remote images and non-image media.\n        $media_card_preview = $media_item_thumbnail;\n        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {\n            $media_card_preview = $media_start_link\n                . '<img class="mg-card-preview-image" src="' . MG_escapeHTML($direct_url)\n                . '" alt="' . $caption . '" loading="lazy" decoding="async">'\n                . '</a>';\n        }\n\n        $media_orientation_class = 'mg-orientation-square';\n        if (is_array($media_size) && isset($media_size[0], $media_size[1]) && $media_size[0] > 0 && $media_size[1] > 0) {\n            if ($media_size[0] > ($media_size[1] * 1.15)) {\n                $media_orientation_class = 'mg-orientation-landscape';\n            } elseif ($media_size[1] > ($media_size[0] * 1.15)) {\n                $media_orientation_class = 'mg-orientation-portrait';\n            }\n        }\n'''
new = '''        // MediaGallery 1.8 default album cards use a square crop for a consistent grid.\n        // Prefer MediaGallery's native 200x200 crop when it already exists. Existing\n        // installations without that derivative fall back to the display image, which\n        // is cropped non-destructively by CSS (object-fit: cover).\n        $media_card_preview = $media_item_thumbnail;\n        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {\n            $card_preview_url = $direct_url;\n            $crop_info = array(\n                'media_type'        => $this->type,\n                'mime_type'         => $this->mime_type,\n                'media_filename'    => $this->filename,\n                'media_mime_ext'    => $this->mime_ext,\n                'remote_media'      => $this->remote_url,\n                'media_tn_attached' => $this->tn_attached,\n            );\n            $crop_relative = self::getDefaultThumbnail($crop_info, '12');\n            if (strpos($crop_relative, '/') !== false\n                    && file_exists($_MG_CONF['path_mediaobjects'] . $crop_relative)) {\n                $card_preview_url = $_MG_CONF['mediaobjects_url'] . '/' . $crop_relative;\n            }\n            $media_card_preview = $media_start_link\n                . '<img class="mg-card-preview-image" src="' . MG_escapeHTML($card_preview_url)\n                . '" alt="' . $caption . '" loading="lazy" decoding="async">'\n                . '</a>';\n        }\n'''
if old not in s:
    raise SystemExit('classMedia preview block not found')
s = s.replace(old, new, 1)
s = s.replace("            'media_orientation_class' => $media_orientation_class,\n", '', 1)
p.write_text(s, encoding='utf-8')

# Root/subalbum covers: prefer native 200x200 crop when available; keep current fallback.
p = Path('include/common.php')
s = p.read_text(encoding='utf-8')
old = '''    $cover_orientation_class = 'mg-orientation-square';\n    if (is_array($mediasize) && isset($mediasize[0], $mediasize[1]) && $mediasize[0] > 0 && $mediasize[1] > 0) {\n        if ($mediasize[0] > ($mediasize[1] * 1.15)) {\n            $cover_orientation_class = 'mg-orientation-landscape';\n        } elseif ($mediasize[1] > ($mediasize[0] * 1.15)) {\n            $cover_orientation_class = 'mg-orientation-portrait';\n        }\n    }\n\n'''
new = '''    // MediaGallery 1.8: album cards use a square cover. Prefer an existing\n    // native 200x200 crop, otherwise the current cover is cropped by CSS.\n    if ($album_data['tn_attached'] != 1 && $cover_filename != '' && $cover_filename != '0'\n            && strpos($cover_filename, 'tn_') !== 0) {\n        $square_cover = MG_getThumbPath('tn/' . $cover_filename[0] . '/' . $cover_filename, '12');\n        $square_cover = rtrim($square_cover, '.');\n        list($square_cover_url, $square_cover_size) = MG_getImageUrl($square_cover);\n        if ($square_cover_size !== false) {\n            $album_last_image = $square_cover_url;\n            $mediasize = $square_cover_size;\n        }\n    }\n\n'''
if old not in s:
    raise SystemExit('common orientation block not found')
s = s.replace(old, new, 1)
s = s.replace("        'cover_orientation_class' => $cover_orientation_class,\n", '', 1)
p.write_text(s, encoding='utf-8')

# Templates: remove orientation classes from default cards.
p = Path('templates/album_page_media_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('mg-card mg-card-compact {media_orientation_class}', 'mg-card mg-card-compact mg-card-square', 1)
p.write_text(s, encoding='utf-8')

p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('mg-card {cover_orientation_class}', 'mg-card mg-card-square', 1)
p.write_text(s, encoding='utf-8')

# Replace the orientation-specific tail with one square-card layer.
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 balanced album and root card previews */'
pos = s.find(marker)
if pos == -1:
    raise SystemExit('balanced card CSS marker not found')
s = s[:pos].rstrip() + '\n\n'
css = '''/* MediaGallery 1.8 square album and root card previews */\n.mg-album-default-grid .mg-card-media {\n  display: grid;\n  place-items: center;\n  width: 100%;\n  aspect-ratio: 1 / 1;\n  min-height: 0;\n  padding: .7rem;\n  overflow: hidden;\n  background: rgba(127, 127, 127, .035);\n  box-sizing: border-box;\n}\n.mg-album-default-grid .mg_thumbnail,\n.mg-album-default-grid .mg_thumbnail_wrapper,\n.mg-album-default-grid .mg_thumbnail_wrapper > a {\n  display: block;\n  width: 100%;\n  height: 100%;\n  min-width: 0;\n  min-height: 0;\n}\n.mg-album-default-grid .mg-card-media img {\n  display: block;\n  width: 100% !important;\n  height: 100% !important;\n  max-width: none !important;\n  max-height: none !important;\n  object-fit: cover;\n  object-position: center center;\n  border-radius: .35rem;\n  transition: transform .28s ease;\n}\n@media (max-width: 38rem) {\n  .mg-album-default-grid .mg-card-media {\n    padding: .55rem;\n  }\n}\n'''
s += css
p.write_text(s, encoding='utf-8')
