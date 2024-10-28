#! /usr/bin/env python3

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    title = "process response"
    height = 360
    html = """
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
            <button type="button" class="btn btn-success" style="min-width: 100%"
                onclick="processResponse(Promise.resolve({action:'SUCCESS', message:'Hello'}));">Success</button>
        </div>
        <div class="col">
            <button type="button" class="btn btn-danger" style="min-width: 100%"
                onclick="processResponse(Promise.resolve({action:'ERROR', message:'Danger'}));">Error</button>
        </div>
        <div class="col">
            <button type="button" class="btn btn-warning" style="min-width: 100%"
                onclick="processResponse(Promise.resolve({action:'WARNING', message:'Warning'}));">Warning</button>
        </div>
        </div>
    </div>
    {{bootstrap_js}}

  </body>  
 </html>
"""


if __name__ == "__main__":
    Viaduc(presentation=Presentation(), args=["", "--debug"])
