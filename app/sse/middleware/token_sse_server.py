from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

exclude = [
    '/api/login',
    '/api/docs',
    '/sse/ping',
]


class Middleware_Token_SSE_SERVER(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str = "",
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        if (
            request.url.path not in exclude and
            not (request.url.path.find("/sse/subscribe") > -1)
            ):
            sse_server_token = request.headers.get('SSE-SERVER-KEY',None)
            if sse_server_token is None : 
                return JSONResponse(
                    status_code=401,
                    content={
                        "error" :  "Unauthorized",
                        "msg"   :  "require SSE-SERVER-KEY for first authorized"
                    }
                )
            if sse_server_token != request.app.custom_setting.data['BASE']['security']['token_sse_server']:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error" :  "Unauthorized",
                        "msg"   :  "SSE-SERVER-KEY not match"
                    }
                )
                
        response = await call_next(request)
        return response
