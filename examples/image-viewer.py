#! /usr/bin/env python3
import base64
import mimetypes
import os
import sys

import webview
from viaduc import Viaduc


class Api(Viaduc.Api):
    def get_dir_name(self):
        file_name = self.window.create_file_dialog(webview.FOLDER_DIALOG, allow_multiple=False)
        if file_name and file_name[0]:
            return file_name[0]

    def open_dir_dialog(self, dir_name):
        print('dir_name', dir_name)
        if not dir_name:
            dir_name = self.get_dir_name()
            if not dir_name:
                # cancel was pressed
                return {
                    'action': 'DONE'
                }
        image_files = []
        for f in os.listdir(dir_name):
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.gif'):
                image_files.append(f)
        if not image_files:
            raise ValueError('No image files in dir')

        return {
            'action': 'CALLBACK',
            'function': 'loadDir',
            'params': {
                'dir': dir_name,
                'imageFiles': image_files
            }
        }

    def load_image(self, image):
        mime, encoding = mimetypes.guess_type(image)
        with open(image, 'rb') as i:
            data = base64.b64encode(i.read()).decode("ascii")
            src = f'data:{mime};base64,{data}'
            return {
                'action': 'CALLBACK',
                'function': 'showImage',
                'params': {
                    'image': image,
                    'src': src
                }
            }


class Presentation(Viaduc.Presentation):
    width = 1200
    height = 600
    title = 'image viewer'
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    {{bootstrap_meta}}

    {{bootstrap_mui_css}}

    <style>
        #content {
            overflow: auto;
            margin-top: 64px;
            height: calc(100% - 64px);
        }
        
        .navbar-brand {
            color: #9d9d9d !important; 
        }
        
        .navbar-brand:hover, .navbar-brand:focus {
            color: #fff  !important;
        }

        #_list {
            max-width: 400px;
        }
        
        #_img {
            max-width: 800px;
            object-fit: contain;
        }
    </style>

    <title>{{title}}</title>
</head>
<body>

<nav class="navbar navbar-dark bg-dark fixed-top">
  <a class="navbar-brand">{{title}}</a>
  <form class="form-inline" action="undefined" onsubmit="openDir(getVal('_dir'));">
    <input id="_dir" class="form-control mr-sm-2" placeholder="Directory" aria-label="Directory">
    <button type="button" class="btn btn-outline-success my-2 my-sm-0" onclick="openDir(null);">Open</button>
  </form>
</nav>

<div id="content" class="container-fluid">
    <div class="row">
        <div id="imageFiles" class="col-sm">
            <ul id="_list" class="list-group">
            </ul>
        </div>
        <div class="col-sm">
            <img id="_img" src="">
        </div>
    </div>
</div>

{{bootstrap_mui_js}}

<script>
    function openDir(_dir) {
        processResponse(pywebview.api.open_dir_dialog(_dir));
    }

    function createListItem(dir, imageFile) {
        return `<a href="#" class="list-group-item list-group-item-action" onclick="processResponse(pywebview.api.load_image('${dir}/${imageFile}'));">${imageFile}</a>`;
    }
    
    function loadDir(params) {
        $('#_dir').val(params.dir);
        $('#_list').empty();
        $('#_img').attr('src', '');
        params.imageFiles.forEach(function(item, index) {
            $('#_list').append(createListItem(params.dir, item));
        });
    }
    
    function showImage(params) {
        $('#_img').attr('src', params.src);
    }
</script>

</body>
</html>    
    '''


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv)
