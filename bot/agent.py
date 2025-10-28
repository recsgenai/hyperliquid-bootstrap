import os, json
from dataclasses import dataclass

@dataclass
class Signal:
    action: str  # 'buy' | 'sell' | 'hold'
    confidence: float
    price: float = None

# --- OpenAI wrapper (example) ---
class OpenAIModel:
    def __init__(self, config):
        self.config = config
        self.api_key = os.getenv('OPENAI_API_KEY')
        # lazy import so project doesn't fail if library missing
        try:
            import openai
            self.openai = openai
            self.openai.api_key = self.api_key
        except Exception:
            self.openai = None

    def analyze(self, market_snapshot):
        # Example: send short prompt to OpenAI and parse the response for a signal.
        # This is a placeholder — implement rate limiting, prompt engineering, and safety.
        if self.openai is None:
            # fallback: simple heuristic
            return Signal('hold', 0.5, market_snapshot['price'])
        prompt = f"Market snapshot: {json.dumps(market_snapshot)}\nDecide: buy/sell/hold and a confidence 0..1"
        resp = self.openai.ChatCompletion.create(
            model=self.config.get('ai', {}).get('model', 'gpt-4o'),
            messages=[{'role':'user','content':prompt}],
            temperature=self.config.get('ai', {}).get('temperature', 0.2),
            max_tokens=128
        )
        text = resp['choices'][0]['message']['content'].strip().lower()
        if 'buy' in text:
            return Signal('buy', 0.6, market_snapshot['price'])
        if 'sell' in text:
            return Signal('sell', 0.6, market_snapshot['price'])
        return Signal('hold', 0.5, market_snapshot['price'])

# --- Qwen / DeepSeek placeholders ---
class QwenModel:
    def __init__(self, config):
        self.config = config
        # TODO: Implement Qwen SDK usage
    def analyze(self, market_snapshot):
        # Placeholder
        return Signal('hold', 0.5, market_snapshot['price'])

class DeepSeekModel:
    def __init__(self, config):
        self.config = config
        # TODO: Implement DeepSeek SDK usage
    def analyze(self, market_snapshot):
        return Signal('hold', 0.5, market_snapshot['price'])

# A factory that returns a model instance based on config
def get_model(config):
    name = config.get('ai', {}).get('model', 'placeholder').lower()
    if 'openai' in name or 'gpt' in name:
        return OpenAIModel(config)
    if 'qwen' in name:
        return QwenModel(config)
    if 'deepseek' in name or 'deepseek' in name:
        return DeepSeekModel(config)
    # default to simple placeholder
    from .agent import AIModelPlaceholder  # fallback to original
    return AIModelPlaceholder(config)
