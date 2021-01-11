#! /usr/bin/env python3
import io
import sys

import matplotlib.pyplot as plt
import numpy as np

from viaduc import Viaduc


def plot() -> str:
    plt.figure(figsize=[5, 4])
    t = np.arange(-2, 2, .01)
    y1 = 2 * np.sin(2 * np.pi * t)
    y2 = 2 * np.cos(2 * np.pi * t)
    plt.plot(y1)
    plt.plot(y2)
    plt.axis('on')
    buf = io.BytesIO()
    plt.savefig(buf, format="svg")
    buf.seek(0)
    return buf.read().decode("utf-8")


class Api(Viaduc.Api):
    def __init__(self):
        super(Viaduc.Api, self).__init__()
        self.plot = plot()

    def get_plot(self):
        return self.plot


class Presentation(Viaduc.Presentation):
    width = 480
    height = 480
    title = 'plot'
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    {{bootstrap_meta}}

    {{bootstrap_mui_css}}

    <title>{{title}}</title>
</head>
<body>

<div id="content">
    <div id="plot">
        <!-- plot here -->
    </div>
    <div class="p-3">
        📈 matplotlib plot included as svg
    </div>
</div>

{{bootstrap_mui_js}}

<script>
    window.addEventListener('pywebviewready', function() {
        getPlot();
    })
    
    function getPlot() {
        pywebview.api.get_plot()
            .then(function(plot) {
                $('#plot').append(plot);
            })
            .catch(function(e) {
                doAlert('alert-error', 'error', e);
            });
    }

</script>

</body>
</html>    
    '''


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv)
