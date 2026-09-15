# MediaGallery reusable media picker

MediaGallery 1.8.0 provides an optional picker for inserting MediaGallery
autotags into editors owned by other Geeklog plugins.

Consumers must not query MediaGallery tables or construct picker URLs. When
MediaGallery is active, call:

```php
$button = '';
if (in_array('mediagallery', $_PLUGINS) && function_exists('MG_getMediaPickerButton')) {
    $button = MG_getMediaPickerButton(array(
        'target' => 'textarea[name="comment"]',
        'tag'    => 'media',
    ));
}
```

The target accepts a simple id selector or a simple `name` selector. The picker
returns the selected autotag with a same-origin `postMessage`. Its JavaScript
inserts the value at the current cursor position and emits `input` and `change`
events.

Supported initial autotag types are `media`, `img` and `mlink`. Consumers
should normally request `media`. Album-level insertion can be added separately
without mixing album identifiers with the media-selection grid.

The `media_list` service complements the existing `album_list` service. Both
apply MediaGallery access rules and should be preferred over direct SQL access.
