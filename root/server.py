import os
import urllib

from path import Path

from root.db.categories.router import category_router
from root.db.location.router import location_router
from root.db.qr.router import qr_router
from root.db.text.router import text_router
from root.create_app import app

# NO_CACHE = False
#
# STORE_PATH = Path("/app/store")
#
#
# def download(url, path):
#     opener = urllib.request.URLopener()
#     opener.addheader('User-Agent', 'whatever')
#     opener.retrieve(url, path)
#
#
# def remove_file(path):
#     if os.path.isfile(path):
#         os.remove(path)
#
#
# os.makedirs(STORE_PATH, exist_ok=True)
# os.makedirs(STORE_PATH / "source", exist_ok=True)
# os.makedirs(STORE_PATH / "result", exist_ok=True)


def create_app():
    # app = Flask(__name__)
    # CORS(app)

    app.register_blueprint(category_router)
    app.register_blueprint(location_router)
    app.register_blueprint(qr_router)
    app.register_blueprint(text_router)

    # load_dotenv(".env")
    #
    # USER = os.getenv("USER")
    # PASSWORD = os.getenv("PASSWORD")
    # HOST = os.getenv("HOST")
    # PORT = os.getenv("PORT")
    # DB = os.getenv("DB")
    # AUTH = os.getenv("AUTH")
    #
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=disable"
    # db = SQLAlchemy(app)

    # @app.route("/")
    # @app.route("/translated_text")
    # def translated_text():
    #     authorization_header = request.headers.get("Authorization")
    #
    #     if not is_authorized(
    #             token_to_validate=AUTH, token_from_request=authorization_header
    #     ):
    #         abort(403)
    #     args = request.args
    #
    #     text_to_translate = args.get("text")
    #     target_language = args.get("tl")
    #
    #     if not text_to_translate:
    #         return "No text"
    #
    #     if not target_language:
    #         return "No target language"
    #
    #     search_result = search_text(
    #         text_to_translate=text_to_translate,
    #         table="translation_result",
    #         language=target_language,
    #         db=db,
    #     )
    #
    #     if search_result:
    #         result = search_result[0]["translated_text"]
    #         last_access_register(
    #             text_to_translate=text_to_translate,
    #             table="translation_result",
    #             language=target_language,
    #             db=db,
    #         )
    #     else:
    #         result = translate(text_to_translate, target_language)
    #         cache_text(
    #             text_to_translate=text_to_translate,
    #             table="translation_result",
    #             language=target_language,
    #             result=result,
    #             db=db,
    #         )
    #
    #     return result

    # @app.route("/get_category", methods=["POST"])
    # def get_category():
    #     authorization_header = request.headers.get("Authorization")
    #
    #     if not is_authorized(
    #             token_to_validate=AUTH, token_from_request=authorization_header
    #     ):
    #         abort(403)
    #
    #     text = request.form.get("text")
    #     if not text:
    #         return "No text"
    #
    #     search_result = search_category(
    #         text_to_category=text,
    #         db=db,
    #     )[0]
    #
    #     if search_result:
    #         result = search_result
    #         last_access_register_category_cache(
    #             text_to_category=text,
    #             db=db,
    #         )
    #     else:
    #         result = categoryController.get_category(text)
    #
    #         cache_category_text(
    #             text_to_category=text,
    #             result=result,
    #             db=db,
    #         )
    #
    #     return result

    # @app.route("/get_all_categories", methods=["GET"])
    # def get_all_categories():
    #     authorization_header = request.headers.get("Authorization")
    #
    #     if not is_authorized(
    #             token_to_validate=AUTH, token_from_request=authorization_header
    #     ):
    #         abort(403)
    #
    #     return categories
    #
    # @app.route("/get_description_for_location", methods=["POST"])
    # def get_description_for_location():
    #     authorization_header = request.headers.get("Authorization")
    #
    #     if not is_authorized(
    #             token_to_validate=AUTH, token_from_request=authorization_header
    #     ):
    #         abort(403)
    #
    #     language = request.form.get("language")
    #     location = request.form.get("location")
    #
    #     if not language:
    #         return "No language"
    #
    #     if language not in ["en", "ru"]:
    #         return "Wrong language, only en and ru are supported"
    #
    #     if not location:
    #         return "No location"
    #
    #     return locationDescriptionController.get_description(location, language)
    #
    # @app.route("/get_seo_optimised_text", methods=["POST"])
    # def get_seo_optimised_text():
    #     authorization_header = request.headers.get("Authorization")
    #
    #     if not is_authorized(
    #             token_to_validate=AUTH, token_from_request=authorization_header
    #     ):
    #         abort(403)
    #
    #     language = request.form.get("language")
    #     text = request.form.get("text")
    #
    #     if not language:
    #         return "No language"
    #
    #     if language not in ["en", "ru"]:
    #         return "Wrong language, only en and ru are supported"
    #
    #     if not text:
    #         return "No text"
    #
    #     return seoOptimisationController.get_text(text, language)
    #
    # @app.route("/get_qr")
    # def get_qr():
    #     args = request.args
    #
    #     url = args.get('url')
    #     original = args.get('original')
    #
    #     if not url:
    #         return "No url"
    #
    #     if not original:
    #         return "No original"
    #
    #     qr_name = urllib.parse.quote_plus(
    #         original) + urllib.parse.quote_plus(url) + ".png"
    #     qr_path = Path().joinpath("store", 'result', qr_name)
    #
    #     if NO_CACHE or not os.path.isfile(qr_path):
    #         path_to_source_image = STORE_PATH / 'source' / \
    #                                urllib.parse.quote_plus(original)
    #         path_to_save = STORE_PATH / 'result' / qr_name
    #
    #         download(original, path_to_source_image)
    #
    #         gen_qr_code(url, path_to_source_image, path_to_save)
    #
    #         remove_file(path_to_source_image)
    #
    #     return send_file('../store/result/' + qr_name)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0")
