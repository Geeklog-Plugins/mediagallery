from pathlib import Path

slideshow = Path('templates/slideshow.thtml')
slideshow.write_text(r'''<!-- MediaGallery 1.8 immersive slideshow -->
{lbslideshow}
<!-- BEGIN noItems -->
<div class="mg-slideshow-empty">
  <p>{no_images}</p>
  <p><a href="{return_to_album_url}">{return_to_album}</a></p>
</div>
<!-- END noItems -->
<!-- BEGIN slideItems -->
<div class="mg-slideshow-shell" id="mgSlideshow" role="region" aria-label="{album_title}">
  <div class="mg-slideshow-stage">
    <img id="slide" class="mg-slideshow-image" src="" alt="" draggable="false"{xhtml}>
  </div>

  <div class="mg-slideshow-top mg-slideshow-chrome">
    <div class="mg-slideshow-album">{album_title}</div>
    <a class="mg-slideshow-close" href="{return_to_album_url}" aria-label="{lang_close}" title="{lang_close}">&times;</a>
  </div>

  <button class="mg-slideshow-nav mg-slideshow-prev mg-slideshow-chrome" type="button" id="mgSlidePrev" aria-label="{lang_previous}" title="{lang_previous}">&#8249;</button>
  <button class="mg-slideshow-nav mg-slideshow-next mg-slideshow-chrome" type="button" id="mgSlideNext" aria-label="{lang_next}" title="{lang_next}">&#8250;</button>

  <div class="mg-slideshow-bottom mg-slideshow-chrome">
    <div class="mg-slideshow-caption" id="caption" aria-live="polite"></div>
    <div class="mg-slideshow-controls">
      <button class="mg-slideshow-play" type="button" id="mgSlidePlay" aria-pressed="true">
        <span id="mgSlidePlayText">{stop}</span>
      </button>
      <span class="mg-slideshow-counter" id="mgSlideCounter" aria-live="polite"></span>
    </div>
  </div>
</div>

<script type="text/javascript">
//<![CDATA[
var photo_urls = [];
var photo_captions = [];
{photo_info}

(function () {
    'use strict';

    var root = document.getElementById('mgSlideshow');
    var image = document.getElementById('slide');
    var caption = document.getElementById('caption');
    var counter = document.getElementById('mgSlideCounter');
    var playButton = document.getElementById('mgSlidePlay');
    var playText = document.getElementById('mgSlidePlayText');
    var prevButton = document.getElementById('mgSlidePrev');
    var nextButton = document.getElementById('mgSlideNext');
    var photoCount = {photo_count};
    var current = 1;
    var playing = true;
    var timer = null;
    var idleTimer = null;
    var touchStartX = null;
    var delay = 4500;
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!root || !image || photoCount < 1) {
        return;
    }

    if (reduceMotion) {
        playing = false;
        root.className += ' mg-reduce-motion';
    }

    function normalize(index) {
        if (index < 1) {
            return photoCount;
        }
        if (index > photoCount) {
            return 1;
        }
        return index;
    }

    function updatePlayButton() {
        playText.textContent = playing ? '{stop}' : '{play}';
        playButton.setAttribute('aria-pressed', playing ? 'true' : 'false');
    }

    function preload(index) {
        var preloadImage;
        index = normalize(index);
        if (!photo_urls[index]) {
            return;
        }
        preloadImage = new Image();
        preloadImage.src = photo_urls[index];
    }

    function schedule() {
        window.clearTimeout(timer);
        if (playing && photoCount > 1) {
            timer = window.setTimeout(function () {
                show(current + 1, true);
            }, delay);
        }
    }

    function show(index, fromAuto) {
        var nextSrc;
        current = normalize(index);
        nextSrc = photo_urls[current];
        if (!nextSrc) {
            return;
        }

        root.classList.add('is-changing');
        image.onload = function () {
            root.classList.remove('is-changing');
        };
        image.src = nextSrc;
        image.alt = photo_captions[current] || '{album_title}';
        caption.textContent = photo_captions[current] || '';
        counter.textContent = current + ' / ' + photoCount;
        preload(current + 1);
        preload(current - 1);

        if (!fromAuto) {
            schedule();
        } else {
            schedule();
        }
    }

    function previous() {
        show(current - 1, false);
    }

    function next() {
        show(current + 1, false);
    }

    function togglePlay() {
        playing = !playing;
        updatePlayButton();
        schedule();
        showChrome();
    }

    function showChrome() {
        root.classList.remove('is-idle');
        window.clearTimeout(idleTimer);
        idleTimer = window.setTimeout(function () {
            root.classList.add('is-idle');
        }, 2600);
    }

    prevButton.onclick = previous;
    nextButton.onclick = next;
    playButton.onclick = togglePlay;

    if (photoCount <= 1) {
        prevButton.style.display = 'none';
        nextButton.style.display = 'none';
        playButton.style.display = 'none';
    }

    document.addEventListener('keydown', function (event) {
        var key = event.key || event.keyCode;
        if (key === 'ArrowLeft' || key === 37) {
            event.preventDefault();
            previous();
        } else if (key === 'ArrowRight' || key === 39) {
            event.preventDefault();
            next();
        } else if (key === ' ' || key === 'Spacebar' || key === 32) {
            event.preventDefault();
            togglePlay();
        } else if (key === 'Escape' || key === 27) {
            window.location.href = '{return_to_album_url_js}';
        }
        showChrome();
    });

    root.addEventListener('mousemove', showChrome);
    root.addEventListener('touchstart', function (event) {
        showChrome();
        if (event.touches && event.touches.length === 1) {
            touchStartX = event.touches[0].clientX;
        }
    }, {passive: true});

    root.addEventListener('touchend', function (event) {
        var delta;
        if (touchStartX === null || !event.changedTouches || !event.changedTouches.length) {
            return;
        }
        delta = event.changedTouches[0].clientX - touchStartX;
        touchStartX = null;
        if (Math.abs(delta) < 45) {
            return;
        }
        if (delta > 0) {
            previous();
        } else {
            next();
        }
    }, {passive: true});

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            window.clearTimeout(timer);
        } else {
            schedule();
        }
    });

    updatePlayButton();
    show(1, false);
    showChrome();
}());
//]]>
</script>
<!-- END slideItems -->
<!-- BEGIN photo_url -->
{URL}
{CAPTION}
<!-- END photo_url -->
''', encoding='utf-8')

