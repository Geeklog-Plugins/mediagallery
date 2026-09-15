# MediaGallery documentation inventory

This directory contains a mixture of current MediaGallery 1.8.0 development documentation and historical documentation inherited from older MediaGallery releases.

Only documents explicitly listed as **current** below should be treated as authoritative for MediaGallery 1.8.0.

## Current 1.8.0 documentation

The main current documents live at the repository root:

- [`../README.md`](../README.md) — project overview, compatibility, storage and upgrade preflight;
- [`../ROADMAP.md`](../ROADMAP.md) — implementation status and remaining release-candidate work;
- [`../TESTING-1.8.md`](../TESTING-1.8.md) — regression/live-test checklist;
- [`../IMPLEMENTATION_NOTES.md`](../IMPLEMENTATION_NOTES.md) — design and implementation notes;
- [`SERVICES.md`](SERVICES.md) — public `PLG_invokeService()` and lifecycle-event interoperability contract.

## Files in `docs/`

| File | Status for 1.8.0 | Notes |
| --- | --- | --- |
| `SERVICES.md` | **Current** | Maintained 1.8 interoperability documentation. |
| `ChangeLog` | Historical reference | Useful release history through 1.7.x, but it is not yet the final 1.8 changelog. |
| `INSTALL` | **Obsolete** | Describes MediaGallery 1.6.10, Geeklog 1.4 and PHP 4-era installation. Do not use for 1.8. |
| `INSTALL_ja` | **Obsolete** | Historical Japanese installation documentation; must not be used for a 1.8 upgrade. |
| `gpl.txt` | Relevant license copy | GPLv2 license text; still relevant. |
| `older/` | Historical archive | Retained only for project history/reference. |

The root `README_ja` is also historical (1.7.2.4-era) and requires a separate translation/update decision before 1.8 RC.

## `public_html/docs/` audit

The files below are installed under the web-visible MediaGallery tree. They are therefore more problematic when stale because administrators can mistake them for current 1.8 documentation.

| Path | Status | Recommendation before 1.8 RC |
| --- | --- | --- |
| `public_html/docs/index.html` | Empty placeholder | Remove unless required to prevent directory listing on a supported server configuration. |
| `public_html/docs/upgrade.html` | **Obsolete** | MediaGallery 1.6.0-era install/upgrade guide. Remove from the public package or replace with current 1.8 instructions. |
| `public_html/docs/english/mediagallery.html` | **Obsolete/incomplete** | Contains stale configuration references and placeholder descriptions. Remove from the public package or rewrite. |
| `public_html/docs/usage.html` | Mixed historical value | Large 1.6-era user guide. Some conceptual sections (albums, media, permissions, autotags) remain useful, but installation, configuration, storage, batch and playback sections are outdated. Review before deciding whether to modernize or archive. |
| `public_html/docs/usage_ja.html` | Mixed historical value | Japanese historical user guide; same issue as `usage.html`, plus translation maintenance. |
| `public_html/docs/images/` | Depends on legacy guides | Keep only if a retained/modernized guide still references the images. |
| `public_html/docs/mediaGallery_logo.png` | Cosmetic/historical | Keep only if a current document uses it. |

### Why the old public guides are not authoritative

The legacy public documentation predates major 1.8 changes, including:

- Geeklog 2.1.1+ as the supported baseline;
- persistent storage below Geeklog's image root rather than the replaceable plugin directory;
- the mandatory 1.7.x media pre-migration step before ZIP upgrades;
- removal of active Flash/ActiveX playback paths;
- current upload/import security behavior;
- Geeklog-native Configuration API usage;
- current batch-session behavior on Geeklog 2.1.1;
- current public service/lifecycle interoperability APIs.

## RC documentation cleanup plan

Before MediaGallery 1.8.0 RC:

1. keep the repository root `README.md` as the primary entry point;
2. create/retain one current install/upgrade guide focused on 1.7.x → 1.8.0 and fresh 1.8.0 installs;
3. remove obsolete install/configuration documents from the web-visible package;
4. decide whether `usage.html` is worth modernizing or should move to a clearly labelled historical archive;
5. update the final changelog with the 1.8.0 modernization work;
6. decide whether Japanese documentation is updated for 1.8.0 or explicitly shipped as legacy-only material.
