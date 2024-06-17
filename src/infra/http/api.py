import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.infra.http.use_cases.Auth import Auth
from src.infra.http.use_cases.Account import Account
from src.infra.http.use_cases.Game import Game

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app.mount("/assets", StaticFiles(directory=os.path.join(os.path.dirname(__file__), '../assets')), name="assets")
app.mount("/images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates/static/images')), name="images")
app.mount("/js", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates/static/js')), name="js")
app.mount("/css", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'templates/static/css')), name="css")


@app.get("/", response_class=HTMLResponse)  
def read_home(request: Request):
    return templates.TemplateResponse(
        name="home.html",
        context={ 'request': request, 'errors': request.query_params.get('errors') })


@app.get("/signup", response_class=HTMLResponse)  
def read_signup(request: Request):
    return render(request=request, is_signup=True)


@app.get("/signin", response_class=HTMLResponse)  
def read_signup(request: Request):
    return render(request=request, is_signing=True)


@app.get("/menu", response_class=HTMLResponse)
def read_menu(request: Request):
    return render(request=request, template_name='menu.html')


@app.get("/transactions", response_class=HTMLResponse)
def read_transactions(request: Request):
    return render(request=request, template_name='transactions.html')


@app.get("/in_game", response_class=HTMLResponse)
def read_in_game(request: Request):
    return render(request=request, template_name="in_game.html")


@app.get("/playing")
def read_playing(request: Request, bet_value: int | str):
    return render(request=request, bet_value=int(bet_value))


def render(
        request: Request,
        template_name: str | None = None,
        bet_value: int | None = None,
        is_signup: bool | None = None,
        is_signing: bool = None):
    
    token = None
    player = None

    if is_signup:
        token = Account.create_player(auth=request.headers.get('Authorization'))
    elif is_signing:
        token = Auth.authenticate(auth=request.headers.get('Authorization'))
    else:
        player = Auth.validate_token(auth=request.query_params.get('token'))

    if player:
        wallet = Account.get_player_wallet(player_id=player.id)
        if bet_value:
            game = Game(wallet=wallet, bet_value=bet_value)
            game.play()
            
            return JSONResponse(content=game.updates)
        else:
            return templates.TemplateResponse(
                name=template_name,
                context={ 'request': request, 'player': player, 'wallet': wallet })
    elif token:
        return JSONResponse({ 'token': token })
    else:
        if is_signup:
            return JSONResponse({ 'error': 'UserAlreadyExists' })
        elif is_signing:
            return JSONResponse({ 'error': 'AuthFailed' })
        else:  
            return read_home(request=request)
