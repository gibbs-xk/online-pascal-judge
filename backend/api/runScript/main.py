import subprocess
import sys
from pathlib import Path

from flask import Blueprint, request, jsonify

run = Blueprint('run', __name__)
root_dir = Path(__file__).resolve().parents[2]
interpreter_path = root_dir / "pascal.py"

@run.route('/languages', methods=["GET"])
def languages():
    return jsonify(["pascal"])


def _run_script(script_text):
    if not interpreter_path.exists():
        return {"stdout": "", "stderr": "Interpreter not found.", "returncode": 1}

    try:
        result = subprocess.run(
            [sys.executable, str(interpreter_path), script_text],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out.", "returncode": 124}

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


@run.route('/code_run', methods=["POST"])
def code_run():
    incoming_data = request.get_json(silent=True) or {}
    script_text = incoming_data.get("script", "")
    return jsonify(_run_script(script_text))


@run.route('/', methods=["POST"])
def execute():
    incoming_data = request.get_json(silent=True) or {}
    script_text = incoming_data.get("script", "")
    return jsonify(_run_script(script_text))
