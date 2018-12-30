import json
import re

from django.conf import settings
from esframework import import_path
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from esframework.event_handling.event_bus import BasicBus
from esframework.exceptions import AggregateRootOutOfSyncError
from esframework.repository import DefaultRepository
from esframework.store import SQLStore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from api.application.command_handler import GameCommandHandler
from api.projections.game_state import GameStateProjection
from api.projections.game_state_model import GameStateModel


def index(request) -> JsonResponse:
    return JsonResponse({"hello": "world"})


@csrf_exempt
def game_handler(request) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseBadRequest("Cannot deal with {} requests".format(request.method))

    # create command handler
    body = json.loads(request.body)
    if 'command' not in body:
        return HttpResponseBadRequest("Cannot execute request, command is missing!")

    if 'data' not in body:
        return HttpResponseBadRequest("Cannot execute request, command data is missing!")

    try:
        command_class = import_path('api.application.commands.{}'.format(body['command']))
        command = command_class(**body['data'])

        store = SQLStore(settings.DB_SESSION)
        eventbus = BasicBus()
        eventbus.subscribe(GameStateProjection(settings.DB_SESSION))
        repository = DefaultRepository('api.domain.aggregate.Game', store, eventbus)
        command_handler = GameCommandHandler(repository)

        method = "handle{0}".format(
            re.sub('([A-Z]+)', r'_\1', command.__class__.__name__).lower()
        )

        if hasattr(command_handler.__class__, method) \
                and callable(getattr(command_handler.__class__, method)):
            command_handler.__getattribute__(method)(command)

    except ImportError:
        return HttpResponseBadRequest("Command does not exist")
    except TypeError:
        return HttpResponseBadRequest("Incorrect parameters")
    except AggregateRootOutOfSyncError:
        return HttpResponse(
            status=409,
            content="Your game is out of sync please refresh and retry request (if needed)")

    return HttpResponse(status=204)


def game_status(request) -> HttpResponse:
    session = sessionmaker(bind=settings.DB_ENGINE)()
    game_id = request.GET.get('game_id')
    if not game_id:
        return HttpResponseBadRequest("No game_id supplied")

    try:
        record = session.query(GameStateModel) \
            .filter_by(aggregate_root_id=game_id) \
            .one()
    except NoResultFound:
        raise RuntimeError('Game does not exist')

    return JsonResponse(
        {
            "tries_left": record.tries_left,
            "word_state": record.word_state,
            "wrong_guessed_letters": record.wrong_guessed_letters,
            "wrong_guessed_word": record.wrong_guessed_word,
            "game_state": record.game_state
        }
    )
