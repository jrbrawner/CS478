from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    make_response
)
from passlib.hash import sha256_crypt
from ..models.Users import db, User
from ..services.WebHelpers import WebHelpers
import logging
from flask import current_app as app, jsonify
from flask_cors import cross_origin
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import current_user, set_access_cookies, unset_access_cookies, unset_jwt_cookies
from datetime import datetime, timezone
from api import jwt
from api.forms.SigninForm import SigninForm
from api.forms.SignupForm import SignupForm
from api.routes.feed import create_feed


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signin", methods = ["GET", "POST"])
@jwt_required(True)
def signin_page():
    form = SigninForm()
    if form.validate_on_submit():

        # Validate login attempt
        user = User.query.filter_by(email=form.email.data).one_or_none()
        password_matches = sha256_crypt.verify(form.password.data, user.password)

        if user:
            if user and password_matches:
                # User exists and password matches password in db
                user.set_last_login()
                access_token = create_access_token(identity=user)
                resp = make_response(redirect("/feed"))

                set_access_cookies(resp, access_token)
                return resp
    return render_template("/auth/signin.html", form=form)

@auth_bp.route("/signup", methods = ["GET", "POST"])
@jwt_required(True)
def signup_page():
    form = SignupForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        major = form.major.data
        grad_year = form.grad_year.data
        username = form.username.data
        email = str(form.email.data).lower()
        password = form.password.data

        existing_user = User.query.filter_by(email=email).scalar()

        if existing_user is None:
            password = sha256_crypt.encrypt(password)
            user = User(
                first_name=first_name,
                last_name=last_name,
                major=major,
                password=password,
                grad_year=grad_year,
                username=username,
                email=email,
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            logging.info("New user created - " + str(user.id) + " - " + str(user.username))
            access_token = create_access_token(identity=user)
            resp = make_response(redirect("/feed"))

            set_access_cookies(resp, access_token)
            return resp

    return render_template('/auth/signup.html', form=form)


@auth_bp.route("/signout", methods=["GET"])
@jwt_required()
def signout_page():
    resp = make_response(redirect('/signout-page'))
    unset_jwt_cookies(resp)
    return resp

@auth_bp.route("/signout-page", methods=["GET"])
@jwt_required(True)
def signout():
   
    return render_template("/auth/signout.html")
########################################################### API BELOW, SERVER RENDERING ABOVE


@cross_origin()
@auth_bp.post("/api/users/register")
def signup():
    """
    User sign-up page.
    """

    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    major = request.form["major"]
    grad_year = request.form["gradYear"]
    username = request.form["username"]
    email = request.form["email"].lower()
    password = request.form["password"]

    existing_user = User.query.filter_by(email=email).scalar()

    if existing_user is None:
        password = sha256_crypt(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            major=major,
            password=password,
            grad_year=grad_year,
            username=username,
            email=email,
        )
        db.session.add(user)
        db.session.commit()  # Create new user
        logging.info("New user created - " + str(user.id) + " - " + str(user.username))
        access_token = create_access_token(identity=user)

        resp = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "userId": user.id,
            "token": access_token,
        }

        set_access_cookies(resp, access_token)

        return resp

    return WebHelpers.EasyResponse("User with that email already exists. ", 400)


@cross_origin()
@auth_bp.post("/api/users/login")
def login():
    """
    Log-in page for registered users.
    """

    email = request.form["email"].lower()
    password = request.form["password"]

    # Validate login attempt
    user = User.query.filter_by(email=email).one_or_none()
    password_matches = sha256_crypt.verify(password, user.password)

    if user:
        if user and password_matches:
            # User exists and password matches password in db
            user.set_last_login()
            # return WebHelpers.EasyResponse(user.username + " logged in.", 200)

            access_token = create_access_token(identity=user)

            resp = jsonify(
                {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "userId": user.id,
                    "token": access_token,
                }
            )
            set_access_cookies(resp, access_token)

            return resp

    # User exists but password does not match password in db
    return WebHelpers.EasyResponse("Invalid username/password combination.", 405)


@app.route("/api/users/me")
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        firstName=current_user.first_name,
        username=current_user.username,
    )


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


#
# @login_manager.user_loader
# def load_user(user_id):
#    """Check if user is logged-in on every page load."""
#    if user_id is not None:
#        return User.query.get(user_id)
#    return None


# @login_manager.unauthorized_handler
# def unauthorized():
#    """Redirect unauthorized users to Login page."""
#    return WebHelpers.EasyResponse("You must login to view this page", 401)


# @auth_bp.route("/api/logout", methods=["GET"])
# @login_required
# def logout():
#    """User log-out logic."""


@auth_bp.post("/api/grant_role")
def grant_role():
    """Add a role to a users account."""

    user_id = request.form["user_id"]
    role_name = request.form["role_name"]
    user = User.query.get(user_id)
    if user:
        user_datastore.add_role_to_user(user, role_name)
        db.session.commit()
        logging.warning(
            f"User id - {current_user.id} - granted {role_name} role to User id - {user_id} - "
        )
        return WebHelpers.EasyResponse("Role granted to user.", 200)
    return WebHelpers.EasyResponse("User with that id does not exist.", 404)


@auth_bp.post("/api/revoke_role")
def revoke_rule():
    """Remove a role from a users account."""

    user_id = request.form["user_id"]
    role_name = request.form["role_name"]

    user = User.query.get(user_id)
    if user:
        user_datastore.remove_role_from_user(user, role_name)
        db.session.commit()
        logging.warning(
            f"User id - {current_user.id} - revoked {role_name} role from User id - {user_id} -"
        )
        return WebHelpers.EasyResponse("Role revoked from user.", 200)
    return WebHelpers.EasyResponse("User with that id does not exist.", 404)


@auth_bp.get("/api/check_roles")
def check_roles():
    """Check a users roles."""

    user_id = request.form["user_id"]
    user = User.query.get(user_id)

    if user:
        roles = [x.serialize() for x in user.roles]
        logging.info(f"User id {current_user.id} accessed User id - {user_id} - roles")
        return roles

    username = current_user.username
    logout_user()
    return WebHelpers.EasyResponse(username + " logged out.", 200)
