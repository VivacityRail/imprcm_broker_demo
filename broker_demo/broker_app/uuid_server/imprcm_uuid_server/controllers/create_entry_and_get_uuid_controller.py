import connexion
import six

from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server import util, db


def id_server_entities_post(new_item=None):  # noqa: E501
    """add details of an entry and get its uuid

     # noqa: E501

    :param new_item: 
    :type new_item: dict | bytes

    :rtype: EntitySchemaWithUri
    """
    RESPONSES = {'new': 201, 'update': 200, 'invalid': 400, 'not implemented': 501}
    HTTP_CODES = {200: 'OK', 201: 'Created', 400: 'Bad Request', 501: 'Not Implemented'}

    if connexion.request.is_json:
        new_item = EntitySchemaNoUuid.from_dict(connexion.request.get_json()) # noqa: E501

        new_uuid, status, the_item, error = db.post_item_as_json(new_item)
        #print('uuid ', new_uuid, 'item', the_item, 'error', error)


    if error:
        # return error object per RFC 7807
        error['status'] = RESPONSES[status]
        error['title']= HTTP_CODES[RESPONSES[status]]
        print(error)
        return error, RESPONSES[status]
    else:
        item_uri = 'https://api.imprcm.vivacityrail.com/id-server/entities_by_uuid/{0}'.format(new_uuid)
        return_body = EntitySchemaWithUri(entity_uri=item_uri, entity_object=the_item)
        print(return_body)
        return return_body, RESPONSES[status]

    return the_item
