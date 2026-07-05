import uuid

from fastapi import Cookie, Response

COOKIE_NAME = "zov_player"


def get_player_id(
    response: Response,
    player_id: str | None = Cookie(default=None, alias=COOKIE_NAME),
) -> str:
    if not player_id or len(player_id) < 32:
        player_id = str(uuid.uuid4())
        response.set_cookie(
            key=COOKIE_NAME,
            value=player_id,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
        )
    return player_id
