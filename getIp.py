from flask import Flask,request

app = Flask(__name__)


@app.route('/')
def hello_world():
    ip=request.remote_addr
    return ip


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9999')