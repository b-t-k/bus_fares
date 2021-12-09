
from flask import Flask

app = Flask(__name__)
# app.register_blueprint(pages, url_prefix="/")

from app import pages

@app.context_processor
def inject_appname():
    return dict(appname="Bus Fare Calculator", variable2="NA")


# if __name__ == '__main__':
#     # app.run(debug=True, port=8888)
#     app.run(debug=True, port=8888, host='0.0.0.0')
