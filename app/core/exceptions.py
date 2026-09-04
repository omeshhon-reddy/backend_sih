from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(404, detail)


class MissingFeaturesError(AppError):
    def __init__(
        self,
        detail: str = "ML features are required to run a prediction"
    ) -> None:
        super().__init__(422, detail)


class InferenceUnavailableError(AppError):
    def __init__(
        self,
        detail: str = "ML model is not available"
    ) -> None:
        super().__init__(503, detail)


class InferenceError(AppError):
    def __init__(
        self,
        detail: str = "Risk prediction failed"
    ) -> None:
        super().__init__(500, detail)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request,
        exc: AppError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(
        request: Request,
        exc: SQLAlchemyError
    ) -> JSONResponse:

        # Print the COMPLETE database error in the Uvicorn terminal
        logger.exception("DATABASE ERROR")

        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            }
        )