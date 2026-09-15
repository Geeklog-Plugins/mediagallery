<?php

// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | MediaGallery 1.8.0 persistent media storage                             |
// +--------------------------------------------------------------------------+

if (strpos(strtolower($_SERVER['PHP_SELF']), strtolower(basename(__FILE__))) !== false) {
    die('This file can not be used on its own!');
}

/**
 * Resolve the persistent MediaGallery storage introduced in 1.8.0.
 *
 * Media files must live outside public_html/mediagallery because Geeklog's
 * native plugin uploader replaces that entire directory during an upgrade.
 * path_images is the native Geeklog filesystem root. images_url is used when
 * explicitly supplied (notably by shared-code multisite setups); the standard
 * single-site URL falls back to <site_url>/images.
 *
 * @return array|false
 */
function MG_getMediaStorageTarget180()
{
    global $_CONF;

    $pathHtml = isset($_CONF['path_html']) ? rtrim($_CONF['path_html'], '/\\') . '/' : '';
    $siteUrl  = isset($_CONF['site_url']) ? rtrim($_CONF['site_url'], '/') : '';

    if ($pathHtml === '' || $siteUrl === '') {
        COM_errorLog('Media Gallery 1.8.0: unable to resolve path_html/site_url for media storage.', 1);
        return false;
    }

    $imagesPath = !empty($_CONF['path_images'])
        ? rtrim($_CONF['path_images'], '/\\') . '/'
        : $pathHtml . 'images/';

    if (!empty($_CONF['images_url'])) {
        $imagesUrl = rtrim($_CONF['images_url'], '/');
    } else {
        $standardImagesPath = $pathHtml . 'images/';
        if (rtrim(str_replace('\\', '/', $imagesPath), '/') !== rtrim(str_replace('\\', '/', $standardImagesPath), '/')) {
            COM_errorLog(
                'Media Gallery 1.8.0: path_images is custom but images_url is not defined; '
                . 'the public media URL cannot be derived safely.',
                1
            );
            return false;
        }
        $imagesUrl = $siteUrl . '/images';
    }

    return array(
        'path' => $imagesPath . 'mediagallery/',
        'url'  => $imagesUrl . '/mediagallery',
    );
}

/**
 * Return the historical 1.7.x media storage path.
 */
function MG_getLegacyMediaStorage180()
{
    global $_CONF;

    if (empty($_CONF['path_html'])) {
        return '';
    }

    return rtrim($_CONF['path_html'], '/\\') . '/mediagallery/mediaobjects/';
}

/**
 * Count files and bytes below a directory without following symlinks.
 *
 * @return array|false
 */
function MG_inventoryMediaStorage180($root)
{
    $root = rtrim($root, '/\\') . '/';
    $inventory = array();
    $count = 0;
    $bytes = 0;

    if (!is_dir($root)) {
        return array('files' => $inventory, 'count' => 0, 'bytes' => 0);
    }

    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS),
            RecursiveIteratorIterator::LEAVES_ONLY
        );

        foreach ($iterator as $file) {
            if ($file->isLink()) {
                COM_errorLog('Media Gallery 1.8.0: refusing media-storage symlink ' . $file->getPathname(), 1);
                return false;
            }
            if (!$file->isFile()) {
                continue;
            }

            $pathname = $file->getPathname();
            $relative = substr($pathname, strlen($root));
            $segments = preg_split('~[\\\\/]~', $relative);
            if ($relative === false || $relative === '' || in_array('..', $segments, true)) {
                COM_errorLog('Media Gallery 1.8.0: invalid media-storage path ' . $pathname, 1);
                return false;
            }

            $size = $file->getSize();
            $inventory[$relative] = $size;
            $count++;
            $bytes += $size;
        }
    } catch (Exception $e) {
        COM_errorLog('Media Gallery 1.8.0: unable to inventory media storage: ' . $e->getMessage(), 1);
        return false;
    }

    ksort($inventory);

    return array('files' => $inventory, 'count' => $count, 'bytes' => $bytes);
}

