# MediaGallery 1.8.0 live test checklist

Use the installable archive in `dist/mediagallery_1.8.0_2.1.1.zip` only after the distribution workflow has rebuilt it from the current `modernize-1.8.0` branch.

Record for every failure or warning:

- Geeklog version;
- PHP version;
- MediaGallery action performed;
- relevant album/plugin settings;
- exact warning/error from Geeklog `error.log`;
- whether the result is reproducible.

## Test order

1. Geeklog 2.1.1 first — compatibility baseline.
2. Upgrade from MediaGallery 1.7.3, then 1.7.0.
3. Geeklog 2.2.2 / PHP 8.3 regression.
4. Shared-code multisite isolation.
5. Final RC ZIP install verification.

---

# Phase A — Geeklog 2.1.1

## Fresh installation and administration

- [ ] Install MediaGallery 1.8.0 through the standard plugin installer.
- [ ] Open MediaGallery Configuration.
- [ ] Confirm there is no FlowPlayer option and no obsolete Flash Media configuration tab.
- [ ] Confirm remaining configuration controls load without PHP warnings.
- [ ] Open each MediaGallery administration menu section.
- [ ] Open **Help** and confirm the private administrator guide renders inside Geeklog administration.
- [ ] As a user without `mediagallery.admin`, request `admin/plugins/mediagallery/help.php` directly and confirm access is denied.
- [ ] Confirm there is no obsolete public `/mediagallery/docs/usage.html` dependency.
- [ ] Confirm public gallery pages load before any media is uploaded.

## Albums

- [ ] Create a normal album below Root.
- [ ] Create a sub-album.
- [ ] Edit title, description, permissions and display options.
- [ ] Move a sub-album to another parent.
- [ ] Confirm inherited/explicit permissions remain coherent after movement.
- [ ] Set and reset an album cover.
- [ ] Sort albums manually/static sort.
- [ ] Test Global Album Attribute Editor on a disposable album tree.
- [ ] Test Global Album Permission Editor on a disposable album tree.
- [ ] Delete an album while moving its contents to another valid album.
- [ ] Delete an album with contents and confirm expected permanent removal.
- [ ] Confirm direct media upload to Root Album (`album_id=0`) is refused.

## Image upload and DNC

Use small PNG, GIF, BMP and JPEG samples.

### DNC disabled

With `discard_original = 0` and **Do not convert original to JPG** unchecked:

- [ ] upload PNG/GIF/BMP;
- [ ] confirm upload completes without warning;
- [ ] confirm the retained original is a real JPEG file;
- [ ] confirm its stored extension is `.jpg` and MediaGallery records JPEG MIME data;
- [ ] confirm thumbnail and display images render normally.

### DNC enabled

With **Do not convert original to JPG** checked:

- [ ] upload PNG/GIF/BMP;
- [ ] confirm the original retains its source format and extension;
- [ ] confirm thumbnail and display images render normally.

### Discard original

With `discard_original = 1`:

- [ ] upload one PNG and one JPEG;
- [ ] confirm no orphan original is created;
- [ ] confirm MIME/extension data remains correct;
- [ ] confirm display and thumbnail derivatives remain usable.

## Media management

- [ ] Edit title, description, keywords and category.
- [ ] Change capture time.
- [ ] Attach/remove/replace a thumbnail.
- [ ] Replace an existing media file.
- [ ] Move media to another album.
- [ ] Delete media.
- [ ] Reorder media manually.
- [ ] Run static media sort.
- [ ] Rotate a supported image.
- [ ] Apply a watermark where enabled.
- [ ] Reset views/ratings where available.
- [ ] Verify lifecycle events still occur after these operations.

## Thumbnail and visual regression

Use representative portrait and landscape images.

- [ ] Confirm album cards are sharp at rest.
- [ ] Confirm portraits do not appear artificially square.
- [ ] Confirm hover/mini-lightbox uses the intended source and `contain` behavior.
- [ ] Confirm no permanent thumbnail scale blur is visible.
- [ ] Test bundled gallery skins.
- [ ] Test slideshow keyboard navigation.
- [ ] Test touch/swipe if a touch device is available.
- [ ] Confirm reduced-motion behavior is acceptable.

## Upload security

