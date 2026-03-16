from flask import jsonify


def api_response(status_code, mensagem, dados=None):
    body = {"status_code": status_code, "mensagem": mensagem}

    if dados is not None:
        body["dados"] = dados

    return jsonify(body)
