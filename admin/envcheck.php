<?php
// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | envcheck.php                                                             |
// |                                                                          |
// | Post configuration checks to validate environemnt                        |
// +--------------------------------------------------------------------------+
// | Copyright (C) 2015 by the following authors:                             |
// |                                                                          |
// | Yoshinori Tahara       taharaxp AT gmail DOT com                         |
// |                                                                          |
// | Based on the Media Gallery Plugin for glFusion CMS                       |
// | Copyright (C) 2002-2009 by the following authors:                        |
// |                                                                          |
// | Mark R. Evans          mark AT glfusion DOT org                           |
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

require_once '../../../lib-common.php';
require_once '../../auth.inc.php';

// Only let admin users access this page
if (!SEC_hasRights('mediagallery.config')) {
    // Someone is trying to illegally access this page
    COM_errorLog("Someone has tried to illegally access the Media Gallery Configuration page. "
               . "User id: {$_USER['uid']}, Username: {$_USER['username']}, IP: " . $_SERVER['REMOTE_ADDR'], 1);
    $display = COM_startBlock($LANG_MG00['access_denied']);
    $display .= $LANG_MG00['access_denied_msg'];
    $display .= COM_endBlock();
    $display = COM_createHTMLDocument($display);
    COM_output($display);
    exit;
}

require_once $_MG_CONF['path_admin'] . 'navigation.php';

function gdVersion($user_ver = 0)
{
   if (! extension_loaded('gd')) { return; }
   static $gd_ver = 0;
   if ($user_ver == 1) { $gd_ver = 1; return 1; }
   if ($user_ver !=2 && $gd_ver > 0) { return $gd_ver; }
   if (function_exists('gd_info')) {
       $ver_info = gd_info();
       preg_match('/\d/', $ver_info['GD Version'], $match);
       $gd_ver = $match[0];
       return $match[0];
   }
   if (preg_match('/phpinfo/', ini_get('disable_functions'))) {
       if ($user_ver == 2) {
           $gd_ver = 2;
           return 2;
       } else {
           $gd_ver = 1;
           return 1;
       }
   }
   ob_start();
   phpinfo(8);
   $info = ob_get_contents();
   ob_end_clean();
   $info = stristr($info, 'gd version');
   preg_match('/\d/', $info, $match);
   $gd_ver = $match[0];
   return $match[0];
}

