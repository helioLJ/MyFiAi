from .. import app
from ..models import User, db

from flask import redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from .. import app, db
from ..models import User
import os

# Configuração do OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  # Adicione esta linha
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Aqui você pode usar as informações do usuário para criar um novo usuário em seu banco de dados
    # e iniciar uma sessão para esse usuário
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User()
        user.id = user_info['id']
        user.name = user_info['name']
        user.email = user_info['email']
        user.google_id = user_info['id']
        user.google_token = token['access_token']
        user.refresh_token = token.get('refresh_token')
        user.profile_pic_url = user_info['picture']
        user.is_active = True
        db.session.add(user)
        db.session.commit()
    else:
        user.google_token = token['access_token']
        if token.get('refresh_token'):
            user.refresh_token = token['refresh_token']
        db.session.commit()
    login_user(user)  # Log in the user
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))