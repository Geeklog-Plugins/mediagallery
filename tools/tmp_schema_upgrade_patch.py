from pathlib import Path

p = Path('autoinstall.php')
s = p.read_text(encoding='utf-8')

post_old = "    require_once $_CONF['path'] . 'plugins/mediagallery/include/config_180.php';\n    if (!MG_migrateMediaStorage180(MG_getLegacyMediaStorage180())) {\n"
post_new = "    require_once $_CONF['path'] . 'plugins/mediagallery/include/config_180.php';\n    require_once $_CONF['path'] . 'plugins/mediagallery/include/schema_180.php';\n    if (!MG_ensureAlbumSchema180(true)) {\n        COM_errorLog('Media Gallery 1.8.0: unable to verify album database schema after install.', 1);\n        return false;\n    }\n    if (!MG_migrateMediaStorage180(MG_getLegacyMediaStorage180())) {\n"
if post_old not in s:
    raise SystemExit('postinstall marker not found')
s = s.replace(post_old, post_new, 1)

upgrade_old = "    require_once $_CONF['path'] . 'plugins/mediagallery/include/config_180.php';\n\n    $target = MG_getMediaStorageTarget180();\n"
upgrade_new = "    require_once $_CONF['path'] . 'plugins/mediagallery/include/config_180.php';\n    require_once $_CONF['path'] . 'plugins/mediagallery/include/schema_180.php';\n\n    if (!MG_ensureAlbumSchema180(true)) {\n        COM_errorLog('Media Gallery 1.8.0: album database schema migration failed.', 1);\n        return 1;\n    }\n\n    $target = MG_getMediaStorageTarget180();\n"
if upgrade_old not in s:
    raise SystemExit('upgrade marker not found')
s = s.replace(upgrade_old, upgrade_new, 1)

p.write_text(s, encoding='utf-8')
