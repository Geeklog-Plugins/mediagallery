from pathlib import Path

# classMedia.php
p = Path('include/classMedia.php')
s = p.read_text(encoding='utf-8')
needle = """        if ($mode == 1) {\n            return $media_item_thumbnail;\n        }\n"""
insert = """        $media_orientation_class = 'mg-orientation-square';\n        if (is_array($media_size) && isset($media_size[0], $media_size[1]) && $media_size[0] > 0 && $media_size[1] > 0) {\n            if ($media_size[0] > ($media_size[1] * 1.15)) {\n                $media_orientation_class = 'mg-orientation-landscape';\n            } elseif ($media_size[1] > ($media_size[0] * 1.15)) {\n                $media_orientation_class = 'mg-orientation-portrait';\n            }\n        }\n\n        if ($mode == 1) {\n            return $media_item_thumbnail;\n        }\n"""
if needle not in s:
    raise SystemExit('classMedia orientation insertion point not found')
s = s.replace(needle, insert, 1)
needle2 = "            'media_card_preview'    => $media_card_preview,\n"
if needle2 not in s:
    raise SystemExit('classMedia set_var point not found')
s = s.replace(needle2, needle2 + "            'media_orientation_class' => $media_orientation_class,\n", 1)
p.write_text(s, encoding='utf-8')

# common.php root/subalbum cover preview + orientation
p = Path('include/common.php')
s = p.read_text(encoding='utf-8')
needle = """    if ($album_data['tn_attached'] == 1) {\n        list($album_last_image, $mediasize) = MG_getImageUrl('covers/cover_' . $album_id);\n        if ($mediasize == false) {\n            $album_last_image = $_MG_CONF['site_url'] . '/mediaobjects/missing.png';\n            $mediasize = @getimagesize($_MG_CONF['path_html'] . 'mediaobjects/missing.png');\n        }\n    }\n\n    $children = MG_getAlbumChildren($album_id);\n"""
insert = """    if ($album_data['tn_attached'] == 1) {\n        list($album_last_image, $mediasize) = MG_getImageUrl('covers/cover_' . $album_id);\n        if ($mediasize == false) {\n            $album_last_image = $_MG_CONF['site_url'] . '/mediaobjects/missing.png';\n            $mediasize = @getimagesize($_MG_CONF['path_html'] . 'mediaobjects/missing.png');\n        }\n    } else {\n        // MediaGallery 1.8: prefer the larger display derivative for album cards.\n        // Fall back to the historical thumbnail when no display image exists.\n        $display_cover_filename = '';\n        if ($cover_filename != '' && $cover_filename != '0' && strpos($cover_filename, 'tn_') !== 0) {\n            $display_cover_filename = $cover_filename;\n        } elseif (isset($filename) && $filename != '' && $filename != ' ') {\n            $display_cover_filename = $filename;\n        }\n        if ($display_cover_filename != '') {\n            list($display_cover_image, $display_cover_size) = MG_getImageUrl(\n                'disp/' . $display_cover_filename[0] . '/' . $display_cover_filename\n            );\n            if ($display_cover_size !== false) {\n                $album_last_image = $display_cover_image;\n                $mediasize = $display_cover_size;\n            }\n        }\n    }\n\n    $cover_orientation_class = 'mg-orientation-square';\n    if (is_array($mediasize) && isset($mediasize[0], $mediasize[1]) && $mediasize[0] > 0 && $mediasize[1] > 0) {\n        if ($mediasize[0] > ($mediasize[1] * 1.15)) {\n            $cover_orientation_class = 'mg-orientation-landscape';\n        } elseif ($mediasize[1] > ($mediasize[0] * 1.15)) {\n            $cover_orientation_class = 'mg-orientation-portrait';\n        }\n    }\n\n    $children = MG_getAlbumChildren($album_id);\n"""
if needle not in s:
    raise SystemExit('common album cover insertion point not found')
