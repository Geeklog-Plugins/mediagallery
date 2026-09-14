from pathlib import Path

p = Path('include/classMedia.php')
s = p.read_text(encoding='utf-8')
old = """        $media_item_thumbnail = MG_getFramedImage($skin, $this->title, $url_media_item,\n                                                  $media_thumbnail, $newwidth, $newheight, $media_start_link);\n"""
new = old + """\n        // MediaGallery 1.8: use the larger display image for default album cards when available.\n        // This avoids visibly upscaling 100/150/200px thumbnails while preserving the\n        // historical framed thumbnail for remote images and non-image media.\n        $media_card_preview = $media_item_thumbnail;\n        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {\n            $media_card_preview = $media_start_link\n                . '<img class=\"mg-card-preview-image\" src=\"' . MG_escapeHTML($direct_url)\n                . '\" alt=\"' . $caption . '\" loading=\"lazy\" decoding=\"async\">'\n                . '</a>';\n        }\n"""
if old not in s:
    raise SystemExit('classMedia anchor not found')
s = s.replace(old, new, 1)
old2 = """            'media_item_thumbnail' => $media_item_thumbnail,\n"""
new2 = old2 + """            'media_card_preview'    => $media_card_preview,\n"""
if old2 not in s:
    raise SystemExit('template var anchor not found')
s = s.replace(old2, new2, 1)
p.write_text(s, encoding='utf-8')

p = Path('templates/album_page_media_cell.thtml')
s = p.read_text(encoding='utf-8')
old = '{media_item_thumbnail}{mp3_podcast}'
if old not in s:
    raise SystemExit('template preview anchor not found')
s = s.replace(old, '{media_card_preview}{mp3_podcast}', 1)
p.write_text(s, encoding='utf-8')

p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
css = r'''\n\n/* MediaGallery 1.8 generous album card previews */\n.mg-album-default-grid .mg-card-media {\n  display: grid;\n  place-items: center;\n  min-height: 15rem;\n  padding: .85rem;\n  overflow: hidden;\n}\n.mg-album-default-grid .mg_thumbnail,\n.mg-album-default-grid .mg_thumbnail_wrapper {\n  display: grid;\n  place-items: center;\n  width: 100%;\n  height: 100%;\n}\n.mg-album-default-grid .mg-card-preview-image {\n  display: block;\n  width: auto;\n  height: auto;\n  max-width: 92%;\n  max-height: 13rem;\n  object-fit: contain;\n  object-position: center;\n}\n@media (max-width: 38rem) {\n  .mg-album-default-grid .mg-card-media { min-height: 13rem; padding: .7rem; }\n  .mg-album-default-grid .mg-card-preview-image { max-width: 96%; max-height: 11.5rem; }\n}\n'''
if 'MediaGallery 1.8 generous album card previews' not in s:
    s += css
p.write_text(s, encoding='utf-8')
