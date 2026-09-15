# MediaGallery 1.8.0 Roadmap

MediaGallery 1.8.0 is a modernization, hardening and interoperability release. It keeps the existing MediaGallery data model and upgrade path while making the plugin safer on current Geeklog/PHP installations, moving user media out of the replaceable plugin directory, modernizing the public UI and exposing cleaner integration points to the Geeklog ecosystem.

**Development branch:** `modernize-1.8.0`  
**Geeklog baseline:** 2.1.1 or newer  
**Compatibility policy:** keep PHP 5.6-compatible syntax for legacy Geeklog 2.1.1 deployments while validating PHP 7.4, 8.1 and 8.3.

The implementation is now largely complete. Remaining work is mainly live regression testing, upgrade validation, documentation cleanup and final release-candidate packaging.

## Current status

### Completed foundations

- [x] Geeklog 2.1.1+ baseline without Geeklog core modifications.
- [x] PHP 5.6-compatible source syntax with PHP 7.4/8.1/8.3 lint coverage.
- [x] Persistent media storage outside `public_html/mediagallery/`.
- [x] Shared-code multisite isolation through each site's Geeklog paths/URLs.
- [x] Safe 1.7.x media pre-migration tool.
- [x] Configuration API cleanup and removal of obsolete fresh-install Flash/FlowPlayer settings.
- [x] Upload/import/remote-media hardening.
- [x] Modern HTML5 playback fallbacks.
- [x] Geeklog-native moderator mail transport.
- [x] Responsive public/admin templates, accessibility and SEO improvements.
- [x] Structured data for media where MediaGallery owns reliable metadata.
- [x] Public `album_list` service through `PLG_invokeService()`.
- [x] Media and album lifecycle notifications through Geeklog plugin APIs.
- [x] Installable 1.8.0 test ZIP generation and validation.

### Remaining before RC

- [ ] Complete the final live regression matrix on Geeklog 2.1.1 and 2.2.2.
- [ ] Complete live PHP 8.2/8.3 warning/deprecation validation.
- [ ] Validate disposable upgrades from MediaGallery 1.7.0 and 1.7.3.
- [ ] Complete live moderation, mail, MIME mismatch, stale-temp and service permission tests.
- [ ] Finish documentation cleanup and remove/archive misleading legacy public documentation.
- [ ] Decide whether `functions_legacy.inc` should remain as the transitional implementation layer for 1.8.0 RC.
- [ ] Build and validate the final RC archive.

## 1. Compatibility and bootstrap

- [x] Require Geeklog 2.1.1 or newer.
- [x] Preserve compatibility with Geeklog 2.2.2.
- [x] Avoid Geeklog core changes.
- [x] Preserve existing database content and administrator configuration during upgrade.
- [x] Complete the static PHP 8.x audit of MediaGallery-owned hot paths.
- [x] Keep plugin bootstrap syntax compatible with PHP 5.6.
- [x] Correct legacy PHP block dependency loading: `phpblock_mg_maenroll()` now loads the MediaGallery helpers it needs instead of relying on page-specific bootstrap order.
- [x] Keep `phpblock_mg_randommedia()` and member-album block behavior compatible with Geeklog 2.1.1.
- [ ] Complete the live PHP 8.2/8.3 runtime warning/deprecation audit.
- [ ] Run the final Geeklog 2.1.1 / 2.2.2 regression matrix.

## 2. Persistent media storage and multisite

Media files are persistent user data and no longer live inside the replaceable plugin public directory.

```php
$_MG_CONF['path_mediaobjects'] = rtrim($_CONF['path_images'], '/\\') . '/mediagallery/';
```

The historical `public_html/mediagallery/mediaobjects/` location is a migration source only.

- [x] Centralize storage path/URL resolution.
- [x] Store 1.8 public media below `path_images/mediagallery/`.
- [x] Isolate shared-code multisite media through `path_images` / `images_url`.
- [x] Isolate private temporary/upload data below each site's `path_data/mediagallery/`.
- [x] Avoid `HTTP_HOST`-derived site identity.
- [x] Create required directories with explicit error handling.
- [x] Implement copy-and-verify legacy media migration.
- [x] Never remove the legacy source automatically.
- [x] Refuse conflicting destination files instead of overwriting them.
- [x] Provide `tools/migrate-media-storage.php` for 1.7.x pre-migration.
- [x] Propagate migration failures to the installer/upgrader.
- [x] Confirm subsequent plugin ZIP replacement preserves media already stored below Geeklog images.
- [ ] Validate the pre-migration path on disposable 1.7.0 and 1.7.3 installations.

### Legacy ZIP upgrade rule

Geeklog replaces the old public plugin directory before loading the new plugin's upgrade code. A 1.7.x installation still storing media below `public_html/mediagallery/mediaobjects/` must therefore run the provided pre-migration tool before uploading the 1.8 ZIP.

