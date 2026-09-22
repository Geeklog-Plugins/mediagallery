<?php

// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | services.inc.php                                                         |
// |                                                                          |
// | Internal/public service API for MediaGallery                             |
// +--------------------------------------------------------------------------+

if (stripos($_SERVER['PHP_SELF'], basename(__FILE__)) !== false) {
    die('This file can not be used on its own.');
}

/**
 * MediaGallery exposes read-only services through Geeklog's native service
 * mechanism. Album and media discovery are available to other plugins.
 *
 * @return bool
 */
function plugin_wsEnabled_mediagallery()
{
    return true;
}

/**
 * Add one album and, optionally, its descendants to a service result.
 *
 * @param int   $albumId
 * @param int   $depth
 * @param bool  $recursive
 * @param bool  $visibleOnly
 * @param array $output
 * @return void
 */
function MG_serviceCollectAlbumTree180($albumId, $depth, $recursive, $visibleOnly, &$output)
{
    global $_MG_CONF;

    $album = new mgAlbum(intval($albumId));
    if (!$album->valid || $album->access <= 0) {
        return;
    }

    if ($visibleOnly && $album->hidden && $album->access < 3) {
        return;
    }

    $output[] = array(
        'id'       => intval($album->id),
        'title'    => strip_tags($album->title),
        'parent'   => intval($album->parent),
        'owner_id' => intval($album->owner_id),
        'hidden'   => (bool) $album->hidden,
        'access'   => intval($album->access),
        'depth'    => intval($depth),
        'url'      => $_MG_CONF['site_url'] . '/album.php?aid=' . intval($album->id),
    );

    if (!$recursive) {
        return;
    }

    $children = $visibleOnly ? $album->getChildrenVisible() : $album->getChildren();
    foreach ($children as $childId) {
        MG_serviceCollectAlbumTree180($childId, $depth + 1, true, $visibleOnly, $output);
    }
}

/**
 * Return an album tree through Geeklog's native PLG_invokeService API.
 *
 * Supported arguments:
 * - uid: user whose member album tree is requested; defaults to current user
 * - root: 'member' (default) or a numeric album id
 * - recursive: include descendants, default true
 * - visible: omit albums not visible to the current caller, default true
 *
 * @param array $args
 * @param array $output
 * @param array $svc_msg
 * @return int
 */
function service_album_list_mediagallery($args, &$output, &$svc_msg)
{
    global $_TABLES, $_USER, $_MG_CONF;

    require_once __DIR__ . '/include/classAlbum.php';

    $output = array();
    $svc_msg = array();

    $currentUid = isset($_USER['uid']) ? intval($_USER['uid']) : 1;
    $uid = isset($args['uid']) ? intval($args['uid']) : $currentUid;
    $root = isset($args['root']) ? $args['root'] : 'member';
    $recursive = !isset($args['recursive']) || (bool) $args['recursive'];
    $visibleOnly = !isset($args['visible']) || (bool) $args['visible'];

    if ($uid < 1) {
        $svc_msg['error_desc'] = 'Invalid user id.';
        return PLG_RET_ERROR;
    }

    // A user may inspect their own tree. Administrators may request another
    // user's tree for administrative/plugin integration purposes.
    if ($uid !== $currentUid && !SEC_hasRights('mediagallery.admin')) {
        $svc_msg['error_desc'] = 'Not authorized to list albums for this user.';
        return PLG_RET_AUTH_FAILED;
    }

    if ($root === 'member' || $root === '') {
        if (empty($_MG_CONF['member_albums'])) {
            return PLG_RET_OK;
        }

        // Zero is a valid root album id and is the historical/default value.
        $memberRoot = isset($_MG_CONF['member_album_root'])
            ? intval($_MG_CONF['member_album_root'])
            : 0;

        $sql = "SELECT album_id FROM {$_TABLES['mg_albums']} "
             . "WHERE owner_id = " . intval($uid)
             . " AND album_parent = " . $memberRoot
             . " ORDER BY album_order DESC";
        $result = DB_query($sql);

        while ($A = DB_fetchArray($result)) {
            MG_serviceCollectAlbumTree180(
                intval($A['album_id']),
                0,
                $recursive,
                $visibleOnly,
                $output
            );
        }

        return PLG_RET_OK;
    }

    if (!is_numeric($root)) {
        $svc_msg['error_desc'] = 'Invalid album root.';
        return PLG_RET_ERROR;
    }

    $rootId = intval($root);
    if ($rootId < 0) {
        $svc_msg['error_desc'] = 'Invalid album root.';
        return PLG_RET_ERROR;
    }

    $rootAlbum = new mgAlbum($rootId);
    if (!$rootAlbum->valid || ($rootId > 0 && $rootAlbum->access <= 0)) {
        $svc_msg['error_desc'] = 'Album not found or not accessible.';
        return PLG_RET_ERROR;
    }

    $children = $visibleOnly ? $rootAlbum->getChildrenVisible() : $rootAlbum->getChildren();
    foreach ($children as $childId) {
        MG_serviceCollectAlbumTree180($childId, 0, $recursive, $visibleOnly, $output);
    }

    return PLG_RET_OK;
}

