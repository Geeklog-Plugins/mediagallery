from pathlib import Path
import re

path = Path('include/lib-media.php')
text = path.read_text(encoding='latin-1')

# Remove the historical inline presentation wrapper while preserving the
# existing description transformation itself.
start = text.find("    $media_desc = PLG_replaceTags(nl2br($media['media_desc']));")
end = text.find("    $getid3link = '';", start)
if start < 0 or end < 0:
    raise SystemExit('Media description block not found')
text = text[:start] + "    $media_desc = PLG_replaceTags(nl2br($media['media_desc']));\n\n" + text[end:]

# Replace the whole historical keyword builder, bounded by stable variables.
start = text.find("    $kwText = '';", end)
end = text.find("    $media_user_id = $media['media_user_id'];", start)
if start < 0 or end < 0:
    raise SystemExit('Keyword builder block not found')
new_kw = """    $kwText = '';
    $lang_keywords = '';
    if ($mg_album->enable_keywords == 1 && !empty($media['media_keywords'])) {
        $lang_keywords = $LANG_MG01['keywords'];
        $keyWords = preg_split('/[\\s,]+/', trim($media['media_keywords']));
        if (!is_array($keyWords)) {
            $keyWords = array();
        }
        foreach ($keyWords as $keyword) {
            $keyword = trim(str_replace('\\\"', ' ', $keyword));
            if ($keyword === '') {
                continue;
            }
            $searchKeyword = rawurlencode($keyword);
            $displayKeyword = MG_escapeHTML(str_replace('_', ' ', $keyword));
            $kwText .= '<a class=\"mg-tag\" href=\"' . $_MG_CONF['site_url']
                . '/search.php?mode=search&amp;swhere=1&amp;keywords=' . $searchKeyword
                . '&amp;keyType=any\">' . $displayKeyword . '</a>';
        }
    }

"""
text = text[:start] + new_kw + text[end:]
path.write_text(text, encoding='latin-1')
print('Patched media description and keyword producers')
