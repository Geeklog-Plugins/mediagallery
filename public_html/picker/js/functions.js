/* MediaGallery simple reusable picker. */
(function (window, document) {
    'use strict';

    function selectedMedia(form) {
        var fields = form.thumbnail;
        var i;
        if (!fields) {
            return '';
        }
        if (typeof fields.length !== 'number') {
            return fields.checked ? fields.value : '';
        }
        for (i = 0; i < fields.length; i += 1) {
            if (fields[i].checked) {
                return fields[i].value;
            }
        }
        return '';
    }

    function albumId(form) {
        var value = parseInt(form.aid.value, 10);
        return isFinite(value) && value > 0 ? value : 0;
    }

    function insertAutotag(tag) {
        if (typeof window.InsertHtml === 'function') {
            window.InsertHtml(tag);
            window.close();
        }
        return false;
    }

    window.insertImage = function (form) {
        var id = selectedMedia(form);
        if (!id) {
            window.alert(lang.no_media);
            return false;
        }
        return insertAutotag('[media:' + id + ' width:640 src:disp align:none link:1]');
    };

    window.insertAlbum = function (form) {
        var id = albumId(form);
        if (!id) {
            window.alert(lang.no_album);
            return false;
        }
        return insertAutotag('[album:' + id + ' width:640 align:none link:1]');
    };

    document.addEventListener('change', function (event) {
        var input = event.target;
        var cards;
        var card;
        var i;
        if (!input || input.name !== 'thumbnail') {
            return;
        }
        cards = document.querySelectorAll('.mg-picker-card');
        for (i = 0; i < cards.length; i += 1) {
            cards[i].classList.remove('is-selected');
        }
        card = input.closest ? input.closest('.mg-picker-card') : input.parentNode;
        if (card) {
            card.classList.add('is-selected');
        }
    });
}(window, document));
