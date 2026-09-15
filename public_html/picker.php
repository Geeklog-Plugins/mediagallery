<?php

require_once '../lib-common.php';

if (!in_array('mediagallery', $_PLUGINS)) {
    COM_handle404();
    exit;
}

require_once $_CONF['path'] . 'plugins/mediagallery/include/classAlbum.php';
require_once $_CONF['path'] . 'plugins/mediagallery/include/classMedia.php';

$target = isset($_GET['target']) ? COM_stripslashes($_GET['target']) : '';
if (!preg_match('/^(#[A-Za-z][A-Za-z0-9_-]*|[A-Za-z]+\\[name="[A-Za-z][A-Za-z0-9_-]*"\\])$/', $target)) {
    $target = '';
}

$tag = isset($_GET['tag']) ? COM_applyFilter($_GET['tag']) : 'media';
if (!in_array($tag, array('media', 'img', 'mlink'), true)) {
    $tag = 'media';
}

$albumId = isset($_GET['album_id']) ? intval($_GET['album_id']) : 0;
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$charset = empty($_CONF['default_charset']) ? 'UTF-8' : $_CONF['default_charset'];
$isFrench = isset($_CONF['language']) && strpos($_CONF['language'], 'french') === 0;

$labels = $isFrench
    ? array('title' => 'Ajouter un média', 'album' => 'Album', 'insert' => 'Insérer',
            'empty' => 'Aucun média accessible dans cet album.', 'previous' => 'Précédent',
            'next' => 'Suivant', 'invalid' => 'La destination de l’éditeur est invalide.')
    : array('title' => 'Add media', 'album' => 'Album', 'insert' => 'Insert',
            'empty' => 'No accessible media in this album.', 'previous' => 'Previous',
            'next' => 'Next', 'invalid' => 'The editor target is invalid.');

$_SCRIPTS->setJavaScriptFile('mediagallery-media-picker', $_MG_CONF['site_url'] . '/js/media-picker.js');
$_SCRIPTS->setCSSFile('mediagallery-media-picker', $_MG_CONF['site_url'] . '/media-picker.css');

$albums = array();
$serviceMessage = array();
$status = PLG_invokeService(
    'mediagallery',
    'album_list',
    array('root' => 0, 'recursive' => true, 'visible' => true),
    $albums,
    $serviceMessage
);

if ($status !== PLG_RET_OK) {
    $albums = array();
}

$allowedAlbums = array();
foreach ($albums as $album) {
    $allowedAlbums[intval($album['id'])] = $album;
}

if (!isset($allowedAlbums[$albumId]) && !empty($allowedAlbums)) {
    $albumIds = array_keys($allowedAlbums);
    $albumId = intval($albumIds[0]);
}

$display = '<h1>' . htmlspecialchars($labels['title'], ENT_QUOTES, $charset) . '</h1>';

if ($target === '') {
    $display .= COM_showMessageText($labels['invalid']);
} else {
    $display .= '<form class="mg-picker-toolbar" action="' . htmlspecialchars($_MG_CONF['site_url'] . '/picker.php', ENT_QUOTES, $charset) . '" method="get">'
             . '<input type="hidden" name="target" value="' . htmlspecialchars($target, ENT_QUOTES, $charset) . '">'
             . '<input type="hidden" name="tag" value="' . htmlspecialchars($tag, ENT_QUOTES, $charset) . '">'
             . '<label for="mg-picker-album">' . htmlspecialchars($labels['album'], ENT_QUOTES, $charset) . '</label>'
             . '<select id="mg-picker-album" name="album_id" onchange="this.form.submit()">';

    foreach ($allowedAlbums as $id => $album) {
        $display .= '<option value="' . $id . '"' . ($id === $albumId ? ' selected="selected"' : '') . '>'
                 . str_repeat('&nbsp;&nbsp;', intval($album['depth']))
                 . htmlspecialchars($album['title'], ENT_QUOTES, $charset) . '</option>';
    }
    $display .= '</select><noscript><button type="submit">OK</button></noscript></form>';

    $mediaResult = array();
    $serviceMessage = array();
    $status = PLG_invokeService(
        'mediagallery',
        'media_list',
        array('album_id' => $albumId, 'page' => $page, 'per_page' => 24),
        $mediaResult,
        $serviceMessage
    );

    $items = ($status === PLG_RET_OK && isset($mediaResult['items'])) ? $mediaResult['items'] : array();
    if (empty($items)) {
        $display .= COM_showMessageText($labels['empty']);
    } else {
        $display .= '<div class="mg-picker-grid">';
        foreach ($items as $item) {
            $autotag = MG_buildAutotag($tag, $item['id']);
            $display .= '<article class="mg-picker-card">'
                     . '<img src="' . htmlspecialchars($item['thumbnail_url'], ENT_QUOTES, $charset) . '" alt="" loading="lazy">'
                     . '<p>' . htmlspecialchars($item['title'], ENT_QUOTES, $charset) . '</p>'
                     . '<button type="button" data-mg-target="' . htmlspecialchars($target, ENT_QUOTES, $charset)
                     . '" data-mg-autotag="' . htmlspecialchars($autotag, ENT_QUOTES, $charset) . '">'
                     . htmlspecialchars($labels['insert'], ENT_QUOTES, $charset) . '</button></article>';
        }
        $display .= '</div>';
    }

    if (isset($mediaResult['pagination'])) {
        $pagination = $mediaResult['pagination'];
        $base = $_MG_CONF['site_url'] . '/picker.php?target=' . rawurlencode($target)
              . '&amp;tag=' . rawurlencode($tag) . '&amp;album_id=' . $albumId . '&amp;page=';
        $display .= '<nav class="mg-picker-pagination">';
        if ($page > 1) {
            $display .= '<a href="' . $base . ($page - 1) . '">' . htmlspecialchars($labels['previous'], ENT_QUOTES, $charset) . '</a>';
        }
        if ($page < intval($pagination['total_pages'])) {
            $display .= '<a href="' . $base . ($page + 1) . '">' . htmlspecialchars($labels['next'], ENT_QUOTES, $charset) . '</a>';
        }
        $display .= '</nav>';
    }
}

COM_output(COM_createHTMLDocument($display, array('pagetitle' => $labels['title'])));
