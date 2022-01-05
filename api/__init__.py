from flask import Flask

def create_app():
    app = Flask(__name__)

    from api.pdf_converter import gen_pdf

    app.register_blueprint(blueprint=gen_pdf, url_prefix='/')

    return app