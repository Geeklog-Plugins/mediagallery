from pathlib import Path

path = Path('include/classMedia.php')
text = path.read_text(encoding='utf-8')
old = """        $direct_url = self::getFileUrl('disp', $this->filename, $this->mime_ext);\n        $direct_path = self::getFilePath('disp', $this->filename, $this->mime_ext);\n        if (!file_exists($direct_path)) {\n            $direct_url = self::getFileUrl('disp', $this->filename, 'jpg');\n        }\n"""
new = """        $direct_url = '';\n        $direct_path = self::getFilePath('disp', $this->filename, $this->mime_ext);\n        if (file_exists($direct_path)) {\n            $direct_url = self::getFileUrl('disp', $this->filename, $this->mime_ext);\n        } else {\n            $direct_jpg_path = self::getFilePath('disp', $this->filename, 'jpg');\n            if (file_exists($direct_jpg_path)) {\n                $direct_url = self::getFileUrl('disp', $this->filename, 'jpg');\n            } elseif (!empty($this->media_thumbnail)) {\n                // Existing installations may not have a display derivative for every image.\n                // Fall back to the proven historical thumbnail instead of emitting a broken URL.\n                $direct_url = $this->media_thumbnail;\n            }\n        }\n"""
if old not in text:
    raise SystemExit('Expected direct preview block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
