import json
def load_env(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}
