from root.api.censorship.main import EventsValidator

from flask import request, abort, jsonify
from root.api.censorship.types.validator_types import EventValidatorResult, PostEventPayload
from flask import Blueprint


censorship_router = Blueprint("Censorship", __name__)


@censorship_router.route("/api/validation/v1.0", methods=['POST'])
def validate():
    event: PostEventPayload = request.json
    if not event:  # если прилетел не json
        abort(400)
    event_to_validate = EventsValidator()
    result: EventValidatorResult = event_to_validate.validate_event(event=event)
    return jsonify(result)  # возвращаем результат в виде json
