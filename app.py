"""
Minimal Flask app — deliberately tiny.

The POINT of this app is to be boring. Every line of it exists to give
the pipeline something real to build, test, deploy and verify.
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Injected by the pipeline at deploy time so you can PROVE which build
# is live. This is how you verify a deployment actually happened.
VERSION = os.environ.get("APP_VERSION", "dev")
ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "local")


@app.route("/")
def home():
    return f"""
    <html><body style="font-family: system-ui; padding: 3rem; text-align:center">
      <h1>CI/CD Practice App</h1>
      <p>Environment: <strong>{ENVIRONMENT}</strong></p>
      <p>Version: <strong>{VERSION}</strong></p>
    </body></html>
    """


@app.route("/health")
def health():
    """Smoke-test target. The pipeline calls this after deploying."""
    return jsonify(status="ok", version=VERSION, environment=ENVIRONMENT)


@app.route("/api/add/<int:a>/<int:b>")
def add(a, b):
    """Something with actual logic, so tests have something to assert."""
    return jsonify(result=a + b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
