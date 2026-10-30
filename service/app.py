"""REST API for customer accounts."""

import os
import sqlite3
import tempfile
from contextlib import closing
from functools import wraps

from flask import Flask, jsonify, request

from service import configure_security


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.environ.get("DATABASE", os.path.join(tempfile.gettempdir(), "accounts.db")),
        API_TOKEN=os.environ.get("API_TOKEN", ""),
        CORS_ORIGINS=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    )
    if test_config:
        app.config.update(test_config)
    configure_security(app)

    def connect():
        db = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        return db

    with closing(connect()) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS accounts ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, "
            "email TEXT NOT NULL UNIQUE, balance REAL NOT NULL DEFAULT 0, "
            "active INTEGER NOT NULL DEFAULT 1)"
        )
        db.commit()

    def authorized(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = app.config["API_TOKEN"]
            if token and request.headers.get("Authorization") != f"Bearer {token}":
                return jsonify(error="Unauthorized"), 401
            return fn(*args, **kwargs)

        return wrapper

    def account(row):
        return dict(id=row["id"], name=row["name"], email=row["email"],
                    balance=row["balance"], active=bool(row["active"]))

    def validate(data, partial=False):
        if not isinstance(data, dict):
            return "JSON object required"
        if not partial and (not data.get("name") or not data.get("email")):
            return "name and email are required"
        if "name" in data and (not isinstance(data["name"], str) or not data["name"].strip()):
            return "name must be a nonempty string"
        if "email" in data and (not isinstance(data["email"], str) or "@" not in data["email"]):
            return "email must be valid"
        if "balance" in data and (
            isinstance(data["balance"], bool)
            or not isinstance(data["balance"], (int, float))
            or data["balance"] < 0
        ):
            return "balance must be a nonnegative number"
        if "active" in data and not isinstance(data["active"], bool):
            return "active must be boolean"
        return None

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/")
    def home():
        return jsonify(service="Customer Accounts", status="ok")

    @app.get("/accounts")
    @authorized
    def list_accounts():
        with closing(connect()) as db:
            rows = db.execute("SELECT * FROM accounts ORDER BY id").fetchall()
        return jsonify([account(row) for row in rows])

    @app.post("/accounts")
    @authorized
    def create_account():
        data = request.get_json(silent=True)
        error = validate(data)
        if error:
            return jsonify(error=error), 400
        try:
            with closing(connect()) as db:
                cursor = db.execute(
                    "INSERT INTO accounts (name, email, balance, active) VALUES (?, ?, ?, ?)",
                    (data["name"].strip(), data["email"].strip().lower(),
                     data.get("balance", 0), int(data.get("active", True))),
                )
                db.commit()
                row = db.execute("SELECT * FROM accounts WHERE id=?", (cursor.lastrowid,)).fetchone()
        except sqlite3.IntegrityError:
            return jsonify(error="email already exists"), 409
        return jsonify(account(row)), 201

    @app.route("/accounts/<int:account_id>", methods=["GET", "PUT", "DELETE"])
    @authorized
    def account_by_id(account_id):
        with closing(connect()) as db:
            row = db.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
            if row is None:
                return jsonify(error="account not found"), 404
            if request.method == "GET":
                return jsonify(account(row))
            if request.method == "DELETE":
                db.execute("DELETE FROM accounts WHERE id=?", (account_id,))
                db.commit()
                return "", 204
            data = request.get_json(silent=True)
            error = validate(data, partial=True)
            if error or not data:
                return jsonify(error=error or "at least one field required"), 400
            updated = account(row)
            updated.update(data)
            try:
                db.execute(
                    "UPDATE accounts SET name=?, email=?, balance=?, active=? WHERE id=?",
                    (updated["name"].strip(), updated["email"].strip().lower(),
                     updated["balance"], int(updated["active"]), account_id),
                )
                db.commit()
            except sqlite3.IntegrityError:
                return jsonify(error="email already exists"), 409
            row = db.execute("SELECT * FROM accounts WHERE id=?", (account_id,)).fetchone()
            return jsonify(account(row))

    return app


app = create_app()
