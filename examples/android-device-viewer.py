#! /usr/bin/env python3

import base64
import io
import json
import sys

import culebratester_client
import culebratester_client.configuration
import culebratester_client.rest

from viaduc import Viaduc


class Culebratester:
    """
    Culebratester API.
    See https://github.com/dtmilano/CulebraTester2-client
    """

    def __init__(self):
        configuration = culebratester_client.configuration.Configuration()
        self.api_instance = culebratester_client.DefaultApi(culebratester_client.ApiClient(configuration))

    def culebra_info(self):
        try:
            return self.api_instance.culebra_info_get()
        except Exception as e:
            raise RuntimeError("Exception when calling DefaultApi->culebra_info_get: %s\n" % e)

    def get_display_real_size(self):
        try:
            return self.api_instance.device_display_real_size_get()
        except Exception as e:
            raise RuntimeError("Exception when calling DefaultApi->device_display_real_size_get: %s\n" % e)

    def screenshot(self, scale=1.0, quality=100):
        try:
            api_response = self.api_instance.ui_device_screenshot_get(scale=scale, quality=quality)
            stream = io.BytesIO(api_response.data)
            return stream.read()
        except Exception as e:
            raise RuntimeError("Exception when calling DefaultApi->ui_device_screenshot_get: %s\n" % e)

    def encode_screenshot(self, scale=1.0, quality=100):
        return f'data:image/png;base64,{base64.b64encode(self.screenshot(scale, quality)).decode("ascii")}'

    def press_back(self):
        try:
            return json.dumps(self.api_instance.ui_device_press_back_get().__dict__)
        except Exception as e:
            raise RuntimeError("Exception when calling DefaultApi->ui_device_press_back_get: %s\n" % e)

    def click(self, x, y):
        try:
            return json.dumps(self.api_instance.ui_device_click_get(x, y).__dict__)
        except Exception as e:
            raise RuntimeError("Exception when calling DefaultApi->ui_device_click_get: %s\n" % e)


culebratester = Culebratester()


class Api(Viaduc.Api):
    def __init__(self):
        super(Viaduc.Api, self).__init__()
        self.obtain_screenshot()

    def obtain_screenshot(self):
        display_real_size = culebratester.get_display_real_size()
        return {'screenshot': culebratester.encode_screenshot(), 'w': display_real_size.x / 4,
                'h': display_real_size.y / 4}

    def press_back(self):
        return culebratester.press_back()

    def click(self, x, y):
        return culebratester.click(x, y)


HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    {{bootstrap_meta}}
    {{bootstrap_mui_css}}
    <style>
        body {
            background: black;
            user-drag: none;
            user-select: none;
        }
        
        #screenshot {
            object-fit: contain;
        }
    </style>
    <title>{{title}}</title>
</head>
<body>

<div id="content">
    <div id="screenshot-container">
        <img id="screenshot" src="">
    </div>
</div>

<div class="dropdown-menu dropdown-menu-sm" id="context-menu">
    <a class="dropdown-item" onclick="pressBack();">Back</a>
    <div class="dropdown-divider"></div>
    <a class="dropdown-item" onclick="pywebview.api.close();">Quit</a>
</div>

{{bootstrap_mui_js}}

<script>
    window.addEventListener('pywebviewready', () => {

        $('#content')
            .on('contextmenu', showContextMenu)
            .on('click', hideContextMenu)
            .on('click', deviceClick);

        $('#context-menu a')
            .on('click', hideContextMenu);

        obtainScreenshot();
    });

    function showContextMenu(e) {
        var top = Math.max(0, e.pageY - 10);
        var left = Math.max(0, e.pageX - 90);
        $('#context-menu').css({
          display: 'block',
          top: top,
          left: left
        }).addClass('show');
        return false;
    }

    function hideContextMenu(e) {
        $('#context-menu').removeClass('show').hide();
    }

    function obtainScreenshot() {
        setTimeout(() => {
        pywebview.api.obtain_screenshot()
            .then(response => {
                var s = $('#screenshot');
                s.css({'max-width': response.w, 'max-height': response.h });
                s.attr('src', response.screenshot);
            })
            .catch(e => {
                doAlert('alert-error', 'error', e);
            });
            }, 500);
    }

    function pressBack() {
        pywebview.api.press_back()
            .then(obtainScreenshot)
            .catch(e => {
                doAlert('alert-error', 'error', e);
            });
    }

    function deviceClick(e) {
        pywebview.api.click(e.pageX * 4, e.pageY * 4)
            .then(obtainScreenshot)
            .catch(e => {
                doAlert('alert-error', 'error', e);
            });
    }
</script>

</body>
</html>   
    '''


class Presentation(Viaduc.Presentation):
    html = HTML
    title = 'android device viewer'
    display_real_size = culebratester.get_display_real_size()
    width = display_real_size.x / 4
    height = display_real_size.y / 4


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv + ['--frameless'])
