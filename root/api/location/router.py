from flask import Blueprint, request

from root.api.location.location_description_controller import (
    locationDescriptionController,
)
from root.auth import check_authorization

location_router = Blueprint("Location", __name__)


@location_router.route("/get_description_for_location", methods=["POST"])
@check_authorization
def get_description_for_location():
    language = request.form.get("language")
    location = request.form.get("location")

    if not language:
        return "No language"

    if language not in ["en", "ru"]:
        return "Wrong language, only en and ru are supported"

    if not location:
        return "No location"

    return locationDescriptionController.get_description(location, language)
