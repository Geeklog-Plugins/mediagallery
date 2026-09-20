# MediaGallery 1.8.0 release notes

MediaGallery 1.8.0 is a major modernization and hardening release for Geeklog. It preserves the mature gallery feature set while updating storage, security, playback, administration, interoperability and compatibility for current Geeklog installations.

## Compatibility

- Geeklog 2.1.1 or newer, including Geeklog 2.2.2.
- PHP 5.6-compatible syntax for the Geeklog 2.1.1 transition line.
- Validation targets also include PHP 7.4, 8.1 and 8.3.
- Existing MediaGallery 1.7.x installations require the documented persistent-media pre-migration before the plugin ZIP upgrade.

## Highlights

- Persistent media storage outside the replaceable plugin public directory.
- Safer 1.7.x upgrades and shared-code multisite isolation.
- Upload, remote-media, FTP, ZIP, CLI, batch and moderation hardening.
- Responsive public/admin interfaces and improved accessibility.
- HTML5-first audio/video playback with obsolete Flash/ActiveX execution removed.
- Canonical URLs, descriptions and conservative media structured data.
- Geeklog-native moderator email through `COM_mail()`.
- Improved album thumbnails and portrait rendering.
- Reusable MediaGallery media picker and permission-filtered album/media discovery.

## Geeklog interoperability

MediaGallery 1.8.0 exposes a shared, consumer-neutral capability contract for Agent, Eclipse, Hub and future integrations.

Current declared capabilities include:

```text
content.read
content.collection
content.search
content.url.resolve
content.lifecycle
dashboard.summary
media.album.list
media.album.read
media.item.read
media.item.collection
```

The plugin provides bounded read-only services for album lists, album reads, media collections, media reads and administration dashboard summaries. Consumers no longer need to know MediaGallery table names or storage paths.

Album lifecycle identifiers use the portable `album:<id>` namespace, while historical media IDs remain unchanged. Save/delete events continue through Geeklog's native lifecycle API so IndexNow, XML Sitemap, Hub and future consumers can react without MediaGallery depending on them.

## Eclipse dashboard support

The `dashboard_summary` service can expose, subject to MediaGallery administration rights:

- album count;
- media count;
- pending moderation count;
- storage-writability alerts;
- pending-moderation alerts;
- the MediaGallery administration link.

This follows the shared Geeklog memorandum dashboard contract rather than an Eclipse-specific API.

## Agent and Hub support

Permission-filtered `album_read` and `media_read` services expose normalized identities, subtypes, canonical URLs, descriptions, dates, ownership and relevant media metadata. The existing Item Info/search/lifecycle APIs remain part of the same interoperability surface.

## Important upgrade note

Before replacing a MediaGallery 1.7.x installation with the 1.8.0 ZIP, migrate legacy media out of:

```text
public_html/mediagallery/mediaobjects/
```

using the supplied migration tool and confirm that the copy/verification succeeds. See `UPGRADE` for the complete procedure.

## Release-candidate validation still required

Before tagging the final release, complete the live matrix documented in `TESTING-1.8.md`, including Geeklog 2.1.1, Geeklog 2.2.2/PHP 8.3, upgrade tests, multisite isolation, moderation, MIME/security checks and validation of the exact generated release archive.
