<?php
// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | Admin menu.                                                              |
// +--------------------------------------------------------------------------+
// | Copyright (C) 2015 by the following authors:                             |
// |                                                                          |
// | Yoshinori Tahara       taharaxp AT gmail DOT com                         |
// |                                                                          |
// | Based on the Media Gallery Plugin for glFusion CMS                       |
// | Copyright (C) 2005-2010 by the following authors:                        |
// |                                                                          |
// | Mark R. Evans          mark AT glfusion DOT org                          |
// +--------------------------------------------------------------------------+
// |                                                                          |
// | This program is free software; you can redistribute it and/or            |
// | modify it under the terms of the GNU General Public License              |
// | as published by the Free Software Foundation; either version 2           |
// | of the License, or (at your option) any later version.                   |
// |                                                                          |
// | This program is distributed in the hope that it will be useful,          |
// | but WITHOUT ANY WARRANTY; without even the implied warranty of           |
// | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |
// | GNU General Public License for more details.                             |
// |                                                                          |
// | You should have received a copy of the GNU General Public License        |
// | along with this program; if not, write to the Free Software Foundation,  |
// | Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.          |
// |                                                                          |
// +--------------------------------------------------------------------------+
//

if (strpos(strtolower($_SERVER['PHP_SELF']), strtolower(basename(__FILE__))) !== false) {
    die('This file can not be used on its own!');
}

function MG_adminEscape($value)
{
    return htmlspecialchars((string) $value, ENT_QUOTES, COM_getCharset());
}

function MG_adminConfigurationForm($buttonClass = 'uk-button')
{
    global $_CONF, $LANG_MG01;

    $configUrl = rtrim((string) $_CONF['site_admin_url'], '/') . '/configuration.php';
    $class = trim((string) $buttonClass);
    $classAttribute = $class === '' ? '' : ' class="' . MG_adminEscape($class) . '"';

    return '<form class="mg-admin-config-form" method="post" action="' . MG_adminEscape($configUrl) . '">'
        . '<input type="hidden" name="conf_group" value="mediagallery">'
        . '<button' . $classAttribute . ' type="submit">' . MG_adminEscape($LANG_MG01['configuration']) . '</button>'
        . '</form>';
}

function MG_adminSafeCount($tableKey)
{
    global $_TABLES;

    if (!isset($_TABLES[$tableKey]) || $_TABLES[$tableKey] === '') {
        return 0;
    }

    $result = DB_query('SELECT COUNT(*) AS mg_count FROM ' . $_TABLES[$tableKey], 1);
    if ($result === false || DB_error()) {
        return 0;
    }

    $row = DB_fetchArray($result);
    return isset($row['mg_count']) ? (int) $row['mg_count'] : 0;
}

function MG_adminStorageStatus()
{
    global $_MG_CONF;

    if (empty($_MG_CONF['path_mediaobjects'])) {
        return false;
    }

    $path = (string) $_MG_CONF['path_mediaobjects'];
    return is_dir($path) && is_writable($path);
}

function MG_adminStyles()
{
    return '<style>'
        . '.mg-admin-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 18px;}'
        . '.mg-admin-config-form{display:inline-block;margin:0;}'
        . '.mg-admin-section{border:1px solid #d8dee6;border-radius:6px;background:#fff;padding:18px;margin:0 0 18px;}'
        . '.mg-admin-section h2{margin:0 0 12px;font-size:1.2em;}'
        . '.mg-admin-section-intro{color:#666;margin:0 0 14px;line-height:1.45;}'
        . '.mg-admin-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:0 0 18px;}'
        . '.mg-admin-metric{border:1px solid #d8dee6;border-radius:6px;background:#f7f9fb;padding:14px 16px;}'
        . '.mg-admin-metric strong{display:block;font-size:1.6em;line-height:1.1;margin-bottom:4px;}'
        . '.mg-admin-metric span{color:#666;font-size:.95em;}'
        . '.mg-admin-status-ok{color:#287a3b;}'
        . '.mg-admin-status-warning{color:#a05a00;}'
        . '.mg-admin-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;}'
        . '.mg-admin-card{border:1px solid #d8dee6;border-radius:6px;background:#fff;padding:16px;box-sizing:border-box;}'
        . '.mg-admin-card h3{margin:0 0 7px;font-size:1.05em;}'
        . '.mg-admin-card p{margin:0 0 12px;color:#666;line-height:1.45;}'
        . '.mg-admin-card .uk-button{margin-top:auto;}'
        . '.mg-admin-submenu{border:1px solid #d8dee6;border-radius:6px;background:#fff;padding:16px 18px;margin:0 0 18px;}'
        . '.mg-admin-submenu h3{margin-top:0;}'
        . '.mg-admin-submenu ul{margin-bottom:0;}'
        . '.mg-admin-stats{margin-top:18px;}'
        . '.mg-admin-actions a.uk-button:hover,.mg-admin-actions a.uk-button:focus,.mg-admin-card a.uk-button:hover,.mg-admin-card a.uk-button:focus{color:#fff!important;text-decoration:none!important;}'
        . '</style>';
}

