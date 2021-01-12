#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2021  Diego Torres Milano
Created on Jan 2, 2021

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Diego Torres Milano
"""

__version__ = '1.0.1'

import argparse as argparse
import re
import sys
import time
from abc import ABC
from html.parser import HTMLParser

import webview
from forbiddenfruit import curse

BOOTSTRAP_TEMPLATE_URL = 'https://getbootstrap.com/docs/4.0/getting-started/introduction/'

BOOTSTRAP_META = '''
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
'''

BOOTSTRAP_CSS = '''
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
          integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" rel="stylesheet">
'''

BOOTSTRAP_MUI_CSS = '''
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons" rel="stylesheet">
    <link crossorigin="anonymous"
          href="https://unpkg.com/bootstrap-material-design@4.1.1/dist/css/bootstrap-material-design.min.css"
          integrity="sha384-wXznGJNEXNG1NFsbm0ugrLFMQPWswR3lds2VeinahP8N0zJw9VWSopbjv2x7WCvX" rel="stylesheet">
'''

BOOTSTRAP_JS = '''
<script crossorigin="anonymous"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script crossorigin="anonymous"
        integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx"
        src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"></script>
'''

BOOTSTRAP_MUI_JS = '''
<script crossorigin="anonymous"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<script crossorigin="anonymous"
        integrity="sha384-fA23ZRQ3G/J53mElWqVJEGJzU0sTs+SvzG8fXVWP+kJQ1lwFAOkcUOysnlKJC33U"
        src="https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js"></script>
<script crossorigin="anonymous"
        integrity="sha384-CauSuKpEqAFajSpkdjv3z9t8E7RlpJ1UP0lKM/+NdtSarroVKu069AlsRPKkFBz9"
        src="https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js"></script>
<script>$(document).ready(function() { $('body').bootstrapMaterialDesign(); });</script>
'''

FRAMELESS_CLOSE_BUTTON = '''
<div class="float-right" style="margin-top: 0px; margin-right: 8px;">
    <button aria-label="Close"
            class="close" onclick="pywebview.api.close()" type="button">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
'''

FRAMELESS_CLOSE_BUTTON_LIGHT = '''
<div class="float-right" style="margin-top: 0px; margin-right: 8px;">
    <button aria-label="Close"
            class="close text-light" onclick="pywebview.api.close()" type="button">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
'''

# template from https://getbootstrap.com/docs/4.0/getting-started/introduction/
HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    {{bootstrap_meta}}

    {{bootstrap_css}}

    <title>Viaduc</title>
  </head>
  <body>

    <div class="alert alert-warning" role="alert">
      ⚠️ Viaduc: Nothing to show. Implement a class extending <strong>Viaduc.Presentation</strong> and add content.
    </div>

    {{bootstrap_js}}

  </body>
</html>
"""

