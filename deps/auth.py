from fastapi import Header, HTTPException

from config.jwt import decode_token

async def get_current_admin(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    if authorization.lower().startswith('bearer '):
        token = authorization.split(' ', 1)[1]
    else:
        token = authorization
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    return payload
