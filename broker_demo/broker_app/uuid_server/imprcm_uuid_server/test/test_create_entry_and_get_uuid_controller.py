# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: E501
from imprcm_uuid_server.test import BaseTestCase


class TestCreateEntryAndGetUuidController(BaseTestCase):
    """CreateEntryAndGetUuidController integration test stubs"""

    def test_id_server_entities_post(self):
        """Test case for id_server_entities_post

        add details of an entry and get its uuid
        """
        cases = [
            {'scheme': "evn",
             'name_url': "3500129934",
             'fts': '2019-03-09T11:23:00Z',
             'tts': None,
             'resp': 201,
             'desc': '1 - create new item',
             'status': 'OK'
             },     # good create case
            {'scheme': "evn",
             'name_url': "3500129934",
             'fts': '2019-03-09T11:23:00Z',
             'tts': None,
             'resp': 400,
             'desc': '2 - try to add existing item',
             'status': 'Error',
             'message': 'item already exists with uuid'
             },     # item already exists
        ]

        # run through the cases as subTests
        for case in cases:
            with self.subTest(case['desc']):
                new_item = EntitySchemaNoUuid(
                    name_url=case['name_url'],
                    scheme_url=case['scheme'],
                    fromtimestamp=case['fts'],
                    totimestamp=case['tts'],
                )

                response = self.client.open(
                    '/id-server/entities',
                    method='POST',
                    data=json.dumps(new_item),
                    content_type='application/json')

                self.assertStatus(response, case['resp'],
                               'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
