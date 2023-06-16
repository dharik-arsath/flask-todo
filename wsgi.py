from app import create_app
from app.user.user_views import validate_cookie

app = create_app()


@app.before_request
def validate_cookie_before_request():
    return validate_cookie()


if __name__ == "__main__":
    # application = create_app()
    app.run(debug = True)