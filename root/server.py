from path import Path

from flask import Flask, request

import os
import os.path

from mtranslate import translate


NO_CACHE = False

STORE_PATH = Path().joinpath("store")



def create_app():
    app = Flask(__name__)

    os.makedirs(STORE_PATH, exist_ok=True)

    @app.route("/")
    def hello():
        return translate("Hello World", "ru")

    return app


if __name__ == "__main__":

    create_app().run(host="0.0.0.0")
