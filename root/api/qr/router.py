import os
import urllib

from flask import request, send_file
from path import Path

from flask import Blueprint

from root.api.qr.main_qr import gen_qr_code

NO_CACHE = False

STORE_PATH = Path("/app/store")


def download(url, path):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    opener.retrieve(url, path)


def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)


os.makedirs(STORE_PATH, exist_ok=True)
os.makedirs(STORE_PATH / "source", exist_ok=True)
os.makedirs(STORE_PATH / "result", exist_ok=True)

qr_router = Blueprint("QR", __name__)


@qr_router.route("/get_qr")
def get_qr():
    args = request.args

    url = args.get('url')
    original = args.get('original')

    if not url:
        return "No url"

    if not original:
        return "No original"

    qr_name = urllib.parse.quote_plus(
        original) + urllib.parse.quote_plus(url) + ".png"
    qr_path = Path().joinpath("store", 'result', qr_name)

    if NO_CACHE or not os.path.isfile(qr_path):
        path_to_source_image = STORE_PATH / 'source' / \
                               urllib.parse.quote_plus(original)
        path_to_save = STORE_PATH / 'result' / qr_name

        download(original, path_to_source_image)

        gen_qr_code(url, path_to_source_image, path_to_save)

        remove_file(path_to_source_image)

    return send_file('../store/result/' + qr_name)
