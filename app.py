from flask import Flask, request, render_template, jsonify, redirect, flash, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "sqli-lab"  # Required for session and flash

@app.route('/')
def index():
    # Show SQLi hint only after 2 failed login attempts (you can change this threshold)
    show_hint = session.get("failed_attempts", 0) >= 2
    return render_template("login.html", show_hint=show_hint)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Hash both username and password to match stored MD5s
    username_hash = hashlib.md5(username.encode()).hexdigest()
    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username_hash}' AND password = '{password_hash}'"

    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            session.pop("failed_attempts", None)  # Reset on success
            return redirect('/success')
        else:
            # Increment failed login attempts
            session["failed_attempts"] = session.get("failed_attempts", 0) + 1
            flash("Login failed! Try SQL injection and decode the MD5.")
            return redirect('/')
    except Exception as e:
        flash(str(e))
        return redirect('/')
    finally:
        conn.close()

@app.route('/success')
def success():
    return "<h1>✅ Login Successful</h1>"

# 🚨 UNSAFE SQL EXECUTION ENDPOINT (for testing only)
@app.route('/api/inject', methods=['POST'])
def inject():
    sql = request.form.get("query")
    try:
        conn = sqlite3.connect("users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
# This code is a simple Flask application that simulates a SQL injection lab.
# It allows users to attempt login with MD5 hashed credentials and provides an endpoint for unsafe SQL execution.
# The application uses SQLite for user data storage and provides a basic HTML interface for login.