s = s.replace(needle, insert, 1)
needle2 = "        'media_item_thumbnail' => $media_item_thumbnail,\n"
if needle2 not in s:
    raise SystemExit('common set_var point not found')
s = s.replace(needle2, needle2 + "        'cover_orientation_class' => $cover_orientation_class,\n", 1)
p.write_text(s, encoding='utf-8')

# media template
p = Path('templates/album_page_media_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('<article class="mg_media_item mg-card mg-card-compact">', '<article class="mg_media_item mg-card mg-card-compact {media_orientation_class}">', 1)
p.write_text(s, encoding='utf-8')

# album/root template
p = Path('templates/album_page_album_cell.thtml')
s = p.read_text(encoding='utf-8')
s = s.replace('<article class="mg_album_item mg-card">', '<article class="mg_album_item mg-card {cover_orientation_class}">', 1)
p.write_text(s, encoding='utf-8')

# CSS: remove malformed literal-escape block and append canonical rules
p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = r'\n\n/* MediaGallery 1.8 generous album card previews */\n'
pos = s.find(marker)
if pos == -1:
    marker = r'\n\n/* MediaGallery 1.8 generous album card previews */'
    pos = s.find(marker)
if pos != -1:
    s = s[:pos].rstrip() + '\n\n'
else:
    marker2 = '/* MediaGallery 1.8 generous album card previews */'
    pos = s.find(marker2)
    if pos != -1:
        s = s[:pos].rstrip() + '\n\n'
css = '''/* MediaGallery 1.8 balanced album and root card previews */
.mg-album-default-grid .mg-card-media {
  display: grid;
  place-items: center;
  height: 17rem;
  min-height: 17rem;
  padding: 1rem;
  overflow: hidden;
  background: rgba(127, 127, 127, .035);
}
.mg-album-default-grid .mg_thumbnail,
.mg-album-default-grid .mg_thumbnail_wrapper,
.mg-album-default-grid .mg_thumbnail_wrapper > a {
  display: grid;
  place-items: center;
  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
}
.mg-album-default-grid .mg-card-media img {
  display: block;
  width: auto !important;
  height: auto !important;
  object-fit: contain;
  object-position: center;
}
.mg-album-default-grid .mg_media_item.mg-orientation-landscape .mg-card-media img,
.mg-album-default-grid .mg_album_item.mg-orientation-landscape .mg-card-media img {
  max-width: 94%;
  max-height: 13rem;
}
.mg-album-default-grid .mg_media_item.mg-orientation-portrait .mg-card-media img,
.mg-album-default-grid .mg_album_item.mg-orientation-portrait .mg-card-media img {
  max-width: 78%;
  max-height: 15rem;
}
.mg-album-default-grid .mg_media_item.mg-orientation-square .mg-card-media img,
.mg-album-default-grid .mg_album_item.mg-orientation-square .mg-card-media img {
  max-width: 86%;
  max-height: 14rem;
}
.mg-album-default-grid .mg-card-media img {
  transition: transform .28s ease;
}
@media (max-width: 38rem) {
  .mg-album-default-grid .mg-card-media {
    height: 14rem;
    min-height: 14rem;
    padding: .75rem;
  }
  .mg-album-default-grid .mg_media_item.mg-orientation-landscape .mg-card-media img,
  .mg-album-default-grid .mg_album_item.mg-orientation-landscape .mg-card-media img {
    max-width: 96%;
    max-height: 10.75rem;
  }
  .mg-album-default-grid .mg_media_item.mg-orientation-portrait .mg-card-media img,
  .mg-album-default-grid .mg_album_item.mg-orientation-portrait .mg-card-media img {
    max-width: 82%;
    max-height: 12.5rem;
  }
  .mg-album-default-grid .mg_media_item.mg-orientation-square .mg-card-media img,
  .mg-album-default-grid .mg_album_item.mg-orientation-square .mg-card-media img {
    max-width: 90%;
    max-height: 11.75rem;
  }
}
'''
s = s.rstrip() + '\n\n' + css
p.write_text(s, encoding='utf-8')
