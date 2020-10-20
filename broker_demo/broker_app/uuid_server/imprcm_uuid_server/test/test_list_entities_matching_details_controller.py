# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from imprcm_uuid_server.models.entity_schema_url_array import EntitySchemaUrlArray  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: E501
from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid  # noqa: E501
from imprcm_uuid_server.test import BaseTestCase
from imprcm_uuid_server import db

import uuid

# basic test data
TEST_UUID_1 = str(uuid.uuid4())
TEST_NAMES_1 =  EntitySchemaWithUuid(
        uuid=TEST_UUID_1,
        entity_detail=EntitySchemaNoUuid(
            name_url='70040001000',
            scheme_url='evn',
            fromtimestamp='2019-03-24T12:00:00Z',
            totimestamp= '2019-04-25'
            )
        )

class TestListEntitiesMatchingDetailsController(BaseTestCase):
    """ListEntitiesMatchingDetailsController integration test stubs"""

    def setUp(self):
        super(TestListEntitiesMatchingDetailsController, self).setUp()
        # populate some data to test with
        with self.test_app.app.app_context():
            # item with 1 name
            entity = db.Entity(uuid = TEST_UUID_1)
            db.the_db.session.add(entity)
            entityname = db.EntityName(
                entity_id = TEST_NAMES_1.uuid,
                scheme_id = TEST_NAMES_1.entity_detail.scheme_url,
                fromtimestamp = TEST_NAMES_1.entity_detail.fromtimestamp,
                totimestamp = TEST_NAMES_1.entity_detail.totimestamp,
                name_url = TEST_NAMES_1.entity_detail.name_url,
                name = TEST_NAMES_1.entity_detail.name_url
                )
            db.the_db.session.add(entityname)
            db.the_db.session.commit()


    def test_id_server_entities_get(self):
        """Test case for id_server_entities_get

        get the uuids for a matching set of details
        """
        query_string = [('entity', '70040001000'),
                        ('schema', 'evn'),
                        ('fromdate', '2019-04-25')]
        response = self.client.open(
            '/id-server/entities',
            method='GET',
            query_string=query_string)
        #print(response.data.decode('utf-8'))
        self.assertStatus(response, 200,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
