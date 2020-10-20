# coding: utf-8

#from __future__ import absolute_import

from flask import json
from six import BytesIO
import uuid
import ast

from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: E501

# PJ import
from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid
from imprcm_uuid_server.encoder import JSONEncoder
from imprcm_uuid_server.test import BaseTestCase


class TestAddNewItemWithUuidController(BaseTestCase):
    """AddNewItemWithUuidController integration test stubs"""

    def test_id_server_uuids_uuid_put(self):
        # generate a valid new item

         # New item details
        item_entity_ok = uuid.uuid4()  # should be a legal UUID
        item_entity_wrong = '23x-30450-30020' # this is not a UUID

        item_scheme_url_ok = 'evn' # this one works - included in setup
        item_scheme_url_wrong = 'evan' # this one doesnt

        item_fromtimestamp_ok = '2019-03-12T00:01:02Z'
        item_fromtimestamp_not3339 = '20190312 00:01:02' # not RFC3339 compliant

        item_totimestamp_1 = None
        item_totimestamp_2 = '2019-03-16' # compliant
        item_totimestamp_3 = '20190316'   # not compliant

        item_name_url = '70047010200'
        item_name = 'Loco 47 102 / EVN 70047010200'

        # group up to list of tuples for subtests
        cases = [
            {'uuid': item_entity_ok,
             'scheme': item_scheme_url_ok,
             'name_url': item_name_url,
             'fts': item_fromtimestamp_ok,
             'tts': item_totimestamp_1,
             'resp': 201,
             'desc': '1 - create new item',
             'status': 'OK'
             },     # good create case
            {'uuid': item_entity_ok,
             'scheme': item_scheme_url_ok,
             'name_url': item_name_url,
             'fts': item_fromtimestamp_ok,
             'tts': item_totimestamp_2,
             'resp': 200, 
             'desc': '2 - update end date',
             'status': 'OK'
             },     # good update case
            {'uuid': item_entity_ok,
             'scheme': item_scheme_url_wrong,
             'name_url': item_name_url,
             'fts': item_fromtimestamp_ok,
             'tts': item_totimestamp_2,
             'resp': 400, 
             'desc': '3 - bad scheme',
             'status': 'Error',
             'message': 'scheme "' + item_scheme_url_wrong + '" not known'
            },     # missing scheme
            {'uuid': item_entity_wrong,
             'scheme': item_scheme_url_ok,
             'name_url': item_name_url,
             'fts': item_fromtimestamp_ok,
             'tts': item_totimestamp_1,
             'resp': 400, 
             'desc': '4 - bad uuid',
             'status': 'Error',  # no message in this one because 
            },     # malformed uuid
            {'uuid': uuid.uuid4(),  # new uuid different from 1-3
             'scheme': item_scheme_url_ok,
             'name_url': item_name_url + '1',
             'fts': item_fromtimestamp_not3339,
             'tts': item_totimestamp_1,
             'resp': 400, 
             'desc': '5 - bad fromtimestamp',
             'status': 'Error',
             'message': 'fromtimestamp "' + item_fromtimestamp_not3339 + '" is not in RFC3339 format'
            },     # malformed timestamp
            {'uuid': uuid.uuid4(),  # new uuid different from 1-3
             'scheme': item_scheme_url_ok,
             'name_url': item_name_url + '2',
             'fts': item_fromtimestamp_ok,
             'tts': item_totimestamp_3,
             'resp': 400, 
             'desc': '6 - bad totimestamp',
             'status': 'Error',
             'message': 'totimestamp "' + item_totimestamp_3 + '" is not in RFC3339 format'
            },     # malformed timestamp
        ]

        # run through the cases as subTests
        for case in cases:
            with self.subTest(case['desc']):
                new_item = EntitySchemaWithUuid(
                    uuid = case['uuid'],
                    entity_detail = EntitySchemaNoUuid(
                        name_url=case['name_url'],
                        scheme_url=case['scheme'],
                        fromtimestamp=case['fts'],
                        totimestamp=case['tts'],
                ))

                response = self.client.open(
                    '/id-server/entities/{scheme_url}/{name_url}/{fromtimestamp}/{uuid}'.format(
                        scheme_url=case['scheme'], 
                        name_url=case['name_url'], 
                        fromtimestamp=case['fts'],
                        uuid=case['uuid']
                        ),
                    method='PUT',
                    data=json.dumps(new_item),
                    content_type='application/json')

                resp = json.loads(response.data.decode('utf-8'))
                # print(resp_body)
                # check the response code
                self.assertStatus(response, case['resp'],
                               'Response body is : ' + str(resp))
                
                # check the response body contains the right information
                if case['status'] == 'OK': 
                    resp_body = resp['entity_object']
                    resp_uri = '/'.join(resp['entity_uri'].split('/')[-3:]) # just the end of the route

                    self.assertEqual(resp_body['uuid'], str(new_item.uuid))
                    self.assertEqual(resp_body['entity_detail']['name_url'], str(new_item.entity_detail.name_url))
                    self.assertEqual(resp_body['entity_detail']['fromtimestamp'], str(new_item.entity_detail.fromtimestamp))
                    self.assertEqual(resp_body['entity_detail']['scheme_url'], str(new_item.entity_detail.scheme_url))

                    # TODO - refactor this pattern - it's going to happen all over the place
                    if new_item.entity_detail.totimestamp == None:
                        self.assertRaises(KeyError, lambda: resp_body['entity_detail']['totimestamp'])
                    else:
                        self.assertEqual(resp_body['entity_detail']['totimestamp'], str(new_item.entity_detail.totimestamp))

                    # todo - refactor: get the path from somewhere
                    self.assertEqual(resp_uri, 'id-server/entities_by_uuid/{0}'.format(new_item.uuid))

                if case['status'] == 'Error':
                    # check that the response contains all the right keys
                    # i.e. set(list) is a subset of set(keys)
                    # TODO - refactor so this list is a constant somewhere central
                    self.assertTrue(set(('detail', 'title', 'type', 'status')).issubset(set(resp.keys())))

                    # check that the right error message is there
                    if('message') in case.keys():
                        self.assertEqual(resp['detail'], case['message'])
                
 
if __name__ == '__main__':
    import unittest
    unittest.main()
