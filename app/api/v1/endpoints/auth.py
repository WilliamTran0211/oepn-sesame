import logging
from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger("open_sesame_logger")


@router.get("/")
def read_root():
    logger.debug("Root endpoint accessed")
    return {"message": "Open Sesame, Authentication!"}


@router.post("/hello")
def post_root():
    logger.debug("Root endpoint accessed")
    return {"message": "Open Sesame, Authentication!"}
