from fastapi import FastAPI
from fastapi.requests import Request

from api import routers
from db import initialize_db
from exception import AuthorizeTemplateException
from settings import TEMPLATES
from utils.keys import check_keys_file_exists
from fastapi.middleware.cors import CORSMiddleware

# Приложение
app = FastAPI()


# Функции инициализации
check_keys_file_exists()
initialize_db()

origins = ["http://localhost:8011", "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация api маршрутов
for i in routers:
    app.include_router(i)


# Определение своей обработки ошибок для шаблонов
@app.exception_handler(AuthorizeTemplateException)
async def authorize_exception_handler(
    request: Request, exc: AuthorizeTemplateException
):
    return TEMPLATES.TemplateResponse(
        request=request, name="login_error.html", context={"detail": exc.detail}
    )


@app.get("/test")
async def test_page(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="test.html", context={})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host='0.0.0.0', port=8000)