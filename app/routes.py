from app import app

@app.route('/')
def home():
    return "Ласкаво просимо до Домашньої Аптечки!"