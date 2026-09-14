from pathlib import Path

# classMedia.php contains historical non-UTF-8 bytes: preserve byte mapping with latin-1.
class_path = Path('include/classMedia.php')
text = class_path.read_text(encoding='latin-1')
old = """        $direct_url = '';
        $direct_path = self::getFilePath('disp', $this->filename, $this->mime_ext);
        if (file_exists($direct_path)) {
            $direct_url = self::getFileUrl('disp', $this->filename, $this->mime_ext);
        } else {
            $direct_jpg_path = self::getFilePath('disp', $this->filename, 'jpg');
            if (file_exists($direct_jpg_path)) {
                $direct_url = self::getFileUrl('disp', $this->filename, 'jpg');
            } elseif (!empty($this->media_thumbnail)) {
                // Existing installations may not have a display derivative for every image.
                // Fall back to the proven historical thumbnail instead of emitting a broken URL.
                $direct_url = $this->media_thumbnail;
            }
        }
"""
new = """        $direct_url = '';
        $direct_preview_path = '';
        $direct_path = self::getFilePath('disp', $this->filename, $this->mime_ext);
        if (file_exists($direct_path)) {
            $direct_url = self::getFileUrl('disp', $this->filename, $this->mime_ext);
            $direct_preview_path = $direct_path;
        } else {
            $direct_jpg_path = self::getFilePath('disp', $this->filename, 'jpg');
            if (file_exists($direct_jpg_path)) {
                $direct_url = self::getFileUrl('disp', $this->filename, 'jpg');
                $direct_preview_path = $direct_jpg_path;
            } elseif (!empty($this->media_thumbnail)) {
                // Existing installations may not have a display derivative for every image.
                // Fall back to the proven historical thumbnail instead of emitting a broken URL.
                $direct_url = $this->media_thumbnail;
            }
        }
"""
if old not in text:
    raise SystemExit('direct preview source block not found')
text = text.replace(old, new, 1)

old = """        // MediaGallery 1.8: default album cards use the full display preview.
        // CSS crops it to a square at rest and reveals the complete image on hover/focus.
        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $card_preview_url = MG_escapeHTML($direct_url);
            $media_card_preview = $media_start_link
                . '<span class=\"mg-card-preview-stack\">'
                . '<img class=\"mg-card-preview-image mg-card-preview-cover\" src=\"' . $card_preview_url
                . '\" alt=\"' . $caption . '\" loading=\"lazy\" decoding=\"async\">'
                . '<img class=\"mg-card-preview-image mg-card-preview-full\" src=\"' . $card_preview_url
                . '\" alt=\"\" aria-hidden=\"true\" loading=\"lazy\" decoding=\"async\">'
                . '</span></a>';
        }
"""
new = """        // MediaGallery 1.8: square crop at rest, complete image on hover/focus.
        // Prefer the lighter display derivative for the full layer when it preserves
        // the original aspect ratio. If a legacy derivative is itself cropped, use
        // the original image so portrait media can really be revealed in full.
        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $card_cover_source = !empty($this->media_thumbnail) ? $this->media_thumbnail : $direct_url;
            $card_full_source = $direct_url;
            $orig_preview_path = self::getFilePath('orig', $this->filename, $this->mime_ext);
            if (file_exists($orig_preview_path)) {
                $orig_preview_size = @getimagesize($orig_preview_path);
                $display_preview_size = ($direct_preview_path != '') ? @getimagesize($direct_preview_path) : false;
                if ($orig_preview_size !== false && $orig_preview_size[0] > 0 && $orig_preview_size[1] > 0) {
                    $use_original_preview = ($display_preview_size === false
                        || $display_preview_size[0] < 1 || $display_preview_size[1] < 1);
                    if (!$use_original_preview) {
                        $orig_ratio = $orig_preview_size[0] / $orig_preview_size[1];
                        $display_ratio = $display_preview_size[0] / $display_preview_size[1];
                        $use_original_preview = abs($orig_ratio - $display_ratio) > 0.02;
                    }
                    if ($use_original_preview) {
                        $card_full_source = self::getFileUrl('orig', $this->filename, $this->mime_ext);
                    }
                }
            }
            $card_cover_url = MG_escapeHTML($card_cover_source);
            $card_full_url = MG_escapeHTML($card_full_source);
            $media_card_preview = $media_start_link
                . '<span class=\"mg-card-preview-stack\">'
                . '<img class=\"mg-card-preview-image mg-card-preview-cover\" src=\"' . $card_cover_url
                . '\" alt=\"' . $caption . '\" loading=\"lazy\" decoding=\"async\">'
                . '<img class=\"mg-card-preview-image mg-card-preview-full\" src=\"' . $card_full_url
                . '\" alt=\"\" aria-hidden=\"true\" loading=\"lazy\" decoding=\"async\">'
                . '</span></a>';
        }
"""
if old not in text:
    raise SystemExit('card preview HTML block not found')
text = text.replace(old, new, 1)
class_path.write_text(text, encoding='latin-1')

common_path = Path('include/common.php')
common = common_path.read_text(encoding='utf-8')
needle = """    // Keep the complete display cover; CSS handles square cropping non-destructively.
    $children = MG_getAlbumChildren($album_id);
"""
replacement = """    // Keep separate cover/full sources for the mini-lightbox. A display derivative
    // that preserves the original ratio stays preferred; a cropped legacy derivative
    // falls back to the original so portrait covers can be revealed completely.
    $album_full_image = $album_last_image;
    if ($album_data['tn_attached'] != 1 && isset($display_cover_filename) && $display_cover_filename != '') {
        list($original_cover_image, $original_cover_size) = MG_getImageUrl(
            'orig/' . $display_cover_filename[0] . '/' . $display_cover_filename
        );
        if ($original_cover_size !== false && $original_cover_size[0] > 0 && $original_cover_size[1] > 0) {
            $use_original_cover = ($mediasize === false || $mediasize[0] < 1 || $mediasize[1] < 1);
            if (!$use_original_cover) {
                $original_cover_ratio = $original_cover_size[0] / $original_cover_size[1];
                $preview_cover_ratio = $mediasize[0] / $mediasize[1];
                $use_original_cover = abs($original_cover_ratio - $preview_cover_ratio) > 0.02;
            }
            if ($use_original_cover) {
                $album_full_image = $original_cover_image;
            }
        }
    }

    $children = MG_getAlbumChildren($album_id);
"""
if needle not in common:
    raise SystemExit('common album full source insertion point not found')
common = common.replace(needle, replacement, 1)
needle2 = """        'album_last_image'     => $album_last_image,
        'album_title'          => $album_data['album_title'],
"""
replacement2 = """        'album_last_image'     => $album_last_image,
        'album_full_image'     => $album_full_image,
        'album_title'          => $album_data['album_title'],
"""
if needle2 not in common:
    raise SystemExit('album_full_image template assignment point not found')
common = common.replace(needle2, replacement2, 1)
common_path.write_text(common, encoding='utf-8')

template_path = Path('templates/album_page_album_cell.thtml')
template = template_path.read_text(encoding='utf-8')
old_template = 'class="mg-card-preview-image mg-card-preview-full" src="{album_last_image}"'
new_template = 'class="mg-card-preview-image mg-card-preview-full" src="{album_full_image}"'
if old_template not in template:
    raise SystemExit('album full preview template source not found')
template = template.replace(old_template, new_template, 1)
template_path.write_text(template, encoding='utf-8')
