<?php
// +--------------------------------------------------------------------------+
// | Media Gallery Plugin - Geeklog                                           |
// +--------------------------------------------------------------------------+
// | MediaGallery 1.8.0 database schema compatibility                         |
// +--------------------------------------------------------------------------+

if (strpos(strtolower($_SERVER['PHP_SELF']), strtolower(basename(__FILE__))) !== false) {
    die('This file can not be used on its own!');
}

/**
 * Ensure that an upgraded MediaGallery database contains every album column
 * written by mgAlbum::saveAlbum().
 *
 * Some long-lived MediaGallery installations reached later plugin versions
 * without all historical mg_albums ALTER statements having been applied. A
 * fresh install has these columns, but REPLACE INTO then fails on an upgraded
 * site as soon as an album is edited.
 *
 * The repair is deliberately additive: existing columns and data are never
 * altered. Missing columns use the same definitions/defaults as mysql_install.
 *
 * @param bool $force Ignore the one-shot marker and inspect the table anyway.
 * @return bool
 */
function MG_ensureAlbumSchema180($force = false)
{
    global $_TABLES;

    if (empty($_TABLES['mg_albums']) || empty($_TABLES['vars'])) {
        return true;
    }

    // Geeklog's vars.name column is VARCHAR(20), including Geeklog 2.1.1.
    $marker = 'mg_schema180_albums';
    if (!$force) {
        $done = DB_getItem($_TABLES['vars'], 'value', "name = '" . DB_escapeString($marker) . "'");
        if ($done === '1') {
            return true;
        }
    }

    // Do not raise a fatal SQL error when called during a partially completed
    // install where the plugin table has not been created yet.
    $table = $_TABLES['mg_albums'];
    $result = DB_query("SHOW COLUMNS FROM `" . str_replace('`', '``', $table) . "`", 1);
    if ($result === false || DB_error()) {
        return true;
    }

    $present = array();
    while ($row = DB_fetchArray($result)) {
        if (isset($row['Field'])) {
            $present[$row['Field']] = true;
        }
    }

    $required = array(
        'album_id'             => "int(11) NOT NULL default '0'",
        'album_title'          => "varchar(255) NOT NULL default ''",
        'album_desc'           => "text NOT NULL",
        'album_parent'         => "int(11) NOT NULL default '0'",
        'album_order'          => "int(11) NOT NULL default '0'",
        'skin'                 => "varchar(255) NOT NULL default 'default'",
        'hidden'               => "tinyint(4) NOT NULL default '0'",
        'album_cover'          => "varchar(40) NOT NULL default '-1'",
        'album_cover_filename' => "varchar(255) default ''",
        'media_count'          => "int(11) unsigned NOT NULL default '0'",
        'album_disk_usage'     => "bigint(20) unsigned NOT NULL default '0'",
        'last_update'          => "int(11) NOT NULL default '0'",
        'album_views'          => "int(11) NOT NULL default '0'",
        'display_album_desc'   => "tinyint(4) NOT NULL default '0'",
        'enable_album_views'   => "tinyint(4) NOT NULL default '0'",
        'image_skin'           => "varchar(255) NOT NULL default 'default'",
        'album_skin'           => "varchar(255) NOT NULL default 'default'",
        'display_skin'         => "varchar(255) NOT NULL default 'default'",
        'enable_comments'      => "tinyint(4) NOT NULL default '0'",
        'exif_display'         => "tinyint(4) NOT NULL default '0'",
        'enable_rating'        => "tinyint(4) NOT NULL default '0'",
        'playback_type'        => "tinyint(4) NOT NULL default '0'",
        'tn_attached'          => "tinyint(4) NOT NULL default '0'",
        'enable_slideshow'     => "tinyint(4) NOT NULL default '0'",
        'enable_random'        => "tinyint(4) NOT NULL default '0'",
        'enable_views'         => "tinyint(4) NOT NULL default '0'",
        'enable_keywords'      => "tinyint(4) NOT NULL default '0'",
        'enable_sort'          => "tinyint(4) NOT NULL default '0'",
        'enable_rss'           => "tinyint(4) NOT NULL default '0'",
        'albums_first'         => "tinyint(4) NOT NULL default '1'",
        'allow_download'       => "tinyint(4) NOT NULL default '0'",
        'full_display'         => "tinyint(4) NOT NULL default '0'",
        'tn_size'              => "tinyint(4) NOT NULL default '0'",
        'max_image_height'     => "int(11) NOT NULL default '0'",
        'max_image_width'      => "int(11) NOT NULL default '0'",
        'max_filesize'         => "bigint(20) unsigned NOT NULL default '0'",
        'display_image_size'   => "tinyint(4) NOT NULL default '2'",
        'display_rows'         => "tinyint(4) NOT NULL default '3'",
        'display_columns'      => "tinyint(4) NOT NULL default '3'",
        'valid_formats'        => "int(11) unsigned NOT NULL default '65535'",
        'filename_title'       => "tinyint(4) NOT NULL default '0'",
        'shopping_cart'        => "tinyint(4) NOT NULL default '0'",
        'wm_auto'              => "tinyint(4) NOT NULL default '0'",
        'wm_id'                => "int(11) NOT NULL default '0'",
        'wm_opacity'           => "int(11) NOT NULL default '0'",
        'wm_location'          => "tinyint(4) NOT NULL default '0'",
        'album_sort_order'     => "tinyint(4) NOT NULL default '0'",
        'member_uploads'       => "tinyint(4) NOT NULL default '0'",
        'moderate'             => "tinyint(4) NOT NULL default '0'",
        'email_mod'            => "tinyint(4) NOT NULL default '0'",
        'featured'             => "tinyint(4) NOT NULL default '0'",
        'cbposition'           => "tinyint(1) NOT NULL default '0'",
        'cbpage'               => "varchar(20) NOT NULL default ''",
        'owner_id'             => "mediumint(9) NOT NULL default '0'",
        'group_id'             => "mediumint(9) NOT NULL default '0'",
        'mod_group_id'         => "mediumint(9) NOT NULL default '0'",
        'perm_owner'           => "tinyint(1) unsigned NOT NULL default '0'",
        'perm_group'           => "tinyint(1) unsigned NOT NULL default '0'",
        'perm_members'         => "tinyint(1) unsigned NOT NULL default '0'",
        'perm_anon'            => "tinyint(1) unsigned NOT NULL default '0'",
        'podcast'              => "tinyint(4) NOT NULL default '0'",
        'mp3ribbon'            => "tinyint(4) NOT NULL default '0'",
        'tnheight'             => "int NOT NULL default '0'",
        'tnwidth'              => "int NOT NULL default '0'",
        'usealternate'         => "tinyint(4) NOT NULL default '0'",
        'rsschildren'          => "tinyint(4) NOT NULL default '0'",
    );

    $missing = array();
    foreach ($required as $column => $definition) {
        if (!isset($present[$column])) {
            $missing[$column] = $definition;
        }
    }

    if (!empty($missing)) {
        $clauses = array();
        foreach ($missing as $column => $definition) {
            $clauses[] = 'ADD `' . str_replace('`', '``', $column) . '` ' . $definition;
        }

        $sql = "ALTER TABLE `" . str_replace('`', '``', $table) . "` " . implode(', ', $clauses);
        DB_query($sql, 1);
        if (DB_error()) {
            COM_errorLog(
                'Media Gallery 1.8.0: unable to repair mg_albums schema. Missing columns: '
                . implode(', ', array_keys($missing)),
                1
            );
            return false;
        }

        COM_errorLog(
            'Media Gallery 1.8.0: repaired mg_albums schema; added columns: '
            . implode(', ', array_keys($missing))
        );
    }

    DB_save(
        $_TABLES['vars'],
        'name,value',
        "'" . DB_escapeString($marker) . "','1'"
    );

    return true;
}