php = Path('public_html/slideshow.php')
text = php.read_text(encoding='utf-8')

old_caption = '''        $PhotoCaption = $mediaObject[$i]['media_title'];
        $PhotoCaption = str_replace(";",  " ", $PhotoCaption);
        $PhotoCaption = str_replace("\\\"", " ", $PhotoCaption);
        $PhotoCaption = str_replace("\\n", " ", $PhotoCaption);
        $PhotoCaption = str_replace("\\r", " ", $PhotoCaption);

        $T->set_var(array(
            'URL'     => 'photo_urls[' . $y . '] = "' . $PhotoURL . '";',
            'CAPTION' => 'photo_captions[' . $y . '] = "' . $PhotoCaption . '";',
        ));'''
new_caption = '''        $PhotoCaption = trim(strip_tags($mediaObject[$i]['media_title']));

        $T->set_var(array(
            'URL'     => 'photo_urls[' . $y . '] = ' . json_encode($PhotoURL) . ';',
            'CAPTION' => 'photo_captions[' . $y . '] = ' . json_encode($PhotoCaption) . ';',
        ));'''
if old_caption not in text:
    raise SystemExit('caption producer block not found')
text = text.replace(old_caption, new_caption, 1)
text = text.replace("    $T->set_var('photo_count', $total_media);", "    $T->set_var('photo_count', $photoCount);", 1)

needle = "$full_toggle = '';\n"
insert = '''$returnToAlbumUrl = $_MG_CONF['site_url'] . '/album.php?aid=' . $album_id . '&amp;page=1&amp;sort=' . $sortOrder;
$returnToAlbumUrlJs = $_MG_CONF['site_url'] . '/album.php?aid=' . $album_id . '&page=1&sort=' . $sortOrder;
$langPrevious = isset($LANG_MG03['previous']) ? $LANG_MG03['previous'] : (isset($LANG_MG03['prev']) ? $LANG_MG03['prev'] : 'Previous');
$langNext = isset($LANG_MG03['next']) ? $LANG_MG03['next'] : 'Next';
$langClose = isset($LANG_MG03['return_to_album']) ? $LANG_MG03['return_to_album'] : 'Return to album';

$full_toggle = '';
'''
if needle not in text:
    raise SystemExit('full_toggle anchor not found')
