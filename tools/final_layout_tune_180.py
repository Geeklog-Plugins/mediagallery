from pathlib import Path

p = Path('public_html/style.css')
s = p.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 final media toolbar + immersive scaling */'
if marker not in s:
    s += r'''

/* MediaGallery 1.8 final media toolbar + immersive scaling */
@media (min-width: 42.01rem) {
  .mg-media-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }
  .mg-media-pagination {
    flex: 0 0 auto;
  }
  .mg-media-actions {
    flex: 1 1 auto;
    margin-left: auto;
    justify-content: flex-end;
    text-align: right;
  }
}

.mg-slideshow-stage {
  overflow: hidden;
}
.mg-slideshow-image {
  width: calc(100vw - 2rem);
  height: calc(100vh - 2rem);
  max-width: none;
  max-height: none;
  object-fit: contain;
  object-position: center center;
}

@media (max-width: 42rem) {
  .mg-slideshow-image {
    width: calc(100vw - 1rem);
    height: calc(100vh - 1rem);
  }
}
'''
p.write_text(s, encoding='utf-8')
