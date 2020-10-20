#!/usr/bin/env python3
import argparse
from imprcm_uuid_server import startup

SWAGGER_DIR = 'swagger/'
DATABASE_URL = 'sqlite:///uuid_data.sqlite3'

serv_port = '8080'
database_url = DATABASE_URL

def main():
    the_app = startup.create_cnxn_app(spec_dir=SWAGGER_DIR, db_url=database_url)
    the_app.run(port=serv_port)


if __name__ == '__main__':
    # pick up host and port from the command line
    parser = argparse.ArgumentParser(description='UUID server')
    parser.add_argument('--port', type=str, default='8080' )
    parser.add_argument('--host', type=str, default='localhost' )
    parser.add_argument('--database', type=str, default=DATABASE_URL )
    the_args = parser.parse_args()
    serv_port = the_args.port
    database_url = the_args.database

    # update the swagger host file 
    startup.update_swagger_host(SWAGGER_DIR, the_args.host, serv_port)

    main()
