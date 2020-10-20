# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from imprcm_uuid_server.models.base_model_ import Model
from imprcm_uuid_server.models.entity_schema_with_uri import EntitySchemaWithUri  # noqa: F401,E501
from imprcm_uuid_server import util


class EntitySchemaUrlArray(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self):  # noqa: E501
        """EntitySchemaUrlArray - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'EntitySchemaUrlArray':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The entity_schema_url_array of this EntitySchemaUrlArray.  # noqa: E501
        :rtype: EntitySchemaUrlArray
        """
        return util.deserialize_model(dikt, cls)