- [ ] Browser upload with a valid Geeklog CSRF token succeeds.
- [ ] Missing/invalid token on the **initial browser mutation** is rejected.
- [ ] Four simultaneous upload slots preserve their own title, description, keywords, category, attached-thumbnail and DNC values.
- [ ] Executable and suspicious double-extension names are rejected.
- [ ] MIME/extension mismatch for explicitly handled media is rejected.
- [ ] A permitted generic file type still works when allowed by album configuration.
- [ ] FTP import accepts a file inside configured `ftp_path`.
- [ ] FTP import rejects a forged outside path.
- [ ] FTP import rejects an escaping symlink.
- [ ] ZIP import accepts a normal archive.
- [ ] ZIP traversal paths are rejected.
- [ ] ZIP symlinks are rejected.
- [ ] ZIP excessive-entry/declared-size limits fail safely.
- [ ] Recursive CLI import preserves nested directory-to-album mapping.
- [ ] Recursive CLI import rejects symlinks.
- [ ] Remote Media accepts a normal public HTTP(S) target.
- [ ] Remote Media rejects localhost/private/reserved targets.
- [ ] Remote Media rejects unsafe redirects.
- [ ] Remote Media rejects oversized/bounded-download violations.

## Batch-session security

The initial operation and internal continuation use different security models.

### Batch start

- [ ] Start resize/rebuild/media batch with a valid Geeklog CSRF token.
- [ ] Confirm invalid/missing CSRF on the **start operation** is rejected.

### Internal continuation/cancellation

- [ ] Confirm automatic continuation advances the session.
- [ ] Confirm continuation is POST-only and a direct GET is rejected.
- [ ] Confirm a missing `session_id` is rejected.
- [ ] Confirm an invalid `session_id` is rejected.
- [ ] Confirm the session owner can continue/cancel.
- [ ] Confirm another normal user cannot continue/cancel.
- [ ] Confirm an eligible MediaGallery administrator can recover/terminate the session.
- [ ] Confirm continuation does **not** fail merely because Geeklog 2.1.1's referer-bound one-time token was already consumed.

## Stale temporary data

- [ ] Create/reproduce a recent temporary tree and confirm cleanup leaves it alone.
- [ ] Create/reproduce a stale temporary tree and confirm cleanup removes only eligible stale content.
- [ ] Confirm cleanup does not escape MediaGallery temporary storage.

## Image backend failure

- [ ] With the configured image backend intentionally unavailable, upload/resize an image.
- [ ] Confirm MediaGallery returns a clear error instead of an undefined-function/fatal path.
- [ ] Restore the backend and confirm normal image handling resumes.

## Moderation

Use an album with member uploads + moderation enabled.

- [ ] Upload as a normal member and confirm the row is stored in `mg_mediaqueue` plus `mg_media_album_queue`, not active media tables.
- [ ] Confirm the submission appears in Geeklog's native moderation screen.
- [ ] Confirm `mediagallery.admin` can open **Edit** without needing `mediagallery.config`.
- [ ] Confirm that same user cannot access normal configuration without `mediagallery.config`.
- [ ] Edit queued title/description and confirm album binding remains unchanged.
- [ ] Forge a different `album_id` while saving and confirm rejection.
- [ ] Approve and confirm media/album rows move to active tables, queue rows disappear and album counter is correct.
- [ ] Confirm approved media renders normally.
- [ ] Reject a second submission and confirm both queue rows disappear.
- [ ] Confirm rejection removes queued original/display/thumbnail files without touching unrelated media.
- [ ] Confirm moderation mutations are rejected without `mediagallery.admin`.

## Moderator email

- [ ] Configure Geeklog mail backend.
- [ ] Enable moderator notification for a moderated album.
- [ ] Submit media and confirm `COM_mail()` delivery.
- [ ] Confirm plaintext/HTML content is acceptable.
- [ ] Confirm multiple uploads in a short period do not create unexpected mail flooding.

## Member Albums

- [ ] Enable Member Albums.
- [ ] Test self-enrollment.
- [ ] Confirm `phpblock_mg_maenroll()` renders without missing-helper fatal errors.
- [ ] Create a member album through batch-create administration.
- [ ] Confirm member root semantics work when root is `0` and when a dedicated root album is configured.
- [ ] Change a member quota and verify quota reporting.
- [ ] Rebuild quotas.
- [ ] Suspend/reactivate a member-album user if supported by current UI.
- [ ] Purge an empty Member Album on a disposable user.
- [ ] Run reset-member-album flags if applicable and confirm consistency.

