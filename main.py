from flask import Flask, Blueprint, render_template
from controllers import clientController, packagesController, invoicesController

app = Flask(__name__)

app.register_blueprint(clientController.app_client)
app.register_blueprint(packagesController.app_packages)
app.register_blueprint(invoicesController.app_invoices)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=8080)
    index()



