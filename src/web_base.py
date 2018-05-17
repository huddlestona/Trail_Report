from flask import Flask
from make_prediction import *

app = Flask(__name__)

#home page

@app.route('/')
# def index():
#   return '''
#     <!DOCTYPE html>
#     <html>
#             <head>
#                 <meta charset="utf-8">
#                 <title>Trip Report</title>
#             </head>
#         <body>
#             <!--page content -->
#             <h1> Determine the conditions of a new trail in Washington</h1>
#             <p>
#                 Trail:
#                 Date:
#                 </p>
#         </body>
#     </html>
#     '''
def begin():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    .dropbtn {
        background-color: #3498DB;
        color: white;
        padding: 16px;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }

    .dropbtn:hover, .dropbtn:focus {
        background-color: #2980B9;
    }

    .dropdown {
        position: relative;
        display: inline-block;
    }

    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f1f1f1;
        min-width: 160px;
        overflow: auto;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
    }

    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }

    .dropdown a:hover {background-color: #ddd}

    .show {display:block;}
    </style>
    </head>
    <body>

    <h2>Trail Report</h2>
    <p>Choose the trail you want to hike below</p>

    <p>
    <script>
    var txt = "Go explore the WTA site!";
    document.write("<p>Don't know what hike to check out?  "+txt.link("https://www.WTA.org") + "</p>");
    </script>
    </p>

    <div class="dropdown">
    <button onclick="myFunction()" class="dropbtn">Choose Hike</button>
      <div id="myDropdown" class="dropdown-content">
        <a href="#home">Hike1</a>
        <a href="#about">Hike2</a>
        <a href="#contact">Hike3</a>
      </div>
    </div>

    <script>
    /* When the user clicks on the button,
    toggle between hiding and showing the dropdown content */
    function myFunction() {
        document.getElementById("myDropdown").classList.toggle("show");
    }

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
      if (!event.target.matches('.dropbtn')) {

        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }
    </script>

    </body>
    </html>
'''






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
