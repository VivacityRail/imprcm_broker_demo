#!/usr/bin/env python3
import argparse
from imprcm_query_server import startup

SWAGGER_DIR = 'swagger/'
DATABASE_URL = 'postgresql://pete@vivienne01/imprcm_demo_ugms_touchdown'

serv_port = '8080'
database_url = DATABASE_URL

def main():
    the_app = startup.create_cnxn_app(spec_dir=SWAGGER_DIR, db_url=database_url)
    print('serving outbound s and c API', flush=True)
    the_app.run(port=serv_port)


if __name__ == '__main__':
    # pick up host and port from the command line
    parser = argparse.ArgumentParser(description='Query server')
    parser.add_argument('--port', type=str, default='8080' )
    parser.add_argument('--extport', type=str, default='8085' )
    parser.add_argument('--host', type=str, default='localhost' )
    parser.add_argument('--database', type=str, default=DATABASE_URL )
    the_args = parser.parse_args()
    serv_port = the_args.port
    external_port = the_args.extport
    database_url = the_args.database

    # update the swagger file to set host and port
    startup.update_swagger_host(SWAGGER_DIR, the_args.host, external_port)

    main()
