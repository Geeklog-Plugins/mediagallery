<?php
// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | Protected administrator guide.                                           |
// +--------------------------------------------------------------------------+

require_once '../../../lib-common.php';
require_once '../../auth.inc.php';

if (!SEC_hasRights('mediagallery.admin')) {
    COM_errorLog(
        'MediaGallery: unauthorized access attempt to administrator guide by user ' .
        (isset($_USER['uid']) ? intval($_USER['uid']) : 1),
        1
    );

    $display = COM_startBlock($LANG_MG00['access_denied']);
    $display .= $LANG_MG00['access_denied_msg'];
    $display .= COM_endBlock();
    COM_output(COM_createHTMLDocument($display));
    exit;
}

$guide = $_CONF['path'] . 'plugins/mediagallery/docs/ADMIN_GUIDE.html';
if (!is_file($guide) || !is_readable($guide)) {
    COM_errorLog('MediaGallery: administrator guide is missing or unreadable: ' . $guide, 1);
    $guideContent = '<p>The MediaGallery administrator guide is not available.</p>';
} else {
    $guideContent = file_get_contents($guide);
    if ($guideContent === false) {
        COM_errorLog('MediaGallery: failed to read administrator guide: ' . $guide, 1);
        $guideContent = '<p>The MediaGallery administrator guide could not be loaded.</p>';
    }
}

$T = new Template($_MG_CONF['template_path']);
$T->set_file('admin_help', 'admin_help.thtml');
$T->set_var(array(
    'admin_home_url'     => $_MG_CONF['admin_url'] . 'index.php',
    'configuration_url'  => $_CONF['site_admin_url'] . '/configuration.php',
    'lang_admin_home'    => isset($LANG_ADMIN['admin_home']) ? $LANG_ADMIN['admin_home'] : $LANG_MG00['admin'],
    'lang_configuration' => $LANG_MG01['configuration'],
    'guide_content'      => $guideContent
));

$display = COM_startBlock($LANG_MG01['help'], '', COM_getBlockTemplate('_admin_block', 'header'));
$display .= $T->finish($T->parse('output', 'admin_help'));
$display .= COM_endBlock(COM_getBlockTemplate('_admin_block', 'footer'));

$headerCode = '<link rel="stylesheet" type="text/css" href="'
    . $_MG_CONF['site_url'] . '/admin.css">';
$display = COM_createHTMLDocument($display, array('headercode' => $headerCode));
COM_output($display);
