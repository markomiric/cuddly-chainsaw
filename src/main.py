from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.config import settings, logger
from src.files.router import router as files_router


# flake8: noqa: W291
def create_application() -> FastAPI:
    application = FastAPI(app_name="Files API", title="Files API", version="1.0.0")

    application.mount("/static", StaticFiles(directory=str(Path("static").resolve())), name="static")

    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Exception: {exc}")
        message = "Something went wrong!"
        if hasattr(exc, "details"):
            message = exc.detail

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"message": message}),
        )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(files_router, prefix="/api/v1")

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    logger.info("Service is healthy and running!")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
