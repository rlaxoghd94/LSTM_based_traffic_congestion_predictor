from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print('main')
    app.run(debug=True, host='0.0.0.0', port=8001)
else :
    print('fucking sub')
