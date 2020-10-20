from os import path, getcwd
from yaml import load, dump
from flask_sqlalchemy import SQLAlchemy
from imprcm_query_server import db, encoder
import connexion
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def create_cnxn_app(spec_dir, db_url):
    app = connexion.App(__name__, specification_dir=spec_dir)

    # sentry configuration
    sentry_sdk.init(
    dsn="https://8a9de4acc7b94e03a2449aad674a5b29@sentry.io/1416850",
    integrations=[FlaskIntegration()]
    )

    # db configuration
    db.setup_app_db(flask_app=app.app, db_url=db_url)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Query API'})

    # with app.app.app_context():
    #     print(db.SandC_Summary.query.all())

    return app

def update_swagger_host(swagger_dir, host, port):
    '''
        update_swagger_host:
        update the host:port in the swagger spec to match those passed in
    '''
    swagfile = path.join(path.dirname(path.realpath(__file__)), swagger_dir, 'swagger.yaml')
    # print(swagfile)
    # print(port)
    with open(swagfile, 'r+') as f:
        swag = load(f)

    swag['host'] = host + ':' + port
    with open(swagfile, "w") as f:
        dump(swag, f)


# def create_all_tables(db_url):
#     # initialise the database. NOTE THIS UPDATES ALL THE TABLES. USE WITH CARE!!!
#     app = create_cnxn_app('./swagger', db_url)
#     db.the_db.create_all(app=app.app)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query server')
    parser.add_argument('--swagger_dir', type=str, default='swagger/' )
    parser.add_argument('db_url', type=str)
    the_args = parser.parse_args()
    create_cnxn_app(the_args.swagger_dir, the_args.db_url)

