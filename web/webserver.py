import config
from flask import Flask
from flask import render_template

app = Flask(__name__)
heading = dict()


@app.route("/")
def main():
    print("config.LOCAL_DNS_PORT:", config.LOCAL_DNS_PORT)
    return str(config.LOCAL_DNS_PORT)


@app.route("/stocks")
def stocks():
    ip = config.LOCAL_DNS_HOST
    return render_template('index.html', ip=ip)


@app.route("/search")
def search():
    ip = config.LOCAL_DNS_HOST
    return render_template('search.html', ip=ip)


# @app.route('/_stuff', methods=['GET'])
# def stuff():
#     global heading
#     if request.method == 'GET':
#         if heading:
#             print heading['value']
#             return heading['value']
#         else:
#             blank = ""
#             return blank


# @app.route('/events', methods=['GET', 'POST'])
# def events():
#     global heading
#     heading = request.json
#     print heading['value']
#     return jsonify({"content":heading})

if __name__ == "__main__":
    app.run(debug=True, host=str(config.LOCAL_DNS_HOST))
