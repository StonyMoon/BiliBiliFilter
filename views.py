from flask import Flask, render_template, request
from danmu_parser import get_user_by_danmu

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST', 'GET'])
def get_xml():
    if (request.method == 'POST'):
        av = request.form.get('url')
        key = request.form.get('key')
        s = get_user_by_danmu(av, key)
        return s
    return 'aa'


if __name__ == '__main__':
    app.run(debug=True)