VIADUC_SCRIPT = """
<script>
    function processResponse(promise) {
        promise
            .then(function(response) {
                console.log('processResponse:', response);
                switch (response.action) {
                    case 'SUCCESS':
                    case 'DONE':
                        if (response.message) {
                            doAlert('alert-success', 'Success', `${response.status} ${response.message}`);
                        }
                        break;
                        
                    case 'WARNING':
                    case 'CANCELED':
                        if (response.message) {
                            doAlert('alert-warning', 'Warning', `${response.status} ${response.message}`);
                        }
                        break;
                    
                    case 'CALLBACK':
                        var f = window[response.function];
                        var p = response.params;
                        if (typeof f === 'function') {
                            f.call(null, p);
                        } else {
                            doAlert('alert-danger', 'Error', `Not a function: ${response.function}`);
                        }
                        break;
                        
                    default:
                        doAlert('alert-danger', 'Error', `Invalid response status: ${response.status}`);
                }
             })
            .catch(function(e) {
                doAlert('alert-danger', 'Error', e);
             });
    }
    
    function doAlert(alertClass, name, text) {
        if (alertClass == 'alert-danger') {
            console.error(name, text);
        }
        if (name.toLowerCase() === 'error') {
            name = `⛔️ ${name}`;
        }
        if (!name.match(new RegExp(':.*$'))) {
            name = `${name}:&nbsp;`;
        }
        $('body').append(
            `<div id="alert" class="alert alert-dismissible fade show ${alertClass}" role="alert" style="display: flex; flex-grow: 1; width: 90vw; position: fixed; bottom: 24px; left: 5%; z-index: 10; margin: auto;"> <strong>${name} </strong> ${text} <button type="button" class="close" data-dismiss="alert" aria-label="Close" onclick=""> <span aria-hidden="true">&times;</span> </button> </div>`
            );
    }
    
    function getVal(id) {
        if (!id.startsWith('#')) {
            id = `#${id}`;
        }
        var e = $(id);
        var t = e.prop('type');
        if (t == 'checkbox') {
            return e.is(':checked');
        }
        if (t == 'radio') {
            var n = e.attr('name');
            return $(`input[name="${n}"]:checked`).val();
        }
        return e.val();
    }
    
    function getVals(idSelector = '_') {
        var a = [];
        document.querySelectorAll(`[id^=${idSelector}]`)
            .forEach(
                function(e) {
                    a.push({id:e.id, val:getVal(e.id)});
                }
            ); 
        return a;
    }
    
    function print(str) {
        pywebview.api.print(str);
    }
</script>
"""


def get_attr(key, attrs):
    for attr in attrs:
        if attr[0] == key:
            return attr[1]
    return None


def has_attr(key, attrs):
    for attr in attrs:
        if attr[0] == key:
            return True
    return False


class Toolkit:
    def __init__(self):
        self.map = dict()
        self.map['frameless_close_button'] = FRAMELESS_CLOSE_BUTTON
        self.map['frameless_close_button_light'] = FRAMELESS_CLOSE_BUTTON_LIGHT


class Bootstrap(Toolkit):
    def __init__(self):
        super(Bootstrap, self).__init__()
        self.map['bootstrap_meta'] = BOOTSTRAP_META
        self.map['bootstrap_css'] = BOOTSTRAP_CSS
        self.map['bootstrap_js'] = BOOTSTRAP_JS


class BootstrapMui(Bootstrap):
    def __init__(self):
        super(BootstrapMui, self).__init__()
        self.map['bootstrap_mui_css'] = BOOTSTRAP_MUI_CSS
        self.map['bootstrap_mui_js'] = BOOTSTRAP_MUI_JS


class ViaducParser(HTMLParser, ABC):
    bootstrap_css = False
    bootstrap_js = False
    popper_js = False
    jquery = False
    fonts_css = False
    parsed = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            if has_attr('src', attrs):
                src = get_attr('src', attrs)
                if 'bootstrap.bundle.min.js' in src or 'bootstrap-material-design.js' in src:
                    self.bootstrap_js = True
                elif 'popper.js' in src:
                    self.popper_js = True
                elif re.search(r'jquery-.+\.slim\.min\.js', src):
                    self.jquery = True
        elif tag == 'link':
            if get_attr('rel', attrs) == 'stylesheet':
                href = get_attr('href', attrs)
                if 'bootstrap.min.css' in href or 'bootstrap-material-design.min.css' in href:
                    self.bootstrap_css = True
                if 'family=Roboto:300,400,500,700|Material+Icons' in href:
                    self.fonts_css = True
        self.parsed += f'<{tag}'
        for attr in attrs:
            self.parsed += f' {attr[0]}="{attr[1]}"'
        self.parsed += '>'

    def handle_data(self, data):
        if data:
            self.parsed += data

    def handle_entityref(self, name):
        if name:
            self.parsed += name

    def handle_endtag(self, tag):
        if tag == 'body':
            self.parsed += VIADUC_SCRIPT
        self.parsed += f'</{tag}>'


