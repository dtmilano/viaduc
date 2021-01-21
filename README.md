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
The simplest Viaduc program instantiates a `Viaduc` object, like this 

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
Let's add a `title` and some `html` which includes some metatags (`{{name}}`) that are replaced by viaduc.

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


![simplest](./screenshots/helloworld.png)
