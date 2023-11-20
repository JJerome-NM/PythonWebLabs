from app import create_app
from config import Config

config = Config.get_config()

app = create_app(config)

if __name__ == '__main__':
    app.run()