def re_escape(self) -> str:
    """
    Re-escapes the '{{' and '}}' so normal '{' and '}' can be used in HTML strings representing HTML pages.
    Otherwise, if the HTML string contains something like

    ```
            body {
                background: magenta;
            }
    ```

    and error like

    ```
            KeyError: '\n                background'
    ```

    will be raised by `format()` as the way of escaping `{` in f-strings is `{{`.
    So, instead of forcing to write HTML strings using `{{` and `}}` we are converting them on-the fly.

    :param self: the string
    :return: the reescaped string
    """
    return self.replace('{{', '☾').replace('}}', '☽').replace('{', '{{').replace('}', '}}') \
        .replace('☾', '{') \
        .replace('☽', '}')


# extension method
curse(str, 're_escape', re_escape)


class Viaduc:
    """
    Viaduc: simplest python gui.
    """
    class Api:
        window: webview.window = None

        def load(self) -> any:
            """
            Load callback.
            :return:
            """
            return None

        def close(self, exit_val=0):
            """
            Close the app.

            :param exit_val: exit value
            """
            self.window.destroy()
            sys.exit(exit_val)

        def map_vals(self, vals: []) -> dict:
            """
            Maps the values as returned by `getVals()` to a dictionary with ids as keys.

            :param vals: the array of ids and values
            :return: a dictionary with ids as keys
            """
            m = {}
            for v in vals:
                m[v['id']] = v['val']
            return m

        def print(self, _str):
            print(_str)

    class Presentation:
        width = 800
        height = 600
        title: str = ""
        # The idea is that html is a single string (that can be copied from the content of a single html file that can
        # be open with the browser, debugged, tested, etc.)
        html: str = HTML
        # NOTE: Usually we want html to be a string so everything is contained in one file, however in this case we are
        # reading it from a file as an example of how it can be done.
        file: str = None

        def __init__(self, toolkit: Toolkit = BootstrapMui()):
            """
            Presentation constructor.

            :param toolkit: the toolkit used by this presentation (i.e. BootstrapMui)
            """
            # read file if necessary
            if self.file:
                with open(self.file) as f:
                    self.html = f.read()

            self.html = self.html.re_escape().format(title=self.title, **toolkit.map)

    def __init__(self, api: Api = Api(), presentation: Presentation = Presentation(), args=None):
        if args is None:
            args = sys.argv
        self.frameless = False
        self.debug = False
        self.api = api
        self.presentation = presentation
        self.parser = ViaducParser()

        # parse args
        arg_parser = argparse.ArgumentParser(description='Viaduc: simplest python GUI.')
        arg_parser.add_argument('-x', '--debug', action='store_true', default=False)
        arg_parser.add_argument('--frameless', action='store_true', default=False)
        parsed_args = arg_parser.parse_args(args[1:])
        self.debug = parsed_args.debug
        self.frameless = parsed_args.frameless

        # parse html
        self.parser.feed(presentation.html)
        if not self.parser.bootstrap_css:
            raise RuntimeError(f'No bootstrap css found in html. See {BOOTSTRAP_TEMPLATE_URL}')
        if not self.parser.bootstrap_js:
            raise RuntimeError(f'No bootstrap js found in html. See {BOOTSTRAP_TEMPLATE_URL}')
        if not self.parser.jquery:
            raise RuntimeError(f'No jquery found in html. See {BOOTSTRAP_TEMPLATE_URL}')

        self.window = webview.create_window(presentation.title,
                                            width=presentation.width,
                                            height=presentation.height,
                                            html=self.parser.parsed,
                                            easy_drag=True,
                                            js_api=api,
                                            frameless=self.frameless,
                                            on_top=True,
                                            transparent=False
                                            )

        if api:
            api.window = self.window

        #
        # On macOS Big Sur we need to start with the window on_top and then remove the attribute after a while.
        #
        webview.start(self.init, (('on_top', False), ('load',)), debug=self.debug)

    def init(self, *args, **kwargs):
        for _init in args:
            f = _init[0]
            if f == 'on_top':
                time.sleep(1)
                self.on_top(_init[1])
            elif f == 'load':
                self.api.load()

    def on_top(self, value):
        self.window.on_top = value


if __name__ == '__main__':
    Viaduc()
