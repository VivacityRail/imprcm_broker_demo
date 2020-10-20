import connexion
import six

from imprcm_uuid_server.models.entity_schema_url_array import EntitySchemaUrlArray  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server import util, db

def id_server_entities_get(entity=None, schema=None, fromdate=None):  # noqa: E501
    """get the uuids for a matching set of details

     # noqa: E501

    :param entity: 
    :type entity: str
    :param schema: 
    :type schema: str
    :param fromdate: 
    :type fromdate: str

    :rtype: EntitySchemaUrlArray
    """
    # return a list of dicts, each of which is structured according to the elements of the required response
    RESPONSES = {'data': 200, 'new': 201, 'update': 200, 'invalid': 400, 'no data': 404, 'not implemented': 501}
    HTTP_CODES = {200: 'OK', 201: 'Created', 400: 'Bad Request', 404: 'Not Found', 501: 'Not Implemented'}


    results, status, error = db.get_matching_details_as_json(scheme_url=schema, name_url=entity, effective_timestamp=fromdate)
    if error:
        # return error object per RFC 7807
        error['status'] = RESPONSES[status]
        error['title']= HTTP_CODES[RESPONSES[status]]
        return error, RESPONSES[status]
    else:
        return_body = [EntitySchemaWithUri(entity_uri='/id-server/entities_by_uuid/{}'.format(item.uuid), 
                                           entity_object=item) for item in results]
        return return_body, RESPONSES[status]

