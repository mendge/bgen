# coding=utf-8
from flask import Flask, request, jsonify
import urllib

app = Flask(__name__)


@app.route("/get/sum", methods=["GET", "POST"])
def get_sum():
    # print("header {}".format(request.headers))
    # print("args ", request.args)
    # print("form {}".format(request.form.to_dict()))
    url = request.form.to_dict()['mcontent']
    print('\n\n')
    print('接收到url:',url)
    print('\n\n')
    info = {}
    info['state'] = "接收成功"
    return jsonify(info)


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run(host="127.0.0.1", port=8080)