## 3. Configuration cleanup

- [x] Add `include/config_180.php` for runtime configuration and migration.
- [x] Add missing Configuration API entries without resetting valid existing values.
- [x] Keep runtime-derived paths and URLs outside administrator-editable configuration.
- [x] Remove fresh-install FlowPlayer and Flash controls.
- [x] Remove playback controls with no useful HTML5 equivalent from maintained interfaces.
- [x] Preserve harmless legacy configuration rows on upgraded sites where automatic deletion is not yet proven safe.
- [ ] Decide whether obsolete 1.7.x Flash/FlowPlayer rows can be removed safely on both supported Geeklog lines.

## 4. Upload, import, batch and remote-media security

- [x] Geeklog CSRF protection on browser upload, Remote Media and FTP import entry forms.
- [x] Correct browser slot association for captions, descriptions, keywords, categories, thumbnails and DNC.
- [x] Preserve originals correctly when DNC requests it.
- [x] Perform real format conversion instead of MIME/extension-only changes.
- [x] Reject unsafe executable/server-side filenames.
- [x] Defense-in-depth validation inside `MG_getFile()`.
- [x] Constrain FTP sources with `realpath()` and reject escaping symlinks.
- [x] Harden recursive CLI imports and preserve nested directory-to-album mapping.
- [x] Harden ZIP extraction against traversal, unsafe temp paths, symlinks, excessive entry counts and oversized declared payloads.
- [x] Restrict Remote Media to bounded public HTTP(S) resources and reject localhost/private/reserved targets and redirects.
- [x] Prevent uploads into the synthetic Root Album (`album_id=0`).
- [x] Prefer content-derived MIME detection and validate explicitly handled MIME/extension pairs.
- [x] Clean deterministic upload failure and image-conversion temporary files.
- [x] Add conservative stale-temp cleanup for interrupted requests.
- [x] Protect album/global/watermark/sort/resize/rebuild/media-manager mutations with appropriate access and CSRF checks.
- [x] Bind posted media IDs to the authorized album before manager, batch and normal edit mutations.
- [x] Remove the orphaned legacy batch-caption mutation.
- [x] Repair Geeklog-native moderation approval/rejection and queued media promotion/removal.
- [x] Remove the orphaned asynchronous upload endpoint and unused `MG_saveUpload()` path.

### Geeklog 2.1.1 batch compatibility

- [x] Keep batch start operations protected by normal Geeklog CSRF validation.
- [x] Make batch continuation/cancellation POST-only.
- [x] Validate the server-generated batch `session_id` and session ownership on every continuation.
- [x] Allow administrator override only where already permitted by MediaGallery.
- [x] Do not require Geeklog 2.1.1's referer-bound one-time token for internal batch continuation, avoiding false “security token expired” failures.

### Remaining live security tests

- [ ] MIME mismatch rejection and generic-file compatibility.
- [ ] Stale-temp cleanup with recent vs stale trees.
- [ ] Full moderation upload/edit/approve/reject flow.
- [ ] Batch continuation/cancellation as owner, another user and administrator.

## 5. Image processing

- [x] Confirm image upload on Geeklog 2.1.1 / PHP 5.6 with GD installed.
- [x] Store generated image derivatives under persistent `images/mediagallery/` storage.
- [x] Centralize GD, ImageMagick and NetPBM capability detection.
- [x] Guard resize, conversion, rotation and watermark operations before backend-specific calls.
- [x] Return a clear error when the configured image backend is unavailable.
- [ ] Validate the missing-backend error live once with GD intentionally disabled on the 2.1.1/PHP 5.6 test instance.

## 6. Playback modernization

- [x] Remove executable Flash playback from default rendering.
- [x] Replace QuickTime/Windows Media ActiveX paths with HTML5 playback or download fallback.
- [x] Route MPEG/MOV/MP4 through maintained HTML5 rendering.
- [x] Use HTML5 audio for supported audio where meaningful.
- [x] Replace FLV/SWF execution with safe download fallbacks.
- [x] Retire generated `mms:` links.
- [x] Replace obsolete XSPF/Flash play-all paths with maintained album/playlist behavior.
- [x] Redirect old `fslideshow.php` entry points to the maintained slideshow.
- [x] Remove unused SWF binaries, SWFObject helpers and obsolete duplicate assets.
- [x] Preserve legacy playback rows only as upgrade/custom-skin compatibility data.

## 7. Email modernization

- [x] Replace bundled PHPMailer moderator notifications.
- [x] Use Geeklog `COM_mail()`.
- [x] Provide HTML and plaintext templates.
- [x] Preserve notification permissions and throttling.
- [ ] Complete a live moderator-email test through the configured Geeklog backend.

## 8. Templates, accessibility, image quality and SEO

