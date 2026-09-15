# MediaGallery service and lifecycle API

MediaGallery 1.8.0 exposes read-only discovery and content-change notifications through Geeklog's native plugin APIs.

Consumers should use these APIs instead of querying `mg_albums`, `mg_media` or `mg_media_albums` directly.

## `album_list` service

The `album_list` service returns albums already filtered through MediaGallery access rules.

### Member album tree

```php
$output = array();
$svc_msg = array();

$status = PLG_invokeService(
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

if ($status === PLG_RET_OK) {
    // $output contains the visible member album tree.
}
```

`uid` defaults to the current Geeklog user. A normal user can request only their own member album tree. A user with `mediagallery.admin` may request another user's tree.

`member_album_root = 0` is valid and supported.

### Numeric root

A caller can request the visible children of a specific album:

```php
$status = PLG_invokeService(
    'mediagallery',
    'album_list',
    array(
        'root'      => 123,
        'recursive' => true,
        'visible'   => true,
    ),
    $output,
    $svc_msg
);
```

The numeric root itself is used as the traversal root; the result contains its children and, when `recursive` is true, their descendants.

### Arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `uid` | current user | User whose member tree is requested when `root=member` |
| `root` | `member` | `member` or a numeric album ID |
| `recursive` | `true` | Include descendants |
| `visible` | `true` | Apply MediaGallery visibility filtering |

### Result

Each result row uses a stable associative structure:

```php
array(
    'id'       => 1064,
    'title'    => 'Thailand',
    'parent'   => 1060,
    'owner_id' => 42,
    'hidden'   => false,
    'access'   => 2,
    'depth'    => 2,
    'url'      => 'https://example.com/mediagallery/album.php?aid=1064',
);
```

Consumers should persist only the MediaGallery album ID when associating their own records with a gallery. Rendering should remain delegated to MediaGallery where practical so consuming plugins do not depend on MediaGallery's storage schema.

## `media_list` service

The `media_list` service returns one page of media from an accessible, visible
album. It is intended for selectors and integrations that must discover media
without querying MediaGallery tables directly.

```php
$output = array();
$svc_msg = array();

$status = PLG_invokeService(
    'mediagallery',
    'media_list',
    array(
        'album_id' => 52,
        'page'      => 1,
        'per_page' => 24,
    ),
    $output,
    $svc_msg
);
```

The result contains `items` and `pagination`. Each item exposes a stable media
ID, title, description, media and MIME types, thumbnail URL and public
MediaGallery URL. `per_page` is limited to 100. Requests for inaccessible or
hidden albums fail without returning their contents.

The reusable picker described in [`MEDIA-PICKER.md`](MEDIA-PICKER.md) consumes
this service and returns the selected autotag to the calling editor.

## Content lifecycle events

MediaGallery 1.8.0 reports content changes through Geeklog's standard lifecycle functions.

Media items retain their historical MediaGallery IDs:

```php
PLG_itemSaved($media_id, 'mediagallery');
PLG_itemDeleted($media_id, 'mediagallery');
```

Albums use a namespaced ID so Geeklog 2.1.1 can distinguish albums from media without requiring the `sub_type` argument introduced in newer Geeklog versions:

```text
album:52
```

Corresponding events are:

```php
PLG_itemSaved('album:52', 'mediagallery');
PLG_itemDeleted('album:52', 'mediagallery');
```

### Events emitted

MediaGallery announces the relevant public representation after these operations:

| Operation | Media event | Album event |
| --- | --- | --- |
| Add media | saved | parent album saved |
| Edit media | saved | every containing album saved |
| Delete media | deleted | affected album saved |
| Reorder/manage media | saved where applicable | affected album saved |
| Move media | saved | source + destination albums saved |
| Create album | — | album saved + parent listing saved |
| Edit album | — | album saved |
| Move album | — | album + old/new parent listings saved |
| Delete album | media deletions as applicable | album deleted + affected parent/target saved |
| Recursive album delete | media deletions as applicable | each deleted album announced |

Repeated notifications for the same album are deduplicated within a single request.

## Resolving album information with `PLG_getItemInfo()`

The existing MediaGallery item-info contract now accepts namespaced album IDs as well as historical media IDs.

Example:

```php
$url = PLG_getItemInfo(
    'mediagallery',
    'album:52',
    'url',
    1
);
```

For `uid = 1` (anonymous), an album URL is returned only when the album is not hidden and has anonymous read permission.

This is important for consumers such as IndexNow: if a formerly public album becomes private, the consumer can observe that it no longer has a public URL and handle its previously known URL appropriately.

Supported album properties include:

- `id`
- `url`
- `title`
- `description`
- `excerpt`
- `raw-description`
- `date-modified`

Media IDs continue through the pre-existing MediaGallery item-info behavior.

## URL resolution

`plugin_idToURL_mediagallery()` also understands namespaced album IDs. This allows a consumer to resolve a deterministic album URL even for a deletion event:

```text
album:52
    -> /mediagallery/album.php?aid=52
```

## Consumer model

The intended integration is:

```text
MediaGallery mutation
        |
        v
PLG_itemSaved / PLG_itemDeleted
        |
        +--> IndexNow
        +--> XML Sitemap
        +--> Hub
        +--> future connectors
```

MediaGallery does not call IndexNow, Hub or another consumer directly.

This keeps the producer/consumer contract generic and avoids coupling other plugins to MediaGallery's SQL schema or internal routes.

## Compatibility

The service and lifecycle extensions are additive in MediaGallery 1.8.0.

- Geeklog 2.1.1 is the minimum supported baseline.
- Album IDs use the `album:<id>` namespace specifically so lifecycle interoperability does not depend on newer Geeklog-only `sub_type` support.
- Existing media IDs, pages, autotags, albums and database tables remain compatible with the historical MediaGallery contract.
