from flask import Flask, request, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print('main')
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '8080')))
else :
    print('fucking sub')
