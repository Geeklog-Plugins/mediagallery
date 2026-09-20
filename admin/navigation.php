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

function MG_adminStyles()
{
    return '<style>'
        . '.mg-admin-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 18px;}'
        . '.mg-admin-config-form{display:inline-block;margin:0;}'
        . '.mg-admin-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:16px 0 20px;}'
        . '.mg-admin-card{border:1px solid #d8dee6;border-radius:6px;background:#fff;padding:16px;box-sizing:border-box;}'
        . '.mg-admin-card h3{margin:0 0 8px;font-size:1.05em;}'
        . '.mg-admin-card p{margin:0 0 12px;color:#666;line-height:1.45;}'
        . '.mg-admin-card ul{margin:0;padding-left:18px;}'
        . '.mg-admin-card li{margin:5px 0;}'
        . '.mg-admin-overview{background:#f7f9fb;border:1px solid #d8dee6;border-radius:6px;padding:16px 18px;margin:0 0 18px;}'
        . '.mg-admin-overview h2{margin-top:0;}'
        . '.mg-admin-actions a.uk-button:hover,.mg-admin-actions a.uk-button:focus{color:#fff!important;text-decoration:none!important;}'
        . '</style>';
}

function MG_showAdminMenu($sub_menu='')
{
    global $_CONF, $_TABLES, $_MG_CONF, $LANG_MG01;

    require_once $_CONF['path'] . 'system/lib-admin.php';

    $help_url = $_MG_CONF['admin_url'] . 'help.php';

    $menu_arr = array(
        array('url'  => $_MG_CONF['admin_url'] . 'category.php',
              'text' => $LANG_MG01['category_manage_help']),

        array('url'  => $_MG_CONF['admin_url'] . 'index.php?s=m',
              'text' => $LANG_MG01['member_albums']),

        array('url'  => $_MG_CONF['admin_url'] . 'index.php?s=b',
              'text' => $LANG_MG01['batch_sessions']),

        array('url'  => $_MG_CONF['admin_url'] . 'index.php?s=c',
              'text' => $LANG_MG01['miscellaneous']),

        array('url'  => $help_url,
              'text' => $LANG_MG01['help']));

    $menu = MG_adminStyles();
    $menu .= '<div class="mg-admin-actions">'
        . '<a class="uk-button uk-button-primary" href="' . MG_adminEscape($_MG_CONF['site_url'] . '/admin.php') . '">' . MG_adminEscape($LANG_MG01['albums']) . '</a>'
        . MG_adminConfigurationForm()
        . '<a class="uk-button" href="' . MG_adminEscape($help_url) . '">' . MG_adminEscape($LANG_MG01['help']) . '</a>'
        . '</div>';

    if ($sub_menu === '') {
        $menu .= '<div class="mg-admin-overview"><h2>' . MG_adminEscape($LANG_MG01['admin']) . '</h2>'
            . '<p>' . MG_adminEscape($LANG_MG01['admin_help']) . '</p></div>';

        $menu .= '<div class="mg-admin-grid">';
        foreach ($menu_arr as $item) {
            if ($item['url'] === $help_url) {
                continue;
            }
            $menu .= '<div class="mg-admin-card"><h3><a href="' . MG_adminEscape($item['url']) . '">'
                . MG_adminEscape($item['text']) . '</a></h3>'
                . '<p><a class="uk-button" href="' . MG_adminEscape($item['url']) . '">' . MG_adminEscape($item['text']) . '</a></p></div>';
        }
        $menu .= '</div>';
    } else {
        $menu .= MG_showAdminSubMenu($sub_menu);
    }

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
    return $menu;
}

?>