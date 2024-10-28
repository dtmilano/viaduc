#! /usr/bin/env python3

from viaduc import Viaduc


class Api(Viaduc.Api):
    def get_vals(self, vals):
        v = self.map_vals(vals)
        return Viaduc.done(f"vals: {v}")


class Presentation(Viaduc.Presentation):
    title = "selects"
    height = 536
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
        <div class="row mb-3">
            <div class="col-12">
                <select id="_select" name="select" class="form-control custom-select">
                    <option selected>Open this select menu</option>
                    <option value="1">One</option>
                    <option value="2">Two</option>
                    <option value="3">Three</option>
                </select>
            </div>
        </div>
        
        <div class="row mb-3">
            <div class="col-12">
                <label for="_cars">Select multiple options</label>
                <select name="cars" id="_cars" class="form-control custom-select" multiple>
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="opel">Opel</option>
                    <option value="audi">Audi</option>
                </select>
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
"""


if __name__ == "__main__":
    Viaduc(api=Api(), presentation=Presentation(), args=["", "--debug"])
