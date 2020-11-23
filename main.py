from flask import Flask, request, jsonify, render_template, Response
from services import candidates, users
from functools import wraps
from flask_cors import CORS, cross_origin
import jwt

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 한글 지원
app.config['JWT_SECRET_KEY'] = "ceos2020"
CORS(app, resources={r'*': {'origins': '*'}})

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token:
            try:
                payload = jwt.decode(access_token, app.config['JWT_SECRET_KEY'])
            except jwt.InvalidTokenError:
                payload = None
            if not payload:
                return "Unauthorized", 401
            email = payload['email']
            user = users.get_user_by_email(email)
        else:
            return "Unauthorized", 401
        return f(*args, **kwargs)

    return decorated_function;


@app.route("/candidates")
def get_candidates():
    return jsonify(candidates.candidates())

@app.route("/vote")
@login_required
def vote_to():
    id = request.args.get("id")
    candidate = candidates.get_candidate(id)
    if candidate:
        candidates.vote(id)
        return f"Successfully Voted to {candidate['name']}", 200
    else:
        return f"Candidate does not exist", 404

@app.route("/reset")
def reset():
    candidates.reset_votes()
    return "Success", 200


@app.route("/auth/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    if not (email and password and name):
        return "Bad Request", 400

    user = users.get_user_by_email(email)
    if user:
        return f"User with email {email} already exists", 409 # conflict
    users.create_user(email, password, name)
    return "Successfully Generated", 201

@app.route("/auth/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not (email and password):
        return "Bad Request", 400
    if users.verify_user(email, password):
        token = jwt.encode({"email": email}, app.config['JWT_SECRET_KEY'])
        return token
    return "Login Failed", 404

# Page Rendering
@app.route("/")
def home():
    candidate_list = candidates.candidates()
    candidate_list.sort(key=lambda candidate: candidate['id'])
    # candidate_list.sort(key=lambda candidate: candidate['voteCount'])
    return render_template("index.html", candidate_list=candidate_list)

app.run(port=8080, host="0.0.0.0")