/**
 * Return true only for historical user media that belongs in persistent
 * storage. Packaged placeholder files such as index.html are deliberately
 * excluded, even when they live below orig/, disp/, tn/ or covers/.
 */
function MG_isUserMediaFile180($relative)
{
    $normalized = str_replace('\\', '/', (string) $relative);

    if (!preg_match('~^(orig|disp|tn|covers)/~', $normalized)) {
        return false;
    }

    if (strtolower(basename($normalized)) === 'index.html') {
        return false;
    }

    return true;
}

/**
 * Check whether a storage root contains user-generated media rather than only
 * the packaged MediaGallery placeholder/type icons at the root.
 */
function MG_mediaStorageHasUserContent180($root)
{
    $inventory = MG_inventoryMediaStorage180($root);
    if ($inventory === false) {
        return false;
    }

    foreach ($inventory['files'] as $relative => $size) {
        if (MG_isUserMediaFile180($relative)) {
            return true;
        }
    }

    return false;
}

/**
 * Count historical user-media files that still need to be synchronized.
 * Matching files in the persistent target make this check idempotent even
 * though the historical source is deliberately retained.
 *
 * @param string|null $source Optional explicit source directory
 * @return int Number of pending files. Returns 0 when storage cannot be
 *             resolved or inventoried; those errors are logged separately.
 */
function MG_countPendingMediaStorage180($source = null)
{
    $target = MG_getMediaStorageTarget180();
    if ($target === false) {
        return 0;
    }

    if ($source === null || $source === '') {
        $source = MG_getLegacyMediaStorage180();
    }
    if ($source === '') {
        return 0;
    }

    $source = rtrim($source, '/\\') . '/';
    $targetPath = rtrim($target['path'], '/\\') . '/';
    if (rtrim(str_replace('\\', '/', $source), '/')
        === rtrim(str_replace('\\', '/', $targetPath), '/')
    ) {
        return 0;
    }

    $inventory = MG_inventoryMediaStorage180($source);
    if ($inventory === false) {
        return 0;
    }

    $pending = 0;
    foreach ($inventory['files'] as $relative => $expectedSize) {
        if (!MG_isUserMediaFile180($relative)) {
            continue;
        }

        $destination = $targetPath . $relative;
        clearstatcache(true, $destination);
        if (!is_file($destination)
            || is_link($destination)
            || filesize($destination) !== $expectedSize
        ) {
            $pending++;
        }
    }

    return $pending;
}

/**
 * Check whether historical user media still needs to be synchronized.
 *
 * Kept as a boolean compatibility wrapper for existing callers.
 */
function MG_mediaStorageNeedsMigration180($source = null)
{
    return MG_countPendingMediaStorage180($source) > 0;
}

/**
 * Safely copy historical media to the 1.8.0 persistent images directory.
 *
 * The source is never deleted here. Each new file is copied to a temporary
 * sibling, size-checked, then atomically renamed into place. Existing target
 * files are accepted only when their size matches, making retries idempotent
 * while refusing to overwrite conflicting data.
 *
 * @param string|null $source Optional explicit source directory
 * @return bool
 */
