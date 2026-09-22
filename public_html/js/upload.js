(function () {
    'use strict';

    var form = document.getElementById('mg-upload-form');
    var input = document.getElementById('mg-upload-files');
    var dropzone = document.getElementById('mg-upload-dropzone');
    var queue = document.getElementById('mg-upload-queue');
    var list = document.getElementById('mg-upload-list');
    var count = document.getElementById('mg-upload-count');
    var template = document.getElementById('mg-upload-item-template');

    if (!form || !input || !dropzone || !queue || !list || !count || !template) {
        return;
    }

    var files = [];
    var metadata = {};

    function fileKey(file) {
        return [file.name, file.size, file.lastModified || 0].join('::');
    }

    function formatSize(bytes) {
        if (!bytes) {
            return '0 B';
        }
        var units = ['B', 'KB', 'MB', 'GB'];
        var index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
        var value = bytes / Math.pow(1024, index);
        return (index === 0 ? value.toFixed(0) : value.toFixed(value >= 10 ? 1 : 2)) + ' ' + units[index];
    }

    function captureMetadata() {
        var items = list.querySelectorAll('[data-upload-item]');
        Array.prototype.forEach.call(items, function (item, index) {
            if (!files[index]) {
                return;
            }
            var key = fileKey(files[index]);
            var data = metadata[key] || {};
            var caption = item.querySelector('[data-field="caption"]');
            var description = item.querySelector('[data-field="description"]');
            var keywords = item.querySelector('[data-field="keywords"]');
            var category = item.querySelector('[data-field="category"]');
            var dnc = item.querySelector('[data-field="dnc"]');
            var thumbnail = item.querySelector('[data-field="thumbnail"]');

            data.caption = caption ? caption.value : '';
            data.description = description ? description.value : '';
            data.keywords = keywords ? keywords.value : '';
            data.category = category ? category.value : '0';
            data.dnc = dnc ? dnc.checked : false;
            data.thumbnail = thumbnail && thumbnail.files && thumbnail.files[0] ? thumbnail.files[0] : (data.thumbnail || null);
            metadata[key] = data;
        });
    }

    function assignFileList(target, fileArray) {
        if (typeof DataTransfer === 'undefined') {
            return false;
        }

        var transfer = new DataTransfer();
        fileArray.forEach(function (file) {
            transfer.items.add(file);
        });
        target.files = transfer.files;
        return true;
    }

    function restoreThumbnail(inputElement, file) {
        if (!inputElement || !file || typeof DataTransfer === 'undefined') {
            return;
        }
        var transfer = new DataTransfer();
        transfer.items.add(file);
        inputElement.files = transfer.files;
    }

    function render() {
        list.innerHTML = '';

        files.forEach(function (file, index) {
            var fragment = template.content.cloneNode(true);
            var item = fragment.querySelector('[data-upload-item]');
            var key = fileKey(file);
            var data = metadata[key] || {};

            Array.prototype.forEach.call(fragment.querySelectorAll('[name]'), function (field) {
                field.name = field.name.replace('__INDEX__', String(index));
            });

            fragment.querySelector('[data-file-name]').textContent = file.name;
            fragment.querySelector('[data-file-size]').textContent = formatSize(file.size);

            var caption = fragment.querySelector('[data-field="caption"]');
            var description = fragment.querySelector('[data-field="description"]');
            var keywords = fragment.querySelector('[data-field="keywords"]');
            var category = fragment.querySelector('[data-field="category"]');
            var dnc = fragment.querySelector('[data-field="dnc"]');
            var thumbnail = fragment.querySelector('[data-field="thumbnail"]');

            if (caption) { caption.value = data.caption || ''; }
            if (description) { description.value = data.description || ''; }
            if (keywords) { keywords.value = data.keywords || ''; }
            if (category && data.category !== undefined) { category.value = data.category; }
            if (dnc) { dnc.checked = !!data.dnc; }
            restoreThumbnail(thumbnail, data.thumbnail);

            var remove = fragment.querySelector('[data-remove-file]');
            if (remove) {
                if (typeof DataTransfer === 'undefined') {
                    remove.disabled = true;
                } else {
                    remove.addEventListener('click', function () {
                        captureMetadata();
                        files.splice(index, 1);
                        assignFileList(input, files);
                        render();
                    });
                }
            }

            list.appendChild(fragment);
        });

        queue.hidden = files.length === 0;
        count.textContent = files.length ? String(files.length) + ' ' + form.getAttribute('data-selected-label') : '';
    }

    function setFiles(nextFiles) {
        captureMetadata();
        files = nextFiles.slice();
        render();
    }

    function mergeDroppedFiles(dropped) {
        captureMetadata();

        var seen = {};
        var merged = [];

        files.concat(dropped).forEach(function (file) {
            var key = fileKey(file);
            if (!seen[key]) {
                seen[key] = true;
                merged.push(file);
            }
        });

        if (assignFileList(input, merged)) {
            setFiles(merged);
        }
    }

    input.addEventListener('change', function () {
        setFiles(Array.prototype.slice.call(input.files || []));
    });

    ['dragenter', 'dragover'].forEach(function (eventName) {
        dropzone.addEventListener(eventName, function (event) {
            event.preventDefault();
            event.stopPropagation();
            dropzone.classList.add('is-dragover');
        });
    });

    ['dragleave', 'drop'].forEach(function (eventName) {
        dropzone.addEventListener(eventName, function (event) {
            event.preventDefault();
            event.stopPropagation();
            dropzone.classList.remove('is-dragover');
        });
    });

    dropzone.addEventListener('drop', function (event) {
        if (!event.dataTransfer || !event.dataTransfer.files || typeof DataTransfer === 'undefined') {
            return;
        }
        mergeDroppedFiles(Array.prototype.slice.call(event.dataTransfer.files));
    });

    dropzone.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            input.click();
        }
    });

    form.addEventListener('submit', function () {
        captureMetadata();
    });
}());
