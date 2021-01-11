#! /usr/bin/env python3
import os
import sys

import webview

from viaduc import Viaduc


class Api(Viaduc.Api):
    def open_file_dialog(self):
        file_types = ('Text Files (*.txt;*.sh;*.c)', 'All files (*.*)')

        file_name = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if file_name and file_name[0]:
            with open(file_name[0]) as f:
                return {
                    'action': 'CALLBACK',
                    'function': 'loadFile',
                    'params': {
                        'fileName': file_name,
                        'content': f.read()
                    }
                }
        else:
            return {
                'action': 'DONE'
            }

    def save_file_dialog(self, vals):
        v = self.map_vals(vals)

        file_name = self.window.create_file_dialog(webview.SAVE_DIALOG, directory=os.path.dirname(v['_fileName']),
                                                   save_filename=os.path.basename(v['_fileName']))
        if file_name:
            with open(file_name, "w+") as f:
                f.write(v['_editor'])

        return {
            'action': 'DONE'
        }


class Presentation(Viaduc.Presentation):
    width = 800
    height = 600
    title = 'editor'
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    {{bootstrap_meta}}

    {{bootstrap_mui_css}}

    <style>
        #content {
            overflow: hidden;
            margin-top: 64px;
            height: calc(100% - 64px);
        }

        textarea[name=editor] {
            resize: none;
            width: 100%;
            height: 100%;
            overflow: auto;
            background: #fff;
        }

        .sans-serif {
            font-family: sans-serif;
        }

        .serif {
            font-family: serif;
        }

        .monospace {
            font-family: monospace;
        }
    </style>

    <title>{{title}}</title>
</head>
<body>

<ul class="nav fixed-top nav-tabs bg-dark">
    <li class="nav-item dropdown">
        <a aria-expanded="false" aria-haspopup="true" class="nav-link" data-toggle="dropdown" id="fileMenu"
           role="button">File</a>
        <div aria-labelledby="fileMenu" class="dropdown-menu">
            <a class="dropdown-item" onclick="openFile();">Open...</a>
            <a class="dropdown-item" onclick="saveFile();">Save...</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" onclick="pywebview.api.close();">Quit</a>
        </div>
    </li>
    <li class="nav-item dropdown">
        <a aria-expanded="false" aria-haspopup="true" class="nav-link" data-toggle="dropdown" id="viewMenu"
           role="button">View</a>
        <div aria-labelledby="viewMenu" class="dropdown-menu">
            <div class="dropdown-item radio">
                <label>
                    <input checked name="font" onchange="changeFont(this);" type="radio" value="sans-serif">
                    Sans-serif
                </label>
            </div>
            <div class="dropdown-item radio">
                <label>
                    <input name="font" onchange="changeFont(this);" type="radio" value="serif">
                    Serif
                </label>
            </div>
            <div class="dropdown-item radio">
                <label>
                    <input name="font" onchange="changeFont(this);" type="radio" value="monospace">
                    Monospace
                </label>
            </div>
        </div>
    </li>
    <li class="nav-item">
        <a class="nav-link" onclick="help();">Help</a>
    </li>
</ul>

<div id="content">
    <form action="return false;">
        <input id="_fileName" name="fileName" type="hidden"/>
        <textarea class="sans-serif" id="_editor" name="editor"></textarea>
    </form>
</div>

{{bootstrap_mui_js}}

<script>
    function openFile() {
        processResponse(pywebview.api.open_file_dialog());
    }

    function loadFile(params) {
        $('#_fileName').val(params.fileName);
        $('#_editor').val(params.content);
    }

    function saveFile() {
        processResponse(pywebview.api.save_file_dialog(getVals()));
    }

    function changeFont(font) {
        $('#_editor').removeClass("sans-serif serif monospace").addClass(font.value);
    }

    function help() {
        doAlert('alert-warning', '🤖', 'Not implemented yet');
    }
</script>

</body>
</html>    
    '''


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv)
