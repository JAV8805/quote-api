from flask import Flask, jsonify, request

app = Flask(__name__)


def quote_premium(age: int, coverage: float) -> float:
    """Annual premium: 1.2% of coverage, +50% loading from age 60."""
    if age < 18 or coverage <= 0:
        raise ValueError("invalid input")
    base = coverage * 0.012
    factor = 1.5 if age >= 60 else 1.0
    return round(base * factor, 2)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/quote")
def quote():
    data = request.get_json(silent=True) or {}
    try:
        premium = quote_premium(int(data["age"]), float(data["coverage"]))
    except (KeyError, ValueError, TypeError):
        return jsonify(error="invalid input"), 400
    return jsonify(premium=premium)