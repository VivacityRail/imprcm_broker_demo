import connexion
import six

from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: E501
from imprcm_uuid_server import util, db
#from imprcm_uuid_server.controllers.get_details_for_uuid_controller import id_server_uuids_uuid_get
from flask import json



def id_server_uuids_uuid_get(uuid):  # noqa: E501
    """get the details for a UUID

     # noqa: E501

    :param uuid: 
    :type uuid: str

    :rtype: EntitySchemaArray
    """
    # return a list of dicts, each of which is structured according to the elements of the required response
    RESPONSES = {'data': 200, 'new': 201, 'update': 200, 'invalid': 400, 'no data': 404, 'not implemented': 501}
    HTTP_CODES = {200: 'OK', 201: 'Created', 400: 'Bad Request', 404: 'Not Found', 501: 'Not Implemented'}


    results, status, error = db.get_item_by_uuid_as_json(uuid)
    if error:
        # return error object per RFC 7807
        error['status'] = RESPONSES[status]
        error['title']= HTTP_CODES[RESPONSES[status]]
        print(error)
        return error, RESPONSES[status]
    else:
        item_uri = 'https://api.imprcm.vivacityrail.com/id-server/entities_by_uuid/{0}'.format(uuid)
        return_body = [EntitySchemaWithUri(entity_uri=item_uri, entity_object=item) for item in results]
        return return_body, RESPONSES[status]

