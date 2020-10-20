# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from imprcm_uuid_server.models.entity_schema_array import EntitySchemaArray  # noqa: E501
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: F401,E501
from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid

from imprcm_uuid_server.test import BaseTestCase
from imprcm_uuid_server import db
import uuid

TEST_UUID_1 = str(uuid.uuid4())
TEST_NAMES_1 =  EntitySchemaWithUuid(
        uuid=TEST_UUID_1,
        entity_detail=EntitySchemaNoUuid(
            name_url='70040001000',
            scheme_url='evn',
            fromtimestamp='20190324T12:00:00Z'  
            )
        )

TEST_UUID_2 = str(uuid.uuid4())
TEST_NAMES_2a =  EntitySchemaWithUuid(
        uuid=TEST_UUID_2,
        entity_detail=EntitySchemaNoUuid(
            name_url='70040001030',
            scheme_url='evn',
            fromtimestamp='20190324T12:00:00Z'  
            )
        )
TEST_NAMES_2b =  EntitySchemaWithUuid(
        uuid=TEST_UUID_2,
        entity_detail=EntitySchemaNoUuid(
            name_url='70040001045',
            scheme_url='evn',
            fromtimestamp='20210324T00:00:00Z'  
            )
        )




class TestGetDetailsForUuidController(BaseTestCase):
    """GetDetailsForUuidController integration test stubs"""

    def setUp(self):
        super(TestGetDetailsForUuidController, self).setUp()
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

            # entity with 2 names
            entity = db.Entity(uuid = TEST_UUID_2)
            db.the_db.session.add(entity)
            entityname = db.EntityName(
                entity_id = TEST_NAMES_2a.uuid,
                scheme_id = TEST_NAMES_2a.entity_detail.scheme_url,
                fromtimestamp = TEST_NAMES_2a.entity_detail.fromtimestamp,
                totimestamp = TEST_NAMES_2a.entity_detail.totimestamp,
                name_url = TEST_NAMES_2a.entity_detail.name_url,
                name = TEST_NAMES_2a.entity_detail.name_url
                )
            db.the_db.session.add(entityname)
            entityname = db.EntityName(
                entity_id = TEST_NAMES_2b.uuid,
                scheme_id = TEST_NAMES_2b.entity_detail.scheme_url,
                fromtimestamp = TEST_NAMES_2b.entity_detail.fromtimestamp,
                totimestamp = TEST_NAMES_2b.entity_detail.totimestamp,
                name_url = TEST_NAMES_2b.entity_detail.name_url,
                name = TEST_NAMES_2b.entity_detail.name_url
                )
            db.the_db.session.add(entityname)
            db.the_db.session.commit()
            # print(db.the_db.session.query(db.EntityName).all())


    def test_id_server_uuids_uuid_get(self):
        """Test case for id_server_uuids_uuid_get

        get the details for a UUID
        """
        response = self.client.open(
            '/id-server/entities_by_uuid/{uuid}'.format(uuid=TEST_UUID_2),
            method='GET')
        print(response.data.decode('utf-8'))
        self.assertStatus(response, 200,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
