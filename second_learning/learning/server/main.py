from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from exceptions import StoryException
from router import blog_get, blog_post, user, article, product, file, dependencies
from auth import authentication
from db import models
from db.database import engine
import logging
import random
import string
import time

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(authentication.router)
app.include_router(dependencies.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response


@app.get('/')
def index():
    return {'message': 'Hello FastAPI'}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


models.Base.metadata.create_all(engine)

# 内部に保存してあるファイルを表示できるようにする。
app.mount('/files', StaticFiles(directory='files'), name='files')