function MG_migrateMediaStorage180($source = null)
{
    $target = MG_getMediaStorageTarget180();
    if ($target === false) {
        return false;
    }

    if (!MG_prepareMediaStorage180($target['path'])) {
        COM_errorLog('Media Gallery 1.8.0: destination media storage is not writable: ' . $target['path'], 1);
        return false;
    }

    if ($source === null || $source === '') {
        $source = MG_getLegacyMediaStorage180();
    }
    if ($source === '') {
        return true;
    }

    $source = rtrim($source, '/\\') . '/';
    $targetPath = rtrim($target['path'], '/\\') . '/';

    if (rtrim(str_replace('\\', '/', $source), '/') === rtrim(str_replace('\\', '/', $targetPath), '/')) {
        return true;
    }

    $sourceInventory = MG_inventoryMediaStorage180($source);
    if ($sourceInventory === false) {
        return false;
    }

    // Only user-generated media belongs in persistent storage. Packaged
    // fallback/type images and index.html placeholders remain in the plugin.
    $filtered = array();
    $filteredBytes = 0;
    foreach ($sourceInventory['files'] as $relative => $size) {
        if (!MG_isUserMediaFile180($relative)) {
            continue;
        }
        $filtered[$relative] = $size;
        $filteredBytes += $size;
    }
    $sourceInventory = array(
        'files' => $filtered,
        'count' => count($filtered),
        'bytes' => $filteredBytes,
    );

    // Fresh installs and already-migrated sites may have no historical files.
    if ($sourceInventory['count'] === 0) {
        return true;
    }

    foreach ($sourceInventory['files'] as $relative => $expectedSize) {
        $src = $source . $relative;
        $dst = $targetPath . $relative;
        $dstDir = dirname($dst);

        if (!MG_prepareDirectory180($dstDir)) {
            COM_errorLog('Media Gallery 1.8.0: unable to prepare destination directory ' . $dstDir, 1);
            return false;
        }

        if (file_exists($dst)) {
            if (!is_file($dst) || is_link($dst) || filesize($dst) !== $expectedSize) {
                COM_errorLog('Media Gallery 1.8.0: conflicting destination media file ' . $dst, 1);
                return false;
            }
            continue;
        }

        $tmp = $dst . '.mg180-' . str_replace('.', '', uniqid('', true)) . '.tmp';
        if (!@copy($src, $tmp)) {
            @unlink($tmp);
            COM_errorLog('Media Gallery 1.8.0: unable to copy media file ' . $src . ' to ' . $dst, 1);
            return false;
        }

        clearstatcache(true, $tmp);
        if (!is_file($tmp) || filesize($tmp) !== $expectedSize) {
            @unlink($tmp);
            COM_errorLog('Media Gallery 1.8.0: copied media file failed size verification ' . $src, 1);
            return false;
        }

        if (!@rename($tmp, $dst)) {
            @unlink($tmp);
            COM_errorLog('Media Gallery 1.8.0: unable to finalize media file ' . $dst, 1);
            return false;
        }
    }

    // Final file-by-file validation. The source remains untouched until the
    // caller/core upgrade mechanism decides it is safe to remove old code.
    foreach ($sourceInventory['files'] as $relative => $expectedSize) {
        $dst = $targetPath . $relative;
        clearstatcache(true, $dst);
        if (!is_file($dst) || is_link($dst) || filesize($dst) !== $expectedSize) {
            COM_errorLog('Media Gallery 1.8.0: final verification failed for ' . $dst, 1);
            return false;
        }
    }

    COM_errorLog(
        'Media Gallery 1.8.0: safely migrated ' . $sourceInventory['count']
        . ' media files (' . $sourceInventory['bytes'] . ' bytes) from '
        . $source . ' to ' . $targetPath
    );

    return true;
}

/**
 * Return the packaged images required when a requested media file is missing.
 */
function MG_getRequiredMediaAssets180()
{
    return array(
        'audio.png',
        'empty.png',
        'flash.png',
        'flv.png',
        'generic.png',
        'googlevideo.png',
        'missing.png',
        'pdf.png',
        'quicktime.png',
        'remote.png',
        'video.png',
        'wmp.png',
        'youtube.png',
        'zip.png',
    );
}

/**
 * Verify that a file is a readable image with usable dimensions.
 */
function MG_validateMediaAsset180($filename)
{
    if (!is_file($filename) || is_link($filename) || !is_readable($filename)) {
        return false;
    }

    $size = @getimagesize($filename);
    return is_array($size)
        && isset($size[0], $size[1])
        && (int) $size[0] > 0
        && (int) $size[1] > 0;
}