text = text.replace(needle, insert, 1)

text = text.replace("    'pagination'        => '<a href=\"' . $_MG_CONF['site_url'] . '/album.php?aid=' . $album_id . '&amp;page=1&amp;sort=' . $sortOrder . '\">' . $LANG_MG03['return_to_album'] .'</a>',", "    'pagination'        => '<a href=\"' . $returnToAlbumUrl . '\">' . $LANG_MG03['return_to_album'] . '</a>',", 1)

setvar_anchor = "    'album_title'       => $album_title,\n"
setvar_insert = "    'album_title'       => $album_title,\n    'return_to_album_url' => $returnToAlbumUrl,\n    'return_to_album_url_js' => json_encode($returnToAlbumUrlJs),\n    'lang_previous'     => $langPrevious,\n    'lang_next'         => $langNext,\n    'lang_close'        => $langClose,\n"
if setvar_anchor not in text:
    raise SystemExit('set_var anchor not found')
text = text.replace(setvar_anchor, setvar_insert, 1)

old_output = "$display = MG_createHTMLDocument($display, $title);\n\nCOM_output($display);"
new_output = "$robots = '<meta name=\"robots\" content=\"noindex,follow\"' . XHTML . '>';\n$display = MG_createHTMLDocument($display, $title, $robots);\n\nCOM_output($display);"
if old_output not in text:
    raise SystemExit('output anchor not found')
text = text.replace(old_output, new_output, 1)
php.write_text(text, encoding='utf-8')

