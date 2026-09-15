# MediaGallery documentation

This directory contains the maintained project documentation that belongs with MediaGallery 1.8.0, plus the GPL license text.

The obsolete MediaGallery 1.6/1.7 installation guides, Japanese translations and duplicated legacy archives have been removed from the `modernize-1.8.0` branch. Japanese documentation can be recreated later by the Japanese community if a maintained 1.8 translation is wanted.

## Current 1.8.0 documentation

The primary documentation lives at the repository root:

- [`../README.md`](../README.md) — project overview, compatibility, major 1.8 changes and upgrade preflight;
- [`../UPGRADE`](../UPGRADE) — current 1.7.x → 1.8.0 upgrade rules and persistent-storage migration;
- [`../ROADMAP.md`](../ROADMAP.md) — implementation status and remaining release-candidate work;
- [`../TESTING-1.8.md`](../TESTING-1.8.md) — regression and live-test checklist;
- [`../IMPLEMENTATION_NOTES.md`](../IMPLEMENTATION_NOTES.md) — design and implementation notes.

## Files in `docs/`

| File | Status | Purpose |
| --- | --- | --- |
| `README.md` | Current | Documentation index. |
| `CHANGELOG.md` | Current | MediaGallery 1.8.0 development changelog plus a concise legacy history. |
| `SERVICES.md` | Current | `PLG_invokeService()` and lifecycle-event interoperability contract. |
| `gpl.txt` | Current | GPLv2 license text. |

## Public user documentation

The web-visible documentation has deliberately been reduced to one maintained guide:

- [`../public_html/docs/usage.html`](../public_html/docs/usage.html) — MediaGallery 1.8.0 user/administrator guide.

The 1.8 user guide covers:

- requirements and image-processing backends;
- albums, media items and member albums;
- browser upload, remote media, FTP/ZIP/CLI import behavior;
- media management and Geeklog 2.1.1-compatible batch sessions;
- permissions and moderation;
- HTML5 playback and slideshow behavior;
- search, RSS, SEO, accessibility and structured data;
- persistent media storage and the mandatory 1.7.x pre-migration step;
- Configuration API behavior;
- MediaGallery service/lifecycle interoperability;
- common troubleshooting cases.

## Removed legacy documentation

The following classes of files were intentionally removed because they were obsolete, duplicated or likely to mislead 1.8 users:

- MediaGallery 1.6.x `INSTALL` / `upgrade.html` instructions;
- incomplete legacy configuration documentation under `public_html/docs/english/`;
- the old 1.6-era `usage.html` and Japanese `usage_ja.html` guides;
- `README_ja` and `INSTALL_ja` from the 1.7.x Japanese distribution;
- duplicated files under `docs/older/`;
- the old plain-text excerpted `docs/ChangeLog`;
- empty public documentation placeholders;
- legacy documentation icons/logo no longer used by the rewritten guide.

## Documentation policy for 1.8

MediaGallery 1.8.0 documentation should describe the current code, not preserve obsolete operational instructions merely for historical completeness. Release history is maintained in `CHANGELOG.md`, while installation, upgrade and usage instructions must match the supported Geeklog 2.1.1+ baseline and the persistent-storage model.

Future translations should be based on the maintained 1.8 documents rather than on the removed 1.6/1.7 guides.