## Categories and EXIF/IPTC

- [ ] Create/edit/delete a MediaGallery category.
- [ ] Assign category to media and confirm search/filter behavior.
- [ ] Open EXIF/IPTC administration.
- [ ] Enable representative EXIF fields.
- [ ] Upload/view a JPEG with EXIF metadata and confirm configured fields display correctly.

## RSS, search, comments and Geeklog integration

- [ ] Enable/rebuild full RSS feed if configured.
- [ ] Enable/rebuild album RSS feed.
- [ ] Confirm an anonymously inaccessible album is not leaked by a public feed configuration intended to be public-only.
- [ ] Confirm podcast feed generation works for a representative album if retained.
- [ ] Search for media by title/keyword/category.
- [ ] Confirm Geeklog search integration returns permitted media only.
- [ ] Enable comments and post/view a comment.
- [ ] Confirm What's New media integration.
- [ ] Confirm user-profile integration where enabled.
- [ ] Enable Random Image Block and confirm only eligible media are selected.
- [ ] Test a featured album if retained by current UI.

## Autotags

Use currently supported tags only.

- [ ] `album`
- [ ] `media`
- [ ] `img`
- [ ] `slideshow`
- [ ] legacy `fslideshow` fallback/redirect behavior
- [ ] `video`
- [ ] `audio`
- [ ] `download`
- [ ] `mlink`
- [ ] Confirm album permissions are respected by rendered autotags.
- [ ] Confirm media/album IDs shown to administrators are usable with the documented autotags.

## Legacy media playback

- [ ] Existing MP3 record: HTML5 audio/fallback without PHP warnings.
- [ ] Existing WMA/legacy audio record: safe fallback without PHP warnings.
- [ ] MOV/MP4/MPEG: HTML5 video where supported.
- [ ] SWF: no Flash execution; safe download fallback.
- [ ] FLV: no Flash/FlowPlayer execution; safe download fallback.
- [ ] Old `fslideshow.php` URL redirects to maintained slideshow.

## Persistent media storage

- [ ] Confirm `path_mediaobjects` resolves below `public_html/images/mediagallery/` on a standard single-site install.
- [ ] Upload an image and confirm `orig`, `disp` and `tn` derivatives are there.
- [ ] Confirm placeholder/type assets required by runtime are present.
- [ ] Reinstall/update the same 1.8 ZIP and confirm existing media remain intact.

## Structured data and SEO

- [ ] Validate canonical media URL.
- [ ] Validate canonical paginated album URL.
- [ ] Confirm page-number suffix in paginated title.
- [ ] Confirm meta description derives safely from editorial description.
- [ ] Validate JSON-LD on local image.
- [ ] Validate JSON-LD on local audio.
- [ ] Validate JSON-LD on video with attached thumbnail.
- [ ] Confirm ineligible video/remote/embed cases do not emit unsupported media structured data.

## Album discovery service

Test `PLG_invokeService('mediagallery', 'album_list', ...)`:

- [ ] as anonymous user;
- [ ] as album owner;
- [ ] as non-owner logged-in user;
- [ ] as administrator;
- [ ] with hidden/private albums;
- [ ] with recursive and visible filters;
- [ ] with Member Album root set to `0`.

## Lifecycle / IndexNow integration

With IndexNow 1.3.0 active:

- [ ] Creating/editing a public album emits `PLG_itemSaved('album:<id>', 'mediagallery')`.
- [ ] Making an album private causes `PLG_getItemInfo(..., uid=1)` to expose no public URL.
- [ ] Deleting an album emits `PLG_itemDeleted('album:<id>', 'mediagallery')`, including recursive child deletion.
- [ ] Adding/editing/deleting media keeps media lifecycle events and announces the affected album page.
- [ ] Moving media announces media plus source/destination albums.
- [ ] `plugin_getiteminfo_mediagallery('album:<id>', 'url', 1)` returns a URL only when anonymously readable.
- [ ] `plugin_idToURL_mediagallery()` resolves the expected album URL for save/delete consumers.
- [ ] No direct MediaGallery → IndexNow coupling is required.

## Error log review

At the end of Phase A:

- [ ] Review Geeklog `error.log` from the complete session.
- [ ] Record every MediaGallery-owned warning/notice/fatal.
- [ ] Fix or explicitly classify each finding before starting Phase B.

---

# Phase B — Upgrade from MediaGallery 1.7.x

