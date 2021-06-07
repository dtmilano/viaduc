#! /usr/bin/env python3

from viaduc import Viaduc


class Api(Viaduc.Api):
    def get_vals(self, vals):
        v = self.map_vals(vals)
        return Viaduc.done(f'vals: {v}')


class Presentation(Viaduc.Presentation):
    title = 'radios'
    height = 440
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
    
    <div class="container-fluid">
        <div class="row">
        <div class="col">
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
                <label class="btn btn-secondary active">
                    <input type="radio" name="color" id="_red" value="red" autocomplete="off" checked> red
                </label>
                <label class="btn btn-secondary">
                    <input type="radio" name="color" id="_blue" value="blue" autocomplete="off"> blue
                </label>
                <label class="btn btn-secondary">
                    <input type="radio" name="color" id="_green" value="green" autocomplete="off"> green
                </label>
            </div>
        </div>
        <div class="col">
            <div class="input-group">
                <div class="input-group-prepend">
                    <div class="input-group-text">
                        <input type="radio" id="_radio" name="radio" value="on" aria-label="Radio button for following text input">
                    </div>
                </div>
                <input type="text" id="_text" name="text" class="form-control" aria-label="Text input with radio button">
            </div>
        </div>
        <div class="col">
            <div class="custom-control custom-radio">
                <input type="radio" id="_male" name="gender" value="male" class="custom-control-input">
                <label class="custom-control-label" for="_male">Male</label>
            </div>
            <div class="custom-control custom-radio">
                <input type="radio" id="_female" name="gender" value="female" class="custom-control-input">
                <label class="custom-control-label" for="_female">Female</label>
            </div>
            <div class="custom-control custom-radio">
                <input type="radio" id="_other" name="gender" value="other" class="custom-control-input">
                <label class="custom-control-label" for="_other">Other</label>
            </div>
        </div>
        
        </div>
        
        <button type="button" class="btn btn-primary" onclick="doGetVals()">Get vals</button>
    </div>
    
    <script>
        function doGetVals() {
            processResponse(pywebview.api.get_vals(getVals()));
        }
    </script>
    {{bootstrap_js}}

  </body>  
 </html>
'''


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=['', '--debug'])
