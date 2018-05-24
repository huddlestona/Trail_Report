from flask import flask

app = Flask(__name__)

#home page

@app.rounte('/')
def index():
  return '''
    <!DOCTYPE html>
    <html>
            <head>
                <meta charset="utf-8">
                <title>Trip Report</title>
            </head>
        <body>
            <!--page content -->
            <h1> Determine the conditions of a new trail in Washington</h1>
            <p>
                Trail:
                Date:
                </p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
