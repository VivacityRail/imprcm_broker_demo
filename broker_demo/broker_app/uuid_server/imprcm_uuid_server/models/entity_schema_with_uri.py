# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from imprcm_uuid_server.models.base_model_ import Model
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: F401,E501
from imprcm_uuid_server.models.uri import Uri  # noqa: F401,E501
from imprcm_uuid_server import util


class EntitySchemaWithUri(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, entity_uri: Uri=None, entity_object: EntitySchemaWithUuid=None):  # noqa: E501
        """EntitySchemaWithUri - a model defined in Swagger

        :param entity_uri: The entity_uri of this EntitySchemaWithUri.  # noqa: E501
        :type entity_uri: Uri
        :param entity_object: The entity_object of this EntitySchemaWithUri.  # noqa: E501
        :type entity_object: EntitySchemaWithUuid
        """
        self.swagger_types = {
            'entity_uri': Uri,
            'entity_object': EntitySchemaWithUuid
        }

        self.attribute_map = {
            'entity_uri': 'entity_uri',
            'entity_object': 'entity_object'
        }

        self._entity_uri = entity_uri
        self._entity_object = entity_object

    @classmethod
    def from_dict(cls, dikt) -> 'EntitySchemaWithUri':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The entity_schema_with_uri of this EntitySchemaWithUri.  # noqa: E501
        :rtype: EntitySchemaWithUri
        """
        return util.deserialize_model(dikt, cls)

    @property
    def entity_uri(self) -> Uri:
        """Gets the entity_uri of this EntitySchemaWithUri.


        :return: The entity_uri of this EntitySchemaWithUri.
        :rtype: Uri
        """
        return self._entity_uri

    @entity_uri.setter
    def entity_uri(self, entity_uri: Uri):
        """Sets the entity_uri of this EntitySchemaWithUri.


        :param entity_uri: The entity_uri of this EntitySchemaWithUri.
        :type entity_uri: Uri
        """

        self._entity_uri = entity_uri

    @property
    def entity_object(self) -> EntitySchemaWithUuid:
        """Gets the entity_object of this EntitySchemaWithUri.


        :return: The entity_object of this EntitySchemaWithUri.
        :rtype: EntitySchemaWithUuid
        """
        return self._entity_object

    @entity_object.setter
    def entity_object(self, entity_object: EntitySchemaWithUuid):
        """Sets the entity_object of this EntitySchemaWithUri.


        :param entity_object: The entity_object of this EntitySchemaWithUri.
        :type entity_object: EntitySchemaWithUuid
        """

        self._entity_object = entity_object