function MG_showAdminMenu($sub_menu='')
{
    global $_CONF, $_TABLES, $_MG_CONF, $LANG_MG01;

    $help_url = $_MG_CONF['admin_url'] . 'help.php';
    $albumsUrl = $_MG_CONF['site_url'] . '/admin.php';

    $menu = MG_adminStyles();
    $menu .= '<div class="mg-admin-actions">'
        . '<a class="uk-button uk-button-primary" href="' . MG_adminEscape($albumsUrl) . '">'
        . MG_adminEscape($LANG_MG01['manage_albums']) . '</a>'
        . MG_adminConfigurationForm()
        . '<a class="uk-button" href="' . MG_adminEscape($help_url) . '">' . MG_adminEscape($LANG_MG01['help']) . '</a>'
        . '</div>';

    if ($sub_menu !== '') {
        return $menu . MG_showAdminSubMenu($sub_menu);
    }

    $albumCount = MG_adminSafeCount('mg_albums');
    $mediaCount = MG_adminSafeCount('mg_media');
    $pendingCount = MG_adminSafeCount('mg_mediaqueue');
    $storageOk = MG_adminStorageStatus();

    $menu .= '<div class="mg-admin-section">'
        . '<h2>' . MG_adminEscape($LANG_MG01['overview']) . '</h2>'
        . '<p class="mg-admin-section-intro">' . MG_adminEscape($LANG_MG01['admin_help']) . '</p>'
        . '<div class="mg-admin-metrics">'
        . '<div class="mg-admin-metric"><strong>' . $albumCount . '</strong><span>' . MG_adminEscape($LANG_MG01['albums']) . '</span></div>'
        . '<div class="mg-admin-metric"><strong>' . $mediaCount . '</strong><span>' . MG_adminEscape($LANG_MG01['media_items']) . '</span></div>'
        . '<div class="mg-admin-metric"><strong>' . $pendingCount . '</strong><span>' . MG_adminEscape($LANG_MG01['pending_media']) . '</span></div>'
        . '<div class="mg-admin-metric"><strong class="' . ($storageOk ? 'mg-admin-status-ok' : 'mg-admin-status-warning') . '">'
        . MG_adminEscape($storageOk ? $LANG_MG01['status_ok'] : $LANG_MG01['status_check']) . '</strong>'
        . '<span>' . MG_adminEscape($LANG_MG01['media_storage']) . '</span></div>'
        . '</div></div>';

    $cards = array(
        array(
            'title' => $LANG_MG01['content_categories'],
            'description' => $LANG_MG01['content_categories_help'],
            'url' => $_MG_CONF['admin_url'] . 'category.php',
            'action' => $LANG_MG01['manage']
        ),
        array(
            'title' => $LANG_MG01['member_albums'],
            'description' => $LANG_MG01['member_albums_help'],
            'url' => $_MG_CONF['admin_url'] . 'index.php?s=m',
            'action' => $LANG_MG01['manage']
        )
    );

    $menu .= '<div class="mg-admin-section"><h2>' . MG_adminEscape($LANG_MG01['content']) . '</h2>'
        . '<div class="mg-admin-grid">';
    foreach ($cards as $card) {
        $menu .= '<div class="mg-admin-card"><h3>' . MG_adminEscape($card['title']) . '</h3>'
            . '<p>' . MG_adminEscape($card['description']) . '</p>'
            . '<a class="uk-button" href="' . MG_adminEscape($card['url']) . '">' . MG_adminEscape($card['action']) . '</a></div>';
    }
    $menu .= '</div></div>';

    $tools = array(
        array(
            'title' => $LANG_MG01['maintenance_tools'],
            'description' => $LANG_MG01['maintenance_tools_help'],
            'url' => $_MG_CONF['admin_url'] . 'index.php?s=b',
            'action' => $LANG_MG01['open_tools']
        ),
        array(
            'title' => $LANG_MG01['reports_tools'],
            'description' => $LANG_MG01['reports_tools_help'],
            'url' => $_MG_CONF['admin_url'] . 'index.php?s=c',
            'action' => $LANG_MG01['open_tools']
        )
    );

    $menu .= '<div class="mg-admin-section"><h2>' . MG_adminEscape($LANG_MG01['maintenance_reports']) . '</h2>'
        . '<div class="mg-admin-grid">';
    foreach ($tools as $card) {
        $menu .= '<div class="mg-admin-card"><h3>' . MG_adminEscape($card['title']) . '</h3>'
            . '<p>' . MG_adminEscape($card['description']) . '</p>'
            . '<a class="uk-button" href="' . MG_adminEscape($card['url']) . '">' . MG_adminEscape($card['action']) . '</a></div>';
    }
    $menu .= '</div></div>';

    return $menu;
}

