#! /usr/bin/env python3

from viaduc import Viaduc


class Api(Viaduc.Api):
    def get_vals(self, vals):
        print(vals)
        v = self.map_vals(vals)
        print(v)
        return Viaduc.done(f'vals: {v}')


class Presentation(Viaduc.Presentation):
    title = 'inputs'
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
        <div class="col">
            <div class="row"><input type="button" value="button" id="_mybutton"></div>
            <div class="row">checkbox: <input type="checkbox" id="_mycheckbox"></div>
            <div class="row">color: <input type="color" id="_mycolor"></div>
            <div class="row">date: <input type="date" id="_mydate"></div>
            <div class="row"><input type="datetime-local"></div>
            <div class="row"><input type="email" name="myemail" id="_myemail"></div>
            <div class="row"><input type="file" name="myfile" id="_myfile"></div>
            <div class="row"><input type="hidden"></div>
            <div class="row"><input type="image"></div>
            <div class="row"><input type="month"></div>
            <div class="row"><input type="number"></div>
            <div class="row"><input type="password"></div>
            <div class="row"><input type="radio"></div>
            <div class="row"><input type="range"></div>
            <div class="row"><input type="reset"></div>
            <div class="row"><input type="search"></div>
            <div class="row"><input type="submit"></div>
            <div class="row"><input type="tel"></div>
            <div class="row"><input type="text"></div>
            <div class="row"><input type="time"></div>
            <div class="row"><input type="url"></div>
            <div class="row"><input type="week"></div>
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
