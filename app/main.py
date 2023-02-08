from fastapi import FastAPI
from routers import weather
from schemas import LoginData, Token
from auth import authenticate_user, create_token

app = FastAPI()
app.include_router(weather.router)


@app.get('/')
def home():
    return 'Weather api'


@app.post('/token')
def login(login_data: LoginData) -> Token:
    user = authenticate_user(**login_data.dict())
    token_str = create_token(user)
    token = Token(access_token=token_str, token_type='bearer')
    return token
