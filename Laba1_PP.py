import os
from flask import Flask,redirect

app = Flask(__name__)
@app.route('/choto-tam')
def hello():
    return "<h1>Hello World</h1>"


    # Bind to PORT if defined, otherwise default to 5000.
    #port = int(os.environ.get('PORT', 80))
    #app.run(host='0.0.0.0', port=port)
'''

from flask import Flask

from flask_restful import Api

from hello import HelloWorld

app = Flask(name)
api = Api(app)

api.add_resource(HelloWorld, "/api/v1/hello-world/<int:id>")

if name == "main":
    app.run(debug=True)'''