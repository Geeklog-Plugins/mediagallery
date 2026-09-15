# MediaGallery documentation

This directory contains the maintained project and administrator documentation for MediaGallery 1.8.0, plus the GPL license text.

The obsolete MediaGallery 1.6/1.7 installation guides, Japanese translations and duplicated legacy archives have been removed from the `modernize-1.8.0` branch. Japanese documentation can be recreated later by the Japanese community if a maintained 1.8 translation is wanted.

## Current 1.8.0 documentation

The primary development/release documentation lives at the repository root:

- [`../README.md`](../README.md) — project overview, compatibility, major 1.8 changes and upgrade preflight;
- [`../UPGRADE`](../UPGRADE) — current 1.7.x → 1.8.0 upgrade rules and persistent-storage migration;
- [`../ROADMAP.md`](../ROADMAP.md) — implementation status and remaining release-candidate work;
- [`../TESTING-1.8.md`](../TESTING-1.8.md) — regression and live-test checklist;
- [`../IMPLEMENTATION_NOTES.md`](../IMPLEMENTATION_NOTES.md) — design and implementation notes.

## Files in `docs/`

| File | Status | Purpose |
| --- | --- | --- |
| `README.md` | Current | Documentation index. |
| `ADMIN_GUIDE.html` | Current/private | Administrator guide rendered only through protected MediaGallery administration. |
| `CHANGELOG.md` | Current | MediaGallery 1.8.0 development changelog plus a concise legacy history. |
| `SERVICES.md` | Current | `PLG_invokeService()` and lifecycle-event interoperability contract. |
| `gpl.txt` | Current | GPLv2 license text. |

## Administrator guide

The MediaGallery guide is intentionally **not stored in the public web tree**.

The Help item in the MediaGallery administration menu points to:

```text
/admin/plugins/mediagallery/help.php
```

That endpoint:

1. loads Geeklog normally;
2. requires the `mediagallery.admin` right;
3. loads the private `docs/ADMIN_GUIDE.html` fragment from the plugin directory;
4. renders it inside the normal Geeklog/MediaGallery administration interface.

This keeps operational documentation available where administrators expect it without publishing a static `/mediagallery/docs/usage.html` URL to all site visitors.

The administrator guide covers requirements, albums/media, upload/import security, batch processing, permissions, moderation, playback, SEO/accessibility, persistent storage, upgrade preflight, configuration, interoperability and troubleshooting.

## Removed legacy/public documentation

The following classes of files were intentionally removed because they were obsolete, duplicated or unnecessarily public:

- MediaGallery 1.6.x `INSTALL`, `upgrade.html` and old `install_doc*.html` instructions;
- incomplete legacy configuration documentation under `public_html/docs/english/`;
- the old public `usage.html` and Japanese `usage_ja.html` guides;
- `README_ja` and `INSTALL_ja` from the 1.7.x Japanese distribution;
- duplicated files under `docs/older/`;
- the old plain-text excerpted `docs/ChangeLog`;
- empty public documentation placeholders;
- legacy documentation icons/logo no longer used.

The `public_html/docs/` tree is no longer needed for administrator documentation in 1.8.0.

## Documentation policy for 1.8

MediaGallery 1.8.0 documentation should describe the current code and should be exposed only to the audience that needs it. Repository development/release documentation stays with the source tree; administrator operational help is private and rendered through an authenticated plugin-admin endpoint.

Release history is maintained in `CHANGELOG.md`. Installation, upgrade and administrative instructions must match the Geeklog 2.1.1+ baseline and the persistent-storage model.

Future translations should be based on the maintained 1.8 documents rather than on the removed 1.6/1.7 guides.
