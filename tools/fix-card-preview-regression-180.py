from pathlib import Path

path = Path('include/classMedia.php')
text = path.read_text(encoding='utf-8')
old = '''        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $media_card_preview = $media_start_link
                . '<span class=\\"mg-card-preview-stack\\">'
                . '<img class=\\"mg-card-preview-image mg-card-preview-cover\\" src=\\"' . MG_escapeHTML($direct_url)
                . '\\" alt=\\"' . $caption . '\\" loading=\\"lazy\\" decoding=\\"async\\">'
                . '<img class=\\"mg-card-preview-image mg-card-preview-full\\" src=\\"' . MG_escapeHTML($direct_url)
                . '\\" alt=\\"\\" aria-hidden=\\"true\\" loading=\\"lazy\\" decoding=\\"async\\">'
                . '</span></a>';
        }
'''
new = '''        $media_card_preview = $media_item_thumbnail;
        if ($searchmode == 0 && $this->type == 0 && $this->remote != 1 && !empty($direct_url)) {
            $media_card_preview = $media_start_link
                . '<span class="mg-card-preview-stack">'
                . '<img class="mg-card-preview-image mg-card-preview-cover" src="' . MG_escapeHTML($direct_url)
                . '" alt="' . $caption . '" loading="lazy" decoding="async">'
                . '<img class="mg-card-preview-image mg-card-preview-full" src="' . MG_escapeHTML($direct_url)
                . '" alt="" aria-hidden="true" loading="lazy" decoding="async">'
                . '</span></a>';
        }
'''
if old not in text:
    raise SystemExit('Expected broken mini-lightbox block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