- [x] Replace legacy slideshow chrome with a native responsive lightbox-style viewer.
- [x] Add semantic H1 album titles and improved heading hierarchy.
- [x] Add navigation landmarks and labelled search/admin controls.
- [x] Modernize album, media, search, file-list, podcast and bundled gallery skins.
- [x] Replace presentation tables where maintained public forms can use semantic responsive markup.
- [x] Improve escaping of attributes, edit values, links and translated confirmation text.
- [x] Add canonical media URLs.
- [x] Add self-canonical album pagination and exclude sort variants.
- [x] Add page-number suffixes to paginated album titles.
- [x] Add canonical-safe meta descriptions from existing album/media editorial descriptions.
- [x] Add conservative media JSON-LD (`ImageObject`, `AudioObject`, eligible `VideoObject`).
- [x] Avoid album-level generic page schema where ownership may belong to Geeklog/theme output.
- [x] Improve album-card thumbnail sharpness by using the original local image as the visual source when available, cropping with `object-fit` rather than scaling small square derivatives.
- [x] Remove persistent thumbnail/lightbox scale transforms that amplified blur and made portrait media appear artificially square.
- [ ] Complete final visual regression across the bundled skins and representative portrait/landscape media.

## 9. Interoperability and public API

MediaGallery exposes content to other Geeklog plugins through Geeklog APIs rather than requiring direct access to `mg_*` tables.

### Album discovery service

```php
PLG_invokeService(
    'mediagallery',
    'album_list',
    array(
        'uid'       => $uid,
        'root'      => 'member',
        'recursive' => true,
        'visible'   => true,
    ),
    $output,
    $svc_msg
);
```

- [x] Implement `album_list` through `PLG_invokeService()`.
- [x] Reuse MediaGallery permissions and album-tree rules.
- [x] Preserve valid `member_album_root = 0` semantics.
- [ ] Complete live tests as owner, non-owner, anonymous user and administrator.

### Content lifecycle events

Media IDs keep their historical raw IDs for backward compatibility. Albums use the portable namespace `album:<id>` so Geeklog 2.1.1 can distinguish album objects without relying on the newer `sub_type` argument.

- [x] Keep existing media `PLG_itemSaved()` events.
- [x] Keep media `PLG_itemDeleted()` events.
- [x] Emit `PLG_itemSaved('album:<id>', 'mediagallery')` on album creation/update.
- [x] Emit `PLG_itemDeleted('album:<id>', 'mediagallery')` on album deletion, including recursive child deletion.
- [x] Notify affected album pages when media are added, edited, deleted or reordered.
- [x] Notify source and destination albums when media are moved.
- [x] Notify old/new parent album listings when albums are moved.
- [x] Extend `plugin_getiteminfo_mediagallery()` to resolve namespaced album objects.
- [x] Return anonymous album URLs only for publicly readable, non-hidden albums.
- [x] Extend `plugin_idToURL_mediagallery()` so consumers can resolve deterministic album URLs, including deletion notifications.
- [x] Deduplicate repeated album lifecycle notifications during a single request.
- [x] Keep the implementation generic: MediaGallery does not call IndexNow directly.
- [ ] Live-test the full chain with IndexNow 1.3.0 on Geeklog 2.1.1 and 2.2.2.

This contract is intended to serve IndexNow, XML Sitemap, Hub and future connectors without coupling MediaGallery to any one consumer.

See `docs/SERVICES.md` for the service and lifecycle API contract.

## 10. Code modernization and cleanup

- [x] Prefer Geeklog APIs over duplicate internal mechanisms where practical.
- [x] Add Geeklog 2.1.1 input compatibility without core changes.
- [x] Centralize 1.8 runtime/storage/security/interoperability helpers.
- [x] Remove dead Flash/ActiveX playback paths already replaced.
- [x] Complete the static PHP 8.x warning/deprecation cleanup in owned hot paths.
- [x] Harden ZIP extraction and recursive CLI paths.
- [ ] Complete live PHP 8.2/8.3 warning/deprecation validation.
- [ ] Decide whether folding `functions_legacy.inc` back into a single final bootstrap is worth the regression risk before RC.
- [ ] Remove only compatibility branches proven dead for the final supported matrix.

## 11. Documentation

### Current 1.8 documentation

- [x] `ROADMAP.md` tracks implementation and RC status.
- [x] `README.md` is the repository landing page for the 1.8 branch.
- [x] `TESTING-1.8.md` contains the regression checklist.
- [x] `IMPLEMENTATION_NOTES.md` records implementation details and design decisions.
- [x] `docs/SERVICES.md` documents the supported plugin service/interoperability API.

### Legacy documentation audit