css = Path('public_html/style.css')
css_text = css.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 immersive slideshow */'
if marker not in css_text:
    css_text += r'''

/* MediaGallery 1.8 immersive slideshow */
.mg-slideshow-shell {
  position: fixed;
  inset: 0;
  z-index: 100000;
  display: grid;
  place-items: center;
  overflow: hidden;
  background:
    radial-gradient(circle at 50% 45%, rgba(255,255,255,.055), transparent 45%),
    #08090b;
  color: #fff;
  touch-action: pan-y;
}

.mg-slideshow-stage {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: clamp(1rem, 3vw, 2.5rem);
}

.mg-slideshow-image {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
  opacity: 1;
  transform: scale(1);
  transition: opacity .32s ease, transform .45s ease;
  user-select: none;
  -webkit-user-select: none;
}

.mg-slideshow-shell.is-changing .mg-slideshow-image {
  opacity: .18;
  transform: scale(.992);
}

.mg-slideshow-top,
.mg-slideshow-bottom {
  position: absolute;
  left: 0;
  right: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: clamp(.75rem, 2vw, 1.35rem) clamp(1rem, 3vw, 2rem);
  transition: opacity .25s ease, transform .25s ease;
}

.mg-slideshow-top {
  top: 0;
  justify-content: space-between;
  background: linear-gradient(to bottom, rgba(0,0,0,.72), transparent);
}

.mg-slideshow-bottom {
  bottom: 0;
  flex-direction: column;
  justify-content: flex-end;
  background: linear-gradient(to top, rgba(0,0,0,.78), transparent);
  text-align: center;
}

.mg-slideshow-album {
  max-width: min(70vw, 55rem);
  overflow: hidden;
  color: rgba(255,255,255,.78);
  font-size: .9rem;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mg-slideshow-close,
.mg-slideshow-nav,
.mg-slideshow-play {
  border: 0;
  color: #fff;
  background: rgba(15,16,19,.46);
  box-shadow: 0 .2rem 1rem rgba(0,0,0,.18);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  cursor: pointer;
  text-decoration: none;
}

.mg-slideshow-close {
  display: inline-grid;
  place-items: center;
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 999px;
  font-size: 1.8rem;
  line-height: 1;
}

.mg-slideshow-nav {
  position: absolute;
  top: 50%;
  z-index: 4;
  display: grid;
  place-items: center;
  width: clamp(2.8rem, 5vw, 4rem);
  height: clamp(4.5rem, 10vh, 7rem);
  padding: 0;
  border-radius: .8rem;
  font-size: clamp(2.2rem, 5vw, 4rem);
  line-height: 1;
  transform: translateY(-50%);
  transition: opacity .25s ease, background .2s ease, transform .25s ease;
}

.mg-slideshow-prev { left: clamp(.5rem, 2vw, 1.5rem); }
.mg-slideshow-next { right: clamp(.5rem, 2vw, 1.5rem); }

.mg-slideshow-close:hover,
.mg-slideshow-close:focus-visible,
.mg-slideshow-nav:hover,
.mg-slideshow-nav:focus-visible,
.mg-slideshow-play:hover,
.mg-slideshow-play:focus-visible {
  background: rgba(255,255,255,.16);
  outline: 2px solid rgba(255,255,255,.8);
  outline-offset: 2px;
}

.mg-slideshow-caption {
  max-width: min(90vw, 70rem);
  color: rgba(255,255,255,.92);
  font-size: clamp(.95rem, 1.2vw + .7rem, 1.25rem);
  line-height: 1.4;
  text-wrap: balance;
}

.mg-slideshow-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .75rem;
}

.mg-slideshow-play {
  min-height: 2.25rem;
  padding: .35rem .8rem;
  border-radius: 999px;
  font: inherit;
}

.mg-slideshow-counter {
  min-width: 3.5rem;
  color: rgba(255,255,255,.72);
  font-variant-numeric: tabular-nums;
}

.mg-slideshow-shell.is-idle .mg-slideshow-chrome {
  opacity: 0;
  pointer-events: none;
}

.mg-slideshow-shell.is-idle .mg-slideshow-top { transform: translateY(-.6rem); }
.mg-slideshow-shell.is-idle .mg-slideshow-bottom { transform: translateY(.6rem); }
.mg-slideshow-shell.is-idle .mg-slideshow-nav { transform: translateY(-50%) scale(.94); }

.mg-slideshow-empty {
  max-width: 42rem;
  margin: 3rem auto;
  text-align: center;
}

/* Subtle gallery lift: visual only; semantic content remains unchanged. */
.mg-album-default-grid .mg-card {
  transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}

.mg-album-default-grid .mg-card-media img {
  transition: transform .28s ease;
}

.mg-album-default-grid .mg-card:hover,
.mg-album-default-grid .mg-card:focus-within {
  transform: translateY(-3px);
  border-color: rgba(127,127,127,.32);
  box-shadow: 0 .65rem 1.5rem rgba(0,0,0,.10);
}

.mg-album-default-grid .mg-card:hover .mg-card-media img,
.mg-album-default-grid .mg-card:focus-within .mg-card-media img {
  transform: scale(1.025);
}

@media (max-width: 40rem) {
  .mg-slideshow-stage { padding: .65rem; }
  .mg-slideshow-top { padding: .7rem .8rem; }
  .mg-slideshow-bottom { padding: .8rem 1rem 1rem; }
  .mg-slideshow-album { max-width: 70vw; }
  .mg-slideshow-nav {
    top: auto;
    bottom: 5.4rem;
    width: 2.85rem;
    height: 3.4rem;
    border-radius: 999px;
    font-size: 2.25rem;
    transform: none;
  }
  .mg-slideshow-prev { left: .75rem; }
  .mg-slideshow-next { right: .75rem; }
  .mg-slideshow-shell.is-idle .mg-slideshow-nav { transform: scale(.94); }
}

@media (prefers-reduced-motion: reduce) {
  .mg-slideshow-image,
  .mg-slideshow-chrome,
  .mg-slideshow-nav,
  .mg-album-default-grid .mg-card,
  .mg-album-default-grid .mg-card-media img {
    transition: none !important;
  }
  .mg-album-default-grid .mg-card:hover,
  .mg-album-default-grid .mg-card:focus-within,
  .mg-album-default-grid .mg-card:hover .mg-card-media img,
  .mg-album-default-grid .mg-card:focus-within .mg-card-media img {
    transform: none;
  }
}
'''
css.write_text(css_text, encoding='utf-8')

roadmap = Path('ROADMAP.md')
road = roadmap.read_text(encoding='utf-8')
entry = '- [x] Replace the legacy slideshow chrome with an immersive native lightbox-style viewer (keyboard, swipe, autoplay, reduced-motion support) while keeping album/media pages as the SEO/AI surfaces.\n'
if entry not in road:
    anchor = '## 8.'
    idx = road.find(anchor)
    if idx >= 0:
        line_end = road.find('\n', idx)
        road = road[:line_end+1] + entry + road[line_end+1:]
    else:
        road += '\n' + entry
roadmap.write_text(road, encoding='utf-8')
