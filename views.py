from flask import Flask, render_template, request, make_response
from danmu_parser import get_user_by_danmu
import mimetypes

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
        response = make_response(s)
        mime_type = mimetypes.guess_type('danmu.xml')[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
            'danmu.xml'.encode().decode('latin-1'))
        return response



        return s

    return 'aa'


if __name__ == '__main__':
    app.run(debug=True)