- [x] Identify `docs/INSTALL` as obsolete (MediaGallery 1.6.10 / Geeklog 1.4 / PHP 4-era requirements).
- [x] Identify `public_html/docs/upgrade.html` as obsolete (MediaGallery 1.6.0-era installation instructions).
- [x] Identify `public_html/docs/english/mediagallery.html` as incomplete legacy configuration documentation with stale references.
- [x] Keep historical changelogs available as project history, clearly separated from 1.8 instructions.
- [ ] Decide whether the large `public_html/docs/usage*.html` guides contain enough still-valid end-user material to modernize, or move them to a clearly labelled legacy archive.
- [ ] Remove obsolete installation/configuration documents from the public installable tree before RC so they cannot contradict 1.8 instructions.
- [ ] Refresh upgrade/install documentation around the persistent-storage preflight and current Geeklog baseline.

## 12. Distribution

- [x] Use one installable archive: `dist/mediagallery_1.8.0_2.1.1.zip`.
- [x] Keep one top-level `mediagallery/` directory in the ZIP.
- [x] Exclude `.github/`, `dist/`, `.gitignore` and build-only content.
- [x] Validate archive filenames against Geeklog 2.2.2 filename rules.
- [x] Validate required 1.8 migration/storage helpers in the archive.
- [x] Automatically rebuild the test archive after validated branch changes without creating build loops.
- [ ] Ensure obsolete public documentation is not shipped in the RC archive.
- [ ] Rebuild and validate the final RC archive after source/documentation cleanup.

## 13. Release-candidate validation matrix

### Fresh installs

- [ ] Fresh 1.8.0 on Geeklog 2.1.1.
- [ ] Fresh 1.8.0 on Geeklog 2.2.2.
- [ ] Confirm Configuration UI has no obsolete Flash/FlowPlayer controls.
- [ ] Confirm upload/edit/delete, thumbnail generation, RSS, search and comments.
- [ ] Confirm clear failure when no image backend is available.

### Upgrades

- [ ] Upgrade disposable MediaGallery 1.7.0 copy.
- [ ] Upgrade disposable MediaGallery 1.7.3 copy.
- [ ] Run pre-migration to `images/mediagallery/` and verify the source remains untouched.
- [ ] Confirm migration is idempotent.
- [ ] Confirm conflicting destination files fail without overwrite.
- [ ] Confirm a legacy upgrade without the required preflight is refused safely.
- [ ] Confirm administrator settings are preserved.

### Multisite

- [ ] Shared plugin code with separate DB/table prefix or databases.
- [ ] Separate `path_images`, `images_url` and `path_data`.
- [ ] Confirm Site A cannot write into or serve Site B storage.
- [ ] Confirm temporary/upload directories are isolated.

### Upload/security regression

- [ ] Browser upload success and invalid/missing CSRF rejection.
- [ ] Four-slot browser upload option association.
- [ ] DNC off/on tests for PNG/GIF/BMP and `discard_original` variants.
- [ ] Executable/double-extension/unknown-MIME rejection.
- [ ] Remote Media public/private/redirect/oversize cases.
- [ ] FTP valid source, forged outside path, unsafe extension and escaping symlink.
- [ ] ZIP import normal and hostile archives.
- [ ] CLI recursive import normal nested directories and symlink rejection.
- [ ] Batch continuation/cancellation ownership matrix.
- [ ] Moderated upload/edit/approve/reject with forged bindings.
- [ ] Stale-temp cleanup age-boundary tests.

### Functional/interoperability regression

- [ ] Moderator email HTML/plaintext through Geeklog mail backend.
- [ ] `album_list` permission matrix.
- [ ] Media/album canonical output with multiple skins and pagination.
- [ ] RSS/podcast generation under PHP 8.3 without warnings.
- [ ] Legacy audio/video fallback paths without warnings.
- [ ] Existing `fslideshow.php` URLs/autotags.
- [ ] MediaGallery → IndexNow save/delete notifications for media and albums.
- [ ] Public-to-private album transition does not expose a public URL through `PLG_getItemInfo(..., uid=1)`.
- [ ] Media move updates the media plus source/destination album URLs.

## 14. Final RC cleanup

- [x] Add explicit image-backend capability detection and clear error reporting.
- [x] Complete the major public template/accessibility/SEO modernization.
- [x] Add generic album/media lifecycle interoperability.
- [ ] Finish live PHP 8.2/8.3 runtime audit.
- [ ] Finish documentation cleanup and current install/upgrade instructions.
- [ ] Decide final `functions_legacy.inc` structure.
- [ ] Run the full live-test matrix.
- [ ] Build and validate the RC ZIP.

## Release principle

MediaGallery 1.8.0 should be safer to upgrade than 1.7.x, preserve user media outside replaceable plugin code, work naturally in single-site and shared-code multisite installations, provide modern accessible public output, use Geeklog-native APIs wherever practical, expose content changes to the wider Geeklog ecosystem, and fail explicitly when required runtime capabilities are unavailable.
