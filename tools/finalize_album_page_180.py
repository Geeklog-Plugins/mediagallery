from pathlib import Path

css_path = Path('public_html/style.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* MediaGallery 1.8 album page modernization */'
if marker not in css:
    css += r'''

/* MediaGallery 1.8 album page modernization */
.mg-album-page-header {
  padding: .7rem .9rem;
  gap: .65rem 1rem;
  border-radius: .35rem;
}

.mg-album-heading {
  flex: 1 1 13rem;
  min-width: 0;
}

.mg-album-page-header .mg_album_title {
  margin: 0;
  font-size: clamp(1.35rem, 1.4vw + .85rem, 1.85rem);
  font-weight: 700;
}

.mg-album-controls {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: .55rem;
  flex: 2 1 30rem;
  min-width: 0;
}

.mg-album-controls .mg_search {
  flex: 1 1 20rem;
  max-width: 32rem;
}

.mg-album-controls .mg_adminbox {
  flex: 0 1 20rem;
}

.mg-album-controls form > div {
  display: flex;
  align-items: center;
  gap: .45rem;
  margin: 0;
}

.mg-album-controls input[type="search"] {
  flex: 1 1 10rem;
  min-width: 0;
}

.mg-album-controls select {
  min-width: 11rem;
  max-width: 100%;
}

.mg-album-toolbar {
  justify-content: space-between;
  margin: .55rem 0 1rem;
  background: transparent;
  padding: 0;
}

.mg-album-actions {
  display: flex;
  align-items: center;
  gap: .4rem;
  flex-wrap: wrap;
}

.mg-album-toolbar .mg_pagination {
  margin-left: auto;
}

.mg_album_grid.mg-album-default-grid,
.mg_album_grid.mg-album-default-grid.mg-cols-1,
.mg_album_grid.mg-album-default-grid.mg-cols-2,
.mg_album_grid.mg-album-default-grid.mg-cols-3,
.mg_album_grid.mg-album-default-grid.mg-cols-4,
.mg_album_grid.mg-album-default-grid.mg-cols-5,
.mg_album_grid.mg-album-default-grid.mg-cols-6,
.mg_album_grid.mg-album-default-grid.mg-cols-7,
.mg_album_grid.mg-album-default-grid.mg-cols-8,
.mg_album_grid.mg-album-default-grid.mg-cols-9,
.mg_album_grid.mg-album-default-grid.mg-cols-10 {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 22rem));
  justify-content: center;
  align-items: stretch;
  gap: 1.1rem;
  margin: 1.1rem 0 1.35rem;
}

.mg-album-default-grid .mg_album_cell {
  display: flex;
  min-width: 0;
}

.mg-album-default-grid .mg-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
  overflow: hidden;
  border: 1px solid rgba(127, 127, 127, .2);
  border-radius: .7rem;
  background: rgba(255, 255, 255, .72);
  box-shadow: 0 .1rem .35rem rgba(0, 0, 0, .06);
  text-align: center;
}

.mg-album-default-grid .mg-card-media {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 11.5rem;
  padding: .85rem .85rem .45rem;
  background: rgba(127, 127, 127, .035);
}

.mg-album-default-grid .mg_thumbnail {
  width: 100%;
  margin: 0;
  align-items: center;
}

.mg-album-default-grid .mg_thumbnail_wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.mg-album-default-grid .mg_thumbnail img {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 15rem;
}

.mg-album-default-grid .mg-card-body {
  display: flex;
  flex: 1 1 auto;
  flex-direction: column;
  align-items: center;
  padding: .65rem .85rem .85rem;
}

.mg-album-default-grid .mg-card-title {
  margin: 0 0 .45rem;
  font-size: 1.05rem;
  line-height: 1.35;
  font-weight: 700;
  overflow-wrap: anywhere;
}

.mg-card-subtitle {
  font-weight: 400;
}

.mg-card-artist,
.mg-card-description,
.mg_search_album {
  margin-bottom: .45rem;
  line-height: 1.45;
}

.mg-card-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .25rem .6rem;
  flex-wrap: wrap;
  margin-top: auto;
  font-size: .88rem;
  line-height: 1.4;
}

.mg-card-meta > span + span::before {
  content: "\00b7";
  margin-right: .6rem;
  opacity: .55;
}

.mg-card-meta-album {
  margin-top: .35rem;
}

.mg-card-rating {
  margin-top: .5rem;
  font-size: .9rem;
}

.mg-card-rating .ratingblock {
  margin: 0 auto;
}

.mg-card-rating .mg_rating,
.mg-card-rating .static {
  font-size: .85rem;
}

.mg-card-tags {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .35rem;
  flex-wrap: wrap;
  margin-top: .5rem;
  font-size: .86rem;
}

.mg-card-tag-list a {
  display: inline-flex;
  align-items: center;
  margin: .12rem .15rem;
  padding: .12rem .42rem;
  border: 1px solid currentColor;
  border-radius: 999px;
  text-decoration: none;
  line-height: 1.25;
}

.mg-card-tag-list a:hover,
.mg-card-tag-list a:focus-visible {
  text-decoration: underline;
}

.mg-card-edit {
  margin-top: .55rem;
  font-size: .86rem;
}

.mg-album-footer {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: .65rem 1rem;
  align-items: start;
  margin-top: .5rem;
}

.mg-album-pagination-bar {
  min-width: 0;
  border-radius: .35rem;
}

.mg-album-page-info {
  display: flex;
  align-items: center;
  gap: .15rem;
  flex-wrap: wrap;
}

.mg-album-pagination-bar .mg_pagination {
  margin-left: auto;
}

.mg-album-secondary-controls {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: .45rem;
  min-width: min(100%, 22rem);
}

.mg-album-secondary-controls .mg_jumpbox,
.mg-album-secondary-controls .mg_sortbox {
  padding: 0;
  text-align: right;
}

.mg-album-secondary-controls form > div {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: .45rem;
  margin: 0;
}

.mg-album-secondary-controls select {
  min-width: 10rem;
  max-width: 16rem;
}

@media (max-width: 52rem) {
  .mg-album-page-header,
  .mg-album-controls {
    align-items: stretch;
  }

  .mg-album-controls {
    flex-basis: 100%;
    justify-content: stretch;
  }

  .mg-album-controls .mg_search,
  .mg-album-controls .mg_adminbox {
    max-width: none;
  }

  .mg-album-footer {
    grid-template-columns: 1fr;
  }

  .mg-album-secondary-controls {
    width: 100%;
    min-width: 0;
  }
}

@media (max-width: 38rem) {
  .mg-album-controls {
    flex-direction: column;
  }

  .mg-album-controls form > div,
  .mg-album-secondary-controls form > div {
    flex-wrap: wrap;
  }

  .mg-album-controls input[type="search"],
  .mg-album-controls select,
  .mg-album-secondary-controls select {
    flex: 1 1 10rem;
    max-width: none;
  }

  .mg_album_grid.mg-album-default-grid,
  .mg_album_grid.mg-album-default-grid[class*="mg-cols-"] {
    grid-template-columns: minmax(0, 1fr);
  }

  .mg-album-toolbar,
  .mg-album-pagination-bar {
    align-items: stretch;
  }

  .mg-album-actions,
  .mg-album-toolbar .mg_pagination,
  .mg-album-pagination-bar .mg_pagination {
    width: 100%;
    margin-left: 0;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
needle = '- [x] Modernize the default media-detail page with semantic article/figure markup, separated navigation/actions, compact metadata and normalized keyword tags.\n'
addition = '- [x] Modernize the default album page with centered auto-fit cards, compact metadata, unified controls and a responsive footer.\n'
if addition not in roadmap:
    if needle in roadmap:
        roadmap = roadmap.replace(needle, needle + addition)
    else:
        roadmap += '\n' + addition
    roadmap_path.write_text(roadmap, encoding='utf-8')

print('Finalized default album page modernization')
