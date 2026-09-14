<?php
// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | MediaGallery 1.8.0 bootstrap                                             |
// +--------------------------------------------------------------------------+

if (strpos(strtolower($_SERVER['PHP_SELF']), strtolower(basename(__FILE__))) !== false) {
    die('This file can not be used on its own!');
}

/*
 * Keep the proven 1.7.3 implementation intact while the 1.8.0 modernization
 * is introduced in controlled layers. This transitional include can be folded
 * back into functions.inc once the configuration/template refactor is stable.
 */
require_once __DIR__ . '/include/input_compat_180.php';
require_once __DIR__ . '/functions_legacy.inc';
require_once __DIR__ . '/include/config_180.php';
require_once __DIR__ . '/include/email_180.php';
require_once __DIR__ . '/include/upload_security_180.php';
require_once __DIR__ . '/include/tmp_cleanup_180.php';
require_once __DIR__ . '/services.inc.php';

/*
 * MediaGallery 1.8 card-preview corrections are kept in a small override while
 * the legacy stylesheet remains intact. More-specific selectors prevent the
 * generic card hover zoom from scaling the complete portrait preview.
 */
if (isset($_SCRIPTS) && is_object($_SCRIPTS)) {
    $cardPreviewCssPath = $_CONF['path_html'] . 'mediagallery/card-preview-1.8.css';
    $cardPreviewCssVersion = @filemtime($cardPreviewCssPath);
    if ($cardPreviewCssVersion === false) {
        $cardPreviewCssVersion = '1.8.0';
    }
    $_SCRIPTS->setCSSFile(
        'mg.cardpreview180',
        '/mediagallery/card-preview-1.8.css?v=' . rawurlencode($cardPreviewCssVersion),
        false
    );
}

MG_addConfigLanguage180();
MG_ensureConfig180();
MG_applyRuntimeConfiguration180();
MG_cleanupStaleTemp180();