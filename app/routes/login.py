from .. import app
from ..models import User, db

from flask import redirect, url_for, make_response
from flask_dance.contrib.google import google
from flask_login import login_user, logout_user, current_user
import os
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

# https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=791695136888-89i5764vvj48uoi3435jf32pc9dnolu7.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth%2Fgoogle%2Fauthorized&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+openid&state=0NmkLolNYJNxMDg12UrS7dLHZDlVv4&access_type=offline&prompt=consent

@app.route('/login')
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    token_url = "https://oauth2.googleapis.com/token"

    if not google.authorized:
        return redirect(url_for('auth'))
    
    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        if resp.status_code == 401:
            refresh_token = google.token.get('refresh_token')
            if refresh_token:
                print(f"refresh_token: {refresh_token}")
                try:
                    token = google.refresh_token(token_url, refresh_token=refresh_token, client_id=os.getenv("GOOGLE_CLIENT_ID"), client_secret=os.getenv("GOOGLE_CLIENT_SECRET"))
                except InvalidGrantError:
                    print("Refresh token is invalid. Clearing token and redirecting user to login.")
                    google.token = None  # Clear the invalid token
                    return redirect(url_for('auth'))
                if token:
                    google.token = token
                else:
                    print("Failed to refresh token")
            else:
                print("No refresh token found")

    assert resp.ok, resp.text
    # rest of your code
    data = resp.json()
    user_id = data["id"]
    name = data["name"]
    email = data["email"]
    profile_pic = data["picture"]
    google_token = google.token['access_token']  # Get the Google token
    refresh_token = google.token['refresh_token']

    user = User.query.filter_by(google_id=user_id).first()
    if not user:
        user = User(
            id=user_id,
            google_id=user_id,
            name=name,
            email=email,
            profile_pic_url=profile_pic,
            google_token=google_token,  # Save the Google token
            refresh_token=refresh_token
        )
        db.session.add(user)
    else:
        user.name = name
        user.email = email
        user.profile_pic_url = profile_pic
        user.google_token = google_token  # Update the Google token
        user.refresh_token = refresh_token

    db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if current_user.is_authenticated:
        token = current_user.google_token  # Get the Google token

        if token:
            try:
                resp = google.post('https://accounts.google.com/o/oauth2/revoke',
                                    params={'token': token},
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})
                if not resp.ok:
                    print(f"Failed to revoke token: {resp.text}")
            except InvalidGrantError:
                print("Token has been expired or revoked.")

        # Logout the user regardless of the token revocation result
        logout_user()

    response = make_response(redirect(url_for('logout')))
    response.delete_cookie('session')

    return response

@app.route('/auth')
def auth():
    response = redirect(url_for('index'))
    response.delete_cookie('session')
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    # Get the new token from Google
    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        data = resp.json()
        user_id = data["id"]
        google_token = google.token['access_token']  # Get the new Google token
        refresh_token = google.token['refresh_token']

        # Store the new token
        user = User.query.filter_by(google_id=user_id).first()
        if user:
            user.google_token = google_token  # Update the Google token
            user.refresh_token = refresh_token
            db.session.commit()

    return redirect(url_for('index'))  # redirect to index instead of login