/**
 * Return one access-filtered page of media from an album.
 *
 * @param array $args album_id, page and per_page
 * @param array $output
 * @param array $svc_msg
 * @return int
 */
function service_media_list_mediagallery($args, &$output, &$svc_msg)
{
    global $_TABLES, $_MG_CONF;

    require_once __DIR__ . '/include/classAlbum.php';
    require_once __DIR__ . '/include/classMedia.php';

    $output = array('items' => array(), 'pagination' => array());
    $svc_msg = array();

    $albumId = isset($args['album_id']) ? intval($args['album_id']) : 0;
    $page = isset($args['page']) ? max(1, intval($args['page'])) : 1;
    $perPage = isset($args['per_page']) ? intval($args['per_page']) : 24;
    $perPage = max(1, min(100, $perPage));

    if ($albumId <= 0) {
        $svc_msg['error_desc'] = 'Invalid album id.';
        return PLG_RET_ERROR;
    }

    $album = new mgAlbum($albumId);
    if (!$album->valid || $album->access <= 0 || ($album->hidden && $album->access < 3)) {
        $svc_msg['error_desc'] = 'Album not found or not accessible.';
        return PLG_RET_AUTH_FAILED;
    }

    $from = " FROM {$_TABLES['mg_media_albums']} AS ma"
          . " INNER JOIN {$_TABLES['mg_media']} AS m ON m.media_id = ma.media_id"
          . ' WHERE ma.album_id = ' . $albumId;
    $countResult = DB_query('SELECT COUNT(*) AS total' . $from);
    $countRow = DB_fetchArray($countResult);
    $total = isset($countRow['total']) ? intval($countRow['total']) : 0;
    $totalPages = max(1, intval(ceil($total / $perPage)));
    if ($page > $totalPages) {
        $page = $totalPages;
    }

    $offset = ($page - 1) * $perPage;
    $result = DB_query('SELECT m.*' . $from
        . ' ORDER BY ma.media_order ASC LIMIT ' . $offset . ',' . $perPage);

    while ($row = DB_fetchArray($result)) {
        $media = new Media($row, $albumId);
        if (isset($media->access) && $media->access <= 0) {
            continue;
        }
        $thumbnail = $media->displayRawThumb(1);
        $output['items'][] = array(
            'id'            => (string) $media->id,
            'album_id'      => $albumId,
            'title'         => $media->title === '' ? (string) $media->id : strip_tags($media->title),
            'description'   => strip_tags($media->description),
            'media_type'    => intval($media->type),
            'mime_type'     => (string) $media->mime_type,
            'thumbnail_url' => isset($thumbnail[0]) ? $thumbnail[0] : '',
            'media_url'     => $_MG_CONF['site_url'] . '/media.php?f=0&s=' . rawurlencode($media->id),
        );
    }

    $output['pagination'] = array(
        'page'        => $page,
        'per_page'    => $perPage,
        'total_items' => $total,
        'total_pages' => $totalPages,
    );

    return PLG_RET_OK;
}


/**
 * Advertise MediaGallery interoperability capabilities.
 *
 * This is a small, provider-owned declaration following the shared Geeklog
 * memorandum capability convention. Consumers must still use the normal
 * MediaGallery permission checks on every read.
 *
 * @return array
 */
function plugin_getcapabilities_mediagallery()
{
    return array(
        'schema' => 1,
        'roles' => array('content', 'service'),
        'capabilities' => array(
            'content.read',
            'content.collection',
            'content.search',
            'content.url.resolve',
            'content.lifecycle',
            'dashboard.summary',
            'media.album.list',
            'media.album.read',
            'media.item.read',
            'media.item.collection'
        )
    );
}

/**
 * Return one access-filtered album.
 *
 * @param array $args album_id
 * @param array $output
 * @param array $svc_msg
 * @return int
 */
function service_album_read_mediagallery($args, &$output, &$svc_msg)
{
    global $_MG_CONF;

    require_once __DIR__ . '/include/classAlbum.php';

    $output = array();
    $svc_msg = array();

    $albumId = isset($args['album_id']) ? intval($args['album_id']) : 0;
    if ($albumId <= 0) {
        $svc_msg['error_desc'] = 'Invalid album id.';
        return PLG_RET_ERROR;
    }

    $album = new mgAlbum($albumId);
    if (!$album->valid || $album->access <= 0 || ($album->hidden && $album->access < 3)) {
        $svc_msg['error_desc'] = 'Album not found or not accessible.';
        return PLG_RET_AUTH_FAILED;
    }

    $output = array(
        'id'            => 'album:' . $albumId,
        'type'          => 'mediagallery',
        'subtype'       => 'album',
        'title'         => strip_tags($album->title),
        'description'   => strip_tags($album->description),
        'url'           => $_MG_CONF['site_url'] . '/album.php?aid=' . $albumId,
        'canonical_url' => $_MG_CONF['site_url'] . '/album.php?aid=' . $albumId,
        'date-modified' => intval($album->last_update),
        'uid'           => intval($album->owner_id),
        'parent_id'     => intval($album->parent)
    );

    return PLG_RET_OK;
}

