import msal
import os
from flask import Flask, session, redirect, url_for, request, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = 'some secret'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Replace these with your own values
TENANT_ID = os.environ.get("a52f2f56-992b-44d5-8250-1d2733397dbb")
CLIENT_ID = os.environ.get("abe4ba25-f73a-4b39-9516-a8625cf7ff16")
CLIENT_SECRET = os.environ.get("23f9bd17-cbeb-46e4-a777-3d0714f9a6c1")
ENDPOINT = os.environ.get("ENDPOINT")
SCOPE = os.environ.get("SCOPE")
REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL; must match to app's redirect_uri set in AAD

@app.route("/")
def index():
    return render_template('signup.html')

@app.route('/login')
def login():
    session.clear()
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=ENDPOINT, client_credential=CLIENT_SECRET
    )
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for("authorized", _external=True, _scheme="https")
    )
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    code = request.args.get('code')
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=ENDPOINT, client_credential=CLIENT_SECRET
    )
    token_response = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("authorized", _external=True, _scheme="https")
    )
    if "access_token" in token_response:
        session["user"] = token_response.get("id_token_claims")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        os.environ.get(
            "AUTHORITY",
            "https://login.microsoftonline.com/" + TENANT_ID
        ) + "/oauth2/v2.0/logout"
        "?post_logout_redirect_uri=" + url_for("index", _external=True)
    )

if __name__ == "__main__":
    app.run(port=5000, ssl_context="adhoc")
