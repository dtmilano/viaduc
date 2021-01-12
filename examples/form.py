#! /usr/bin/env python3
import sys

from viaduc import Viaduc


class Api(Viaduc.Api):
    def do_something(self, vals) -> dict[str, str]:
        v = self.map_vals(vals)
        if not v['_email']:
            raise ValueError('Empty email')
        if not v['_password']:
            raise ValueError('Empty password')
        response = {
            'action': 'DONE',
            'message': 'Operation completed'
        }
        return response


class Presentation(Viaduc.Presentation):
    width = 800
    height = 560
    title = 'form example'
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    {{bootstrap_meta}}

    {{bootstrap_css}}

    <style>
            body {
                background: linear-gradient(to right, #aa076b, #61045f);
            }

            .container-fluid {
                margin-top: 24px;
            }

    </style>

    <title>{{title}}</title>
</head>
<body>

{{frameless_close_button_light}}

<!--<div class="float-right" style="margin-top: -24px; margin-right: 8px;">-->
<!--    <button aria-label="Close"-->
<!--            class="close text-light" onclick="pywebview.api.close()" type="button">-->
<!--        <span aria-hidden="true">&times;</span>-->
<!--    </button>-->
<!--</div>-->

<div class="d-flex flex-column container-fluid mb-0">
    <h1 class="text-light display-1">{{title}}</h1>
    <p class="text-light text-justify">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
        magna aliqua. Feugiat nibh sed pulvinar proin gravida hendrerit. Et egestas quis ipsum suspendisse ultrices
        gravida. Dignissim enim sit amet venenatis urna cursus eget nunc. Vel eros donec ac odio tempor orci dapibus.
    </p>


    <form>
        <div class="form-group">
            <label class="text-light" for="_email">Email address</label>
            <input aria-describedby="_emailHelp" class="form-control" id="_email" type="email">
            <small class="form-text text-white-50" id="_emailHelp">We'll never share your email with anyone else.</small>
        </div>
        <div class="form-group">
            <label class="text-light" for="_password">Password</label>
            <input class="form-control" id="_password" type="password">
        </div>
        <div class="form-group form-check">
            <input class="form-check-input" id="_check" type="checkbox">
            <label class="form-check-label text-light" for="_check">Check me out</label>
        </div>
        <button class="btn btn-primary" onclick="doSomething()" type="button">Submit</button>
    </form>


</div>

{{bootstrap_js}}

<script>
        function doSomething() {
            processResponse(pywebview.api.do_something(getVals()));
        }

</script>
</body>
</html>
    '''


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv + ['--frameless'])
