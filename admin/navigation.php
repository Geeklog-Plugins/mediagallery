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

require_once $_CONF['path'] . 'system/lib-admin.php';

function MG_adminEscape($value)
{
    return htmlspecialchars((string) $value, ENT_QUOTES, COM_getCharset());
}

function MG_showAdminMenu($sub_menu = '')
{
    global $_CONF, $_MG_CONF, $LANG_MG01;

    $T = new Template($_MG_CONF['template_path']);
    $T->set_file('admin_navigation', 'admin_navigation.thtml');

    $T->set_var(array(
        'admin_home_url'    => $_MG_CONF['admin_url'] . 'index.php',
        'configuration_url' => $_CONF['site_admin_url'] . '/configuration.php',
        'help_url'          => $_MG_CONF['admin_url'] . 'help.php',
        'lang_overview'     => $LANG_MG01['overview'],
        'lang_configuration'=> $LANG_MG01['configuration'],
        'lang_help'         => $LANG_MG01['help'],
        'sub_menu'          => MG_showAdminSubMenu($sub_menu),
    ));

    return $T->finish($T->parse('output', 'admin_navigation'));
}

function MG_showAdminSubMenu($sub_menu)
{
    global $_TABLES, $_MG_CONF, $LANG_MG01;

    $adminUrl = $_MG_CONF['admin_url'];
    $title = '';
    $items = array();

    switch ($sub_menu) {
        case 'member_albums':
            $title = $LANG_MG01['member_albums'];
            $items = array(
                array($adminUrl . 'createmembers.php', $LANG_MG01['batch_create_members']),
                array($adminUrl . 'purgealbums.php', $LANG_MG01['purge_member_albums']),
                array($adminUrl . 'resetmembers.php', $LANG_MG01['reset_members']),
                array($adminUrl . 'quotareport.php', $LANG_MG01['quota_reports']),
            );
            break;

        case 'rss_feeds':
            $title = $LANG_MG01['rss_feeds'];
            $items = array(
                array($adminUrl . 'rssrebuild.php?mode=full', $LANG_MG01['rss_rebuild_all']),
                array($adminUrl . 'rssrebuild.php?mode=album', $LANG_MG01['rss_rebuild_album']),
            );
            break;

        case 'batch_sessions':
            $sessionCount = DB_count($_TABLES['mg_sessions'], 'session_status', '1');
            $title = $LANG_MG01['maintenance_tools'];
            $items = array(
                array($adminUrl . 'sessions.php', $LANG_MG01['paused_sessions'] . ' (' . $sessionCount . ')'),
                array($adminUrl . 'maint.php?mode=thumbs&step=one', $LANG_MG01['rebuild_thumb']),
                array($adminUrl . 'maint.php?mode=resize&step=one', $LANG_MG01['resize_display']),
                array($adminUrl . 'maint.php?mode=remove&step=one', $LANG_MG01['discard_originals']),
                array($adminUrl . 'quota.php', $LANG_MG01['rebuild_quota']),
                array($adminUrl . 'staticsortalbums.php', $LANG_MG01['static_sort_albums']),
                array($adminUrl . 'staticsortmedia.php', $LANG_MG01['static_sort_media']),
                array($adminUrl . 'massdelete.php', $LANG_MG01['batch_delete_albums']),
                array($_MG_CONF['site_url'] . '/admin.php?album_id=0&mode=globalperm&a=1', $LANG_MG01['globalperm']),
                array($_MG_CONF['site_url'] . '/admin.php?album_id=0&mode=globalattr&a=1', $LANG_MG01['globalattr']),
            );
            break;

        case 'miscellaneous':
            $title = $LANG_MG01['reports_tools'];
            $items = array(
                array($adminUrl . 'usage_rpt.php', $LANG_MG01['usage_reports']),
                array($adminUrl . 'exif_admin.php', $LANG_MG01['exif_admin_header']),
                array($adminUrl . 'rssrebuild.php?mode=full', $LANG_MG01['rss_rebuild_all']),
                array($adminUrl . 'rssrebuild.php?mode=album', $LANG_MG01['rss_rebuild_album']),
                array($adminUrl . 'envcheck.php', $LANG_MG01['env_check']),
            );
            break;
    }

    if ($title === '' || empty($items)) {
        return '';
    }

    $html = '<div class="mg-admin-subnav">'
          . '<strong class="mg-admin-subnav__title">' . MG_adminEscape($title) . '</strong>'
          . '<div class="mg-admin-subnav__links">';

    foreach ($items as $item) {
        $html .= '<a href="' . MG_adminEscape($item[0]) . '">' . MG_adminEscape($item[1]) . '</a>';
    }

    $html .= '</div></div>';

    return $html;
}

?>