function MG_showAdminSubMenu($sub_menu)
{
    global $_CONF, $_TABLES, $_MG_CONF, $LANG_MG01, $LANG27;

    $menu = '';
    $admin_url = $_MG_CONF['admin_url'];
    switch ($sub_menu) {
        case 'member_albums':
            $menu .= '<h3>' . $LANG_MG01['member_albums'] . '</h3>' . LB;
            $menu .= '<ul>' . LB
                   . '<li><a href="' . $admin_url . 'createmembers.php">' . $LANG_MG01['batch_create_members'] . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'purgealbums.php">'   . $LANG_MG01['purge_member_albums']  . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'resetmembers.php">'  . $LANG_MG01['reset_members']        . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'quotareport.php">'   . $LANG_MG01['quota_reports']        . '</a></li>' . LB
                   . '</ul>' . LB;
            break;

        case 'rss_feeds':
            $menu .= '<h3>' . $LANG_MG01['rss_feeds'] . '</h3>' . LB;
            $menu .= '<ul>' . LB
                   . '<li><a href="' . $admin_url . 'rssrebuild.php?mode=full">'  . $LANG_MG01['rss_rebuild_all']   . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'rssrebuild.php?mode=album">' . $LANG_MG01['rss_rebuild_album'] . '</a></li>' . LB
                   . '</ul>' . LB;
            break;

        case 'batch_sessions':
            $session_count = DB_count($_TABLES['mg_sessions'],'session_status','1');
            $menu .= '<h3>' . $LANG_MG01['batch_sessions'] . '</h3>' . LB;
            $menu .= '<ul>' . LB
                   . '<li><a href="' . $admin_url . 'sessions.php">'                       . $LANG_MG01['paused_sessions']
                                                                                           . ' (' . $session_count .  ')'      . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'maint.php?mode=thumbs&amp;step=one">' . $LANG_MG01['rebuild_thumb']       . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'maint.php?mode=resize&amp;step=one">' . $LANG_MG01['resize_display']      . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'maint.php?mode=remove&amp;step=one">' . $LANG_MG01['discard_originals']   . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'quota.php">'                          . $LANG_MG01['rebuild_quota']       . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'staticsortalbums.php">'               . $LANG_MG01['static_sort_albums']  . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'staticsortmedia.php">'                . $LANG_MG01['static_sort_media']   . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'massdelete.php">'                     . $LANG_MG01['batch_delete_albums'] . '</a></li>' . LB

                   . '<li><a href="' . $_MG_CONF['site_url'] . '/admin.php?album_id=0&amp;mode=globalperm&amp;a=1">' . $LANG_MG01['globalperm'] . '</a></li>' . LB
                   . '<li><a href="' . $_MG_CONF['site_url'] . '/admin.php?album_id=0&amp;mode=globalattr&amp;a=1">' . $LANG_MG01['globalattr'] . '</a></li>' . LB
                   . '</ul>' . LB;
            break;

        case 'miscellaneous':
            $menu .= '<h3>' . $LANG_MG01['miscellaneous'] . '</h3>' . LB;
            $menu .= '<ul>' . LB
                   . '<li><a href="' . $admin_url . 'usage_rpt.php">'             . $LANG_MG01['usage_reports']     . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'exif_admin.php">'            . $LANG_MG01['exif_admin_header'] . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'rssrebuild.php?mode=full">'  . $LANG_MG01['rss_rebuild_all']   . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'rssrebuild.php?mode=album">' . $LANG_MG01['rss_rebuild_album'] . '</a></li>' . LB
                   . '<li><a href="' . $admin_url . 'envcheck.php">'              . $LANG_MG01['env_check']         . '</a></li>' . LB
                   . '</ul>' . LB;
            break;
    }
    return $menu === '' ? '' : '<div class="mg-admin-submenu">' . $menu . '</div>';
}

?>