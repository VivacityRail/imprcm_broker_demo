import connexion
import six

from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: E501
from imprcm_uuid_server import util, db
from imprcm_uuid_server.controllers.get_details_for_uuid_controller import id_server_uuids_uuid_get
from flask import json


def id_server_uuids_uuid_put(scheme_url, name_url, fromtimestamp, uuid, new_item=None):  # noqa: E501
    """add a new item with known uuid and a reference

     # noqa: E501

    :param uuid: 
    :type uuid: str
    :param new_item: 
    :type new_item: dict | bytes

    :rtype: None
    """

    # adds a new item to the database and returns its representation 

    # returns 200 if item updated; 201 if item added
    # TODO: make response JSON-API compliant

    RESPONSES = {'new': 201, 'update': 200, 'invalid': 400, 'not implemented': 501}
    HTTP_CODES = {200: 'OK', 201: 'Created', 400: 'Bad Request', 501: 'Not Implemented'}


    if connexion.request.is_json:
        new_item = EntitySchemaWithUuid.from_dict(connexion.request.get_json())
        new_uuid, status, error = db.put_item_with_uuid_as_json(
            scheme_url=scheme_url,
            name_url=name_url,
            fromtimestamp=fromtimestamp,
            uuid_url=uuid, 
            new_entity_with_uuid=new_item) # status is "new" or "updated"

    # print('ctrlr - new uuid: {0}, status: {1}, error: {2}'.format(new_uuid, status, error))
    if error:
        # return error object per RFC 7807
        error['status'] = RESPONSES[status]
        error['title']= HTTP_CODES[RESPONSES[status]]
        return error, RESPONSES[status]
    else:
        item_uri = 'https://api.imprcm.vivacityrail.com/id-server/entities_by_uuid/{0}'.format(new_uuid)
        return_body = EntitySchemaWithUri(entity_uri=item_uri, entity_object=new_item)
        print(return_body)
        return return_body, RESPONSES[status]
