from flask import Flask
from controllers.analysis import analysis_bp
from controllers.peformance import performance_bp
from controllers.home import main_bp

app = Flask(__name__)

app.register_blueprint(analysis_bp)
app.register_blueprint(performance_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)