Run on disposable copies only.

## MediaGallery 1.7.3 → 1.8.0

- [ ] Back up database and `public_html/mediagallery/mediaobjects/`.
- [ ] Extract the 1.8 package without replacing the live plugin yet.
- [ ] Run `php tools/migrate-media-storage.php /path/to/geeklog`.
- [ ] Confirm every source file is copied/verified in persistent destination.
- [ ] Confirm the legacy source remains untouched.
- [ ] Re-run migration and confirm idempotence.
- [ ] Create a conflicting destination file with different size and confirm migration fails without overwrite.
- [ ] Upload/install the 1.8 ZIP only after successful pre-migration.
- [ ] Confirm existing albums/media remain accessible.
- [ ] Confirm titles/descriptions/permissions/owners remain intact.
- [ ] Confirm administrator settings remain intact.
- [ ] Confirm harmless legacy Flash/FlowPlayer rows do not affect runtime.
- [ ] Confirm a database containing only remote-media records does not falsely require local media files.
- [ ] Confirm a second 1.8 ZIP update preserves persistent media.

## MediaGallery 1.7.0 → 1.8.0

- [ ] Repeat the essential migration, upgrade and preservation checks above.

---

# Phase C — Geeklog 2.2.2 / PHP 8.3

- [ ] Fresh install MediaGallery 1.8.0.
- [ ] Open all administration sections including protected Help.
- [ ] Repeat core album create/edit/move/delete flow.
- [ ] Repeat representative image upload + DNC cases.
- [ ] Repeat media edit/move/delete/reorder.
- [ ] Repeat batch ownership/security flow.
- [ ] Repeat moderation + moderator email.
- [ ] Repeat Member Albums essentials.
- [ ] Repeat RSS/search/comments/autotag essentials.
- [ ] Repeat legacy playback/fallback checks.
- [ ] Repeat portrait/landscape visual regression.
- [ ] Repeat `album_list` permission matrix.
- [ ] Repeat IndexNow lifecycle integration.
- [ ] Review `error.log` specifically for PHP 8.2/8.3 warnings/deprecations.
- [ ] Confirm no MediaGallery-owned runtime warning/deprecation remains unexplained.

---

# Phase D — Shared-code multisite

With separate site DB/table prefixes or databases and site-specific Geeklog paths:

- [ ] confirm each site resolves its own `path_images/mediagallery/`;
- [ ] confirm each site resolves its own `images_url`;
- [ ] confirm `path_data/mediagallery/` is site-specific;
- [ ] confirm temporary/upload staging is isolated;
- [ ] upload on Site A and confirm Site B does not see/write/serve that storage;
- [ ] upload on Site B and confirm Site A remains isolated.

---

# Phase E — RC archive

- [ ] Confirm current source tree contains `docs/ADMIN_GUIDE.html` and `admin/help.php`.
- [ ] Confirm obsolete `public_html/docs/usage.html`, Japanese docs and old install docs are absent.
- [ ] Rebuild `dist/mediagallery_1.8.0_2.1.1.zip` from final source.
- [ ] Inspect archive contents.
- [ ] Install the exact RC ZIP once on Geeklog 2.1.1.
- [ ] Install the exact RC ZIP once on Geeklog 2.2.2.
- [ ] Confirm both archive installs pass smoke tests before tagging/releasing the RC.


## Capability declaration and dashboard summary

- [ ] Confirm `plugin_getcapabilities_mediagallery()` returns schema 1 and the documented content/media/dashboard capabilities.
- [ ] Confirm `album_read` returns an accessible album and refuses an inaccessible/hidden album for the caller.
- [ ] Confirm `media_read` returns a visible media item and does not leak an item available only through inaccessible albums.
- [ ] Confirm `media_list` keeps pagination bounded and permission-filtered.
- [ ] Confirm `dashboard_summary` refuses unauthorized users.
- [ ] Confirm `dashboard_summary` returns albums, media and pending metrics for an eligible administrator.
- [ ] Confirm a non-writable persistent storage target produces a dashboard alert without breaking the dashboard.
- [ ] Confirm Eclipse 1.2 consumes the summary without MediaGallery-specific SQL or adapters.
- [ ] Confirm Agent/Hub can consume album/media identity, URLs and descriptions through the public contracts.
- [ ] Repeat the checks on Geeklog 2.1.1 and Geeklog 2.2.2.