function MG_checkEnvironment($storageMessage = '', $storageSuccess = true)
{
    global $_CONF,  $_MG_CONF, $LANG_MG01, $_TABLES;

    $retval = '';

    $T = new Template($_MG_CONF['template_path']);
    $T->set_file('admin', 'envcheck.thtml');
    $T->set_var('site_url', $_CONF['site_url']);
    $T->set_var('site_admin_url', $_CONF['site_admin_url']);
    $T->set_var('xhtml', XHTML);

    $T->set_block('admin', 'CheckRow2', 'CRow2');
    $T->set_block('admin', 'CheckRow1', 'CRow1');

    $T->set_var('CRow2', '');

    if (ini_get('safe_mode') != 1) {
        switch ($_CONF['image_lib']) {
            case 'imagemagick' :
                $binary = 'convert' . ((PHP_OS == 'WINNT') ? '.exe' : '');
                clearstatcache();
                if (! @file_exists($_MG_CONF['path_to_imagemagick'] . $binary)) {
                    $T->set_var(array('config_item' => 'ImageMagick Programs','status' => '<span style="color:red">' .  $LANG_MG01['not_found'] . '</span>'));
                } else {
                    $T->set_var(array('config_item' => 'ImageMagick Programs','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
                }
                $T->parse('CRow2', 'CheckRow2', true);
                break;
            case 'netpbm' :
                $binary = 'jpegtopnm' . ((PHP_OS == 'WINNT') ? '.exe' : '');
                clearstatcache();
                if (! @file_exists($_CONF['path_to_netpbm'] . $binary)) {
                    $T->set_var(array('config_item' => 'NetPBM Programs','status' => '<span style="color:red">' . $LANG_MG01['not_found'] . '</span>'));
                } else {
                    $T->set_var(array('config_item' => 'NetPBM Programs','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
                }
                $T->parse('CRow2', 'CheckRow2', true);
                break;
            case 'gdlib' :
                if ($gdv = gdVersion()) {
                    if ($gdv >=2) {
                        $T->set_var(array('config_item' => 'GD Libraries','status' => '<span style="color:green">v2 Installed</span>'));
                    } else {
                        $T->set_var(array('config_item' => 'GD Libraries','status' => '<span style="color:yellow">v1 Installed</span>'));
                    }
                } else {
                    $T->set_var(array('config_item' => 'GD Libraries','status' => '<span style="color:red">' . $LANG_MG01['not_found'] . '</span>'));
                }
                $T->parse('CRow2', 'CheckRow2', true);
                break;
        }

        if ($_MG_CONF['jhead_enabled']) {
            $binary = '/jhead' . ((PHP_OS == 'WINNT') ? '.exe' : '');
            clearstatcache();
            if (! @file_exists($_MG_CONF['jhead_path'] . $binary)) {
                $T->set_var(array('config_item' => 'jhead Program','status' => '<span style="color:red">' .  $LANG_MG01['not_found'] . '</span>'));
            } else {
                $T->set_var(array('config_item' => 'jhead Program','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
            }
            $T->parse('CRow2', 'CheckRow2', true);
        }

        if ($_MG_CONF['jpegtran_enabled']) {
            $binary = '/jpegtran' . ((PHP_OS == 'WINNT') ? '.exe' : '');
            clearstatcache();
            if (! @file_exists($_MG_CONF['jpegtran_path'] . $binary)) {
                $T->set_var(array('config_item' => 'jpegtran Program','status' => '<span style="color:red">' .  $LANG_MG01['not_found'] . '</span>'));
            } else {
                $T->set_var(array('config_item' => 'jpegtran Program','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
            }
            $T->parse('CRow2', 'CheckRow2', true);
        }

        if ($_MG_CONF['ffmpeg_enabled']) {
            $binary = '/ffmpeg' . ((PHP_OS == 'WINNT') ? '.exe' : '');
            clearstatcache();
            if (! @file_exists($_MG_CONF['ffmpeg_path'] . $binary)) {
                $T->set_var(array('config_item' => 'ffmpeg Program','status' => '<span style="color:red">' .  $LANG_MG01['not_found'] . '</span>'));
            } else {
                $T->set_var(array('config_item' => 'ffmpeg Program','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
            }
            $T->parse('CRow2', 'CheckRow2', true);
        }

        if ($_MG_CONF['zip_enabled']) {
            $binary = '/unzip' . ((PHP_OS == 'WINNT') ? '.exe' : '');
            clearstatcache();
            if (! @file_exists($_MG_CONF['zip_path'] . $binary)) {
                $T->set_var(array('config_item' => 'unzip Program','status' => '<span style="color:red">' .  $LANG_MG01['not_found'] . '</span>'));
            } else {
                $T->set_var(array('config_item' => 'unzip Program','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
            }
            $T->parse('CRow2', 'CheckRow2', true);
        }
    } else {
        $T->set_var(array('config_item' => 'Program Locations','status' => '<span style="color:red">Unable to check because of safe_mode restrictions</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
    }

    $tmp = $T->get_var('CRow2');
    if (!empty($tmp)) {
        $T->set_var('config_title', $LANG_MG01['host_environment']);
        $T->parse('CRow1', 'CheckRow1', true);
    }

    $T->set_var('CRow2', '');
    $T->set_var('config_title', $LANG_MG01['mg_dir_structure']);
    $errCount = 0;

    if (! is_writable($_MG_CONF['tmp_path'])) {
        $T->set_var(array('config_item' => 'tmp Path','status' => '<span style="color:red">' .  $LANG_MG01['not_writable'] . '</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
    } else {
        $T->set_var(array('config_item' => 'tmp Path','status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
    }

    $loopy=array('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f');
    $elements = count($loopy);
    for ($i=0; $i<$elements; $i++) {
        if (! is_writable($_MG_CONF['path_mediaobjects'] . 'orig/' . $loopy[$i])) {
            $errCount++;
            $T->set_var(array('config_item' => $_MG_CONF['path_mediaobjects'] . 'orig/' . $loopy[$i],'status' => '<span style="color:red">' . $LANG_MG01['not_writable'] . '</span>'));
            $T->parse('CRow2', 'CheckRow2', true);
        }
    }
    for ($i=0; $i<$elements; $i++) {
        if (! is_writable($_MG_CONF['path_mediaobjects'] . 'disp/' . $loopy[$i])) {
            $T->set_var(array('config_item' => $_MG_CONF['path_mediaobjects'] . 'disp/' . $loopy[$i],'status' => '<span style="color:red">' . $LANG_MG01['not_writable'] . '</span>'));
            $errCount++;
            $T->parse('CRow2', 'CheckRow2', true);
        }
    }
    for ($i=0; $i<$elements; $i++) {
        if (! is_writable($_MG_CONF['path_mediaobjects'] . 'tn/' . $loopy[$i])) {
            $T->set_var(array('config_item' => $_MG_CONF['path_mediaobjects'] . 'tn/' . $loopy[$i],'status' => '<span style="color:red">' . $LANG_MG01['not_writable'] . '</span>'));
            $T->parse('CRow2', 'CheckRow2', true);
            $errCount++;
        }
    }
    if (! is_writable($_MG_CONF['path_mediaobjects'] . 'covers/')) {
        $T->set_var(array('config_item' => $_MG_CONF['path_mediaobjects'] . 'covers/','status' => '<span style="color:red">' . $LANG_MG01['not_writable'] . '</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
        $errCount++;
    }
    if ($errCount == 0) {
        $T->set_var(array('config_item' => $LANG_MG01['mg_directories'],'status' => '<span style="color:green">' . $LANG_MG01['ok'] . '</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
    }
    $T->parse('CRow1', 'CheckRow1', true);

    $T->set_var('CRow2', '');
    $T->set_var('config_title', $LANG_MG01['media_storage']);

    $expectedStorage = MG_getMediaStorageTarget180();
    $activePath = isset($_MG_CONF['path_mediaobjects']) ? rtrim($_MG_CONF['path_mediaobjects'], '/\\') . '/' : '';
    $activeUrl = isset($_MG_CONF['mediaobjects_url']) ? rtrim($_MG_CONF['mediaobjects_url'], '/') : '';
    $expectedPath = $expectedStorage !== false ? rtrim($expectedStorage['path'], '/\\') . '/' : '';
    $pathMatches = $expectedPath !== '' && rtrim(str_replace('\\', '/', $activePath), '/') === rtrim(str_replace('\\', '/', $expectedPath), '/');
    $storageRootOk = $activePath !== '' && is_dir($activePath) && is_readable($activePath) && is_writable($activePath);

    $T->set_var(array(
        'config_item' => $LANG_MG01['active_media_path'],
        'status' => '<code>' . htmlspecialchars($activePath, ENT_QUOTES, 'UTF-8') . '</code> ' . ($storageRootOk ? '<span style="color:green">' . $LANG_MG01['ok'] . '</span>' : '<span style="color:red">' . $LANG_MG01['storage_root_invalid'] . '</span>'),
    ));
    $T->parse('CRow2', 'CheckRow2', true);
    if (!$pathMatches) {
        $T->set_var(array(
            'config_item' => $LANG_MG01['expected_media_path'],
            'status' => $expectedPath === '' ? '<span style="color:red">' . $LANG_MG01['storage_unresolved'] . '</span>' : '<code>' . htmlspecialchars($expectedPath, ENT_QUOTES, 'UTF-8') . '</code> <span style="color:red">' . $LANG_MG01['storage_path_mismatch'] . '</span>',
        ));
        $T->parse('CRow2', 'CheckRow2', true);
    }
    $T->set_var(array(
        'config_item' => $LANG_MG01['active_media_url'],
        'status' => '<a href="' . htmlspecialchars($activeUrl, ENT_QUOTES, 'UTF-8') . '">' . htmlspecialchars($activeUrl, ENT_QUOTES, 'UTF-8') . '</a>',
    ));
    $T->parse('CRow2', 'CheckRow2', true);

    $assetRoot = isset($_MG_CONF['path_mediaassets']) ? rtrim($_MG_CONF['path_mediaassets'], '/\\') . '/' : '';
    $validAssets = 0;
    $invalidAssets = array();
    foreach (MG_getRequiredMediaAssets180() as $asset) {
        $assetPath = $assetRoot . $asset;
        if (MG_validateMediaAsset180($assetPath)) {
            $validAssets++;
        } else {
            $invalidAssets[] = $asset;
        }
    }
    $assetCount = count(MG_getRequiredMediaAssets180());
    $assetStatus = '<code>' . htmlspecialchars($assetRoot, ENT_QUOTES, 'UTF-8') . '</code><br>'
        . '<span style="color:' . (empty($invalidAssets) ? 'green' : 'red') . '">'
        . sprintf($LANG_MG01['valid_media_assets'], $validAssets, $assetCount) . '</span>';
    $T->set_var(array('config_item' => $LANG_MG01['plugin_media_assets'],'status' => $assetStatus));
    $T->parse('CRow2', 'CheckRow2', true);
    foreach ($invalidAssets as $asset) {
        $T->set_var(array('config_item' => htmlspecialchars($asset, ENT_QUOTES, 'UTF-8'),'status' => '<span style="color:red">' . $LANG_MG01['invalid_media_asset'] . '</span>'));
        $T->parse('CRow2', 'CheckRow2', true);
    }

    if ($storageMessage !== '') {
        $T->set_var(array(
            'config_item' => $LANG_MG01['storage_operation'],
            'status' => '<span style="color:' . ($storageSuccess ? 'green' : 'red') . '">' . htmlspecialchars($storageMessage, ENT_QUOTES, 'UTF-8') . '</span>',
        ));
        $T->parse('CRow2', 'CheckRow2', true);
    }
    $T->parse('CRow1', 'CheckRow1', true);

    $T->set_var('CRow2', '');
    $T->set_var('config_title', $LANG_MG01['php_ini_settings']);
    $inichecks = array('upload_max_filesize', 'file_uploads', 'post_max_size', 'max_execution_time','memory_limit', 'max_input_time', 'safe_mode', 'upload_tmp_dir');
    for ($i=0; $i < count($inichecks); $i++) {
        $iniValue = ini_get($inichecks[$i]);
        if ($iniValue === false || $iniValue === '') {
            $iniValue = '&mdash;';
        } else {
            $iniValue = htmlspecialchars((string) $iniValue, ENT_QUOTES, 'UTF-8');
        }
        $T->set_var(array('config_item' => $inichecks[$i],'status' => $iniValue));
        $T->parse('CRow2', 'CheckRow2', true);
    }
    $T->parse('CRow1', 'CheckRow1', true);

    // Count only real historical user media. The explanatory copy itself is
    // taken from the active MediaGallery language file; only the numeric count
    // is generated here.
    $pendingMediaCount = MG_countPendingMediaStorage180();
    $repairStorageHelp = $pendingMediaCount > 0
        ? '<strong>' . (int) $pendingMediaCount . '</strong> &mdash; ' . $LANG_MG01['repair_media_storage_help']
        : $LANG_MG01['repair_media_storage_help'];

    $T->set_var(array(
        'lang_recheck'  => $LANG_MG01['recheck'],
        'lang_continue' => $LANG_MG01['continue'],
        'lang_repair_storage' => $LANG_MG01['repair_media_storage'],
        'repair_storage_help' => $repairStorageHelp,
        'storage_migration_needed' => $pendingMediaCount > 0 ? 'true' : '',
        'media_storage_current' => $LANG_MG01['media_storage_current'],
        'gltoken_name' => CSRF_TOKEN,
        'gltoken' => SEC_createToken(),
    ));

    $T->parse('output', 'admin');
    $retval .= $T->finish($T->get_var('output'));
    return $retval;
}

$mode = '';
if (isset($_POST['mode'])) {
    $mode = COM_applyFilter($_POST['mode']);
} else if (isset ($_GET['mode'])) {
    $mode = COM_applyFilter($_GET['mode']);
}

$storageMessage = '';
$storageSuccess = true;
$action = isset($_POST['action']) ? COM_applyFilter($_POST['action']) : '';

if ($action === 'repair_media_storage') {
    if (!SEC_checkToken()) {
        $storageSuccess = false;
        $storageMessage = $LANG_MG01['invalid_security_token'];
        COM_errorLog('MediaGallery: storage migration rejected because of an invalid CSRF token.', 1);
    } else {
        $target = MG_getMediaStorageTarget180();
        $legacy = MG_getLegacyMediaStorage180();
        if ($target === false || !MG_prepareMediaStorage180($target['path'])) {
            $storageSuccess = false;
            $storageMessage = $LANG_MG01['repair_media_storage_failed'];
        } else {
            $storageSuccess = MG_migrateMediaStorage180($legacy);
            if ($storageSuccess) {
                $storageMessage = $LANG_MG01['repair_media_storage_success'];
                COM_errorLog('MediaGallery: persistent media storage synchronized from ' . $legacy . ' to ' . $target['path'] . '; source files retained.');
            } else {
                $storageMessage = $LANG_MG01['repair_media_storage_failed'];
            }
        }
    }
}

if ($mode == $LANG_MG01['continue']) {
    COM_redirect($_MG_CONF['admin_url'] . 'index.php');
}

$T = new Template($_MG_CONF['template_path']);
$T->set_file('admin', 'administration.thtml');
$T->set_var(array(
    'site_admin_url' => $_CONF['site_admin_url'],
    'site_url'       => $_MG_CONF['site_url'],
    'lang_admin'     => $LANG_MG00['admin'],
    'xhtml'          => XHTML,
    'admin_body'     => MG_checkEnvironment($storageMessage, $storageSuccess),
    'title'          => $LANG_MG01['env_check'],
));
$T->parse('output', 'admin');

$display = COM_startBlock($LANG_MG00['admin'], '', COM_getBlockTemplate('_admin_block', 'header'));
$display .= MG_showAdminMenu('miscellaneous');
$display .= $T->finish($T->get_var('output'));
$display .= COM_endBlock(COM_getBlockTemplate('_admin_block', 'footer'));
$display = COM_createHTMLDocument($display);

COM_output($display);
?>