/**
 * Return one access-filtered media item.
 *
 * @param array $args media_id and optional album_id
 * @param array $output
 * @param array $svc_msg
 * @return int
 */
function service_media_read_mediagallery($args, &$output, &$svc_msg)
{
    global $_TABLES, $_MG_CONF;

    require_once __DIR__ . '/include/classAlbum.php';
    require_once __DIR__ . '/include/classMedia.php';

    $output = array();
    $svc_msg = array();

    $mediaId = isset($args['media_id']) ? (string) $args['media_id'] : '';
    $requestedAlbumId = isset($args['album_id']) ? intval($args['album_id']) : 0;
    if ($mediaId === '') {
        $svc_msg['error_desc'] = 'Invalid media id.';
        return PLG_RET_ERROR;
    }

    $escapedId = DB_escapeString($mediaId);
    $sql = "SELECT m.*, ma.album_id FROM {$_TABLES['mg_media']} AS m "
         . "INNER JOIN {$_TABLES['mg_media_albums']} AS ma ON ma.media_id=m.media_id "
         . "WHERE m.media_id='" . $escapedId . "'";
    if ($requestedAlbumId > 0) {
        $sql .= ' AND ma.album_id=' . $requestedAlbumId;
    }
    $result = DB_query($sql);

    while ($row = DB_fetchArray($result)) {
        $albumId = intval($row['album_id']);
        $album = new mgAlbum($albumId);
        if (!$album->valid || $album->access <= 0 || ($album->hidden && $album->access < 3)) {
            continue;
        }

        $media = new Media($row, $albumId);
        if (isset($media->access) && $media->access <= 0) {
            continue;
        }

        $thumbnail = $media->displayRawThumb(1);
        $url = $_MG_CONF['site_url'] . '/media.php?f=0&s=' . rawurlencode($media->id);
        $output = array(
            'id'            => (string) $media->id,
            'type'          => 'mediagallery',
            'subtype'       => 'media',
            'album_id'      => $albumId,
            'title'         => $media->title === '' ? (string) $media->id : strip_tags($media->title),
            'description'   => strip_tags($media->description),
            'url'           => $url,
            'canonical_url' => $url,
            'date-modified' => isset($row['media_upload_time']) ? intval($row['media_upload_time']) : 0,
            'uid'           => isset($row['media_user_id']) ? intval($row['media_user_id']) : 0,
            'media_type'    => intval($media->type),
            'mime_type'     => (string) $media->mime_type,
            'thumbnail_url' => isset($thumbnail[0]) ? $thumbnail[0] : '',
            'media_url'     => $url
        );
        return PLG_RET_OK;
    }

    $svc_msg['error_desc'] = 'Media not found or not accessible.';
    return PLG_RET_AUTH_FAILED;
}

/**
 * Return a bounded administration summary for generic dashboards.
 *
 * @param array $args
 * @param array $output
 * @param array $svc_msg
 * @return int
 */
function service_dashboard_summary_mediagallery($args, &$output, &$svc_msg)
{
    global $_TABLES, $_MG_CONF;

    $output = array();
    $svc_msg = array();

    if (!SEC_hasRights('mediagallery.admin') && !SEC_hasRights('mediagallery.config')) {
        $svc_msg['error_desc'] = 'Not authorized to read MediaGallery administration summary.';
        return PLG_RET_AUTH_FAILED;
    }

    $albums = DB_count($_TABLES['mg_albums']);
    $media = DB_count($_TABLES['mg_media']);
    $pending = DB_count($_TABLES['mg_mediaqueue']);

    $alerts = array();
    if (!empty($_MG_CONF['path_mediaobjects']) && !is_writable($_MG_CONF['path_mediaobjects'])) {
        $alerts[] = array(
            'id' => 'storage',
            'status' => 'critical',
            'message' => 'Persistent media storage is not writable.'
        );
    }
    if ($pending > 0) {
        $alerts[] = array(
            'id' => 'pending',
            'status' => 'warning',
            'message' => 'Media submissions are waiting for moderation.',
            'count' => intval($pending)
        );
    }

    $output = array(
        'schema' => 1,
        'status' => empty($alerts) ? 'ok' : 'warning',
        'metrics' => array(
            array('id' => 'albums', 'label' => 'Albums', 'value' => intval($albums)),
            array('id' => 'items', 'label' => 'Media', 'value' => intval($media)),
            array('id' => 'pending', 'label' => 'Pending', 'value' => intval($pending))
        ),
        'alerts' => $alerts,
        'links' => array(
            array('label' => 'Manage MediaGallery', 'url' => $_MG_CONF['admin_url'] . 'index.php')
        ),
        'updated' => time()
    );

    return PLG_RET_OK;
}
