# viaduc
![Upload Python Package](https://github.com/dtmilano/viaduc/workflows/Upload%20Python%20Package/badge.svg)
[![PyPI version](https://badge.fury.io/py/viaduc.svg)](https://badge.fury.io/py/viaduc)

Viaduc is probably the simplest way to create a nice-looking gui using python and tiny bit of html/css/js.

![form](./screenshots/form.png)

See the code for this example [here](./examples/form.py).

**viaduc** uses pywebview and [Bootstrap](https://getbootstrap.com/) to provide a gui for other tools and scripts.

# install
```
$ pip install viaduc
```

# simplest
The simplest Viaduc program instantiates a `Viaduc` object, like this ([simplest.py](./examples/simplest.py))

```
#! /usr/bin/env python3

from viaduc import Viaduc

if __name__ == '__main__':
    Viaduc()
```

and you will see this window

![simplest](./screenshots/simplest.png)

# helloworld
Then, let's do something more interesting implementing the `Presentation` class.
Let's add a `title` and some `html` which includes some metatags (`{{name}}`) that are replaced by viaduc ([helloworld.py](./examples/helloworld.py)).

```
#! /usr/bin/env python3

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    title = 'hello world'
    html = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    {{bootstrap_meta}}

    {{bootstrap_css}}

    <title>{{title}}</title>
  </head>
  <body>
    <div class="jumbotron">
        <h1>{{title}}</h1>
        <p class="lead">Welcome to <em>Viaduc</em>, the simplest way of creating a GUI in python.</p>
    </div>
    
    {{bootstrap_js}}

  </body>  
 </html>
'''


if __name__ == '__main__':
    Viaduc(presentation=Presentation())
```

and we will obtain this


![helloworld](./screenshots/helloworld.png)

# temperature converter
We have seen how `Presentation` can implement the GUI, but what about the interaction?
([temperature-converter.py](./examples/temperature-converter.py))

```
#! /usr/bin/env python3
import sys

from viaduc import Viaduc


def fahrenheit_to_celsius(fahrenheit):
    return round((5 / 9) * (float(fahrenheit) - 32), 2)


class Api(Viaduc.Api):
    def convert(self, vals):
        v = self.map_vals(vals)
        if not v['_fahrenheit']:
            raise ValueError('Enter a temperature')
        response = {
            'action': 'CALLBACK',
            'function': 'showCelsius',
            'params': {
                'celsius': fahrenheit_to_celsius(v['_fahrenheit'])
            }
        }
        return response


class Presentation(Viaduc.Presentation):
    width = 320
    height = 468
    title = 'temperature converter'
    html = '''
    <!-- copy file here -->
    '''
    file = "temperature-converter.html"


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv + ['--frameless'])
```

Here we are also implementing `Api` which provides the means of interoperation between domains.

Another thing to note here is that instead of having the HTML as a string we are reading it from a file, just to keep this example file smaller and being able to focus on the important parts.

When we execute it we obtain this window. It's `frameless` as we are passing this extra argument to `Viaduc`.


![temperature-converter](./screenshots/temperature-converter.png)

Clicking the **Convert** button or pressing **RETURN** converts the temperature from Fahrenheit to Celsius, invoking the `convert()` method. All the form values are automatically added by `Viaduc` as `vals` which contains `id`s and `values`.

Once we convert the temperature using `fahrenheit_to_celsius()` we use the `CALLBACK` action to invoke a javascript method defined in [temperature-converter.html](./examples/temperature-converter.html#L65) to show the result.

# editor
We can also interact with the local filesystem reading and writing files. This [editor](./examples/editor.py) shows these interactions.

Also shows how to use [Bootstrap Material Design](https://mdbootstrap.github.io/bootstrap-material-design/).

![editor](./screenshots/editor-example.gif)
