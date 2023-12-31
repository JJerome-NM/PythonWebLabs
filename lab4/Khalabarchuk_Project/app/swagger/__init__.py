from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger-ui'
API_URL = '../static/swagger/swagger.yaml'

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'WebPython-Fifteen-Lab'
    }
)