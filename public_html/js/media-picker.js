(function () {
    'use strict';

    function insertAtCursor(target, value) {
        var field = document.querySelector(target);
        var start;
        var end;

        if (!field || typeof field.value !== 'string') {
            return;
        }

        start = typeof field.selectionStart === 'number' ? field.selectionStart : field.value.length;
        end = typeof field.selectionEnd === 'number' ? field.selectionEnd : start;
        field.value = field.value.substring(0, start) + value + field.value.substring(end);
        field.focus();

        if (typeof field.setSelectionRange === 'function') {
            field.setSelectionRange(start + value.length, start + value.length);
        }

        if (typeof Event === 'function') {
            field.dispatchEvent(new Event('input', {bubbles: true}));
            field.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }

    document.addEventListener('click', function (event) {
        var launcher = event.target.closest ? event.target.closest('[data-mg-picker-url]') : null;
        var choice = event.target.closest ? event.target.closest('[data-mg-autotag]') : null;
        var picker;

        if (launcher) {
            event.preventDefault();
            picker = window.open(
                launcher.getAttribute('data-mg-picker-url'),
                'mediagallery-picker',
                'width=920,height=720,resizable=yes,scrollbars=yes'
            );
            if (picker) {
                picker.focus();
            }
            return;
        }

        if (choice) {
            event.preventDefault();
            if (window.opener && !window.opener.closed) {
                window.opener.postMessage({
                    source: 'mediagallery',
                    action: 'insert',
                    target: choice.getAttribute('data-mg-target'),
                    value: choice.getAttribute('data-mg-autotag')
                }, window.location.origin);
                window.close();
            }
        }
    });

    window.addEventListener('message', function (event) {
        var data = event.data;

        if (event.origin !== window.location.origin || !data) {
            return;
        }
        if (data.source !== 'mediagallery' || data.action !== 'insert') {
            return;
        }
        if (typeof data.target !== 'string' || typeof data.value !== 'string') {
            return;
        }

        insertAtCursor(data.target, data.value);
    });
}());
