   .. _imprcm-requirements: 

IMPRCM Requirements - Additional
=================================

These are the additional requirements created as part of the IMPRCM work, where gaps were found. These form part of the full set of IMPRCM :ref:`requirements`.



.. table:: IMPRCM Requirements: Additional
   :class: table-hover
   :name: tab_requirements_additional
   :widths: 1 2 3 1  

   
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Category             |Title                                            |Description                                                                                           |IMPRCM Reference|
   +=====================+=================================================+======================================================================================================+================+
   |Broker operation     |File is returned in required format              |Broker returns requested data in a file format defined in request                                     |131             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Broker operation     |Scheduled outputs                                |Broker can provide scheduled  outputs                                                                 |132             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Broker operation     |Data is returned in required format              |Broker returns a data item in a format defined in query process or in architecture                    |146             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Broker operation     |Webservice request to broker                     |Broker can receive a request for data via webservice                                                  |150             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Broker operation     |User request to broker                           |Broker can receive a request for data via user                                                        |151             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Broker operation     |Broker can process data                          |Broker can collate, filter or apply other standard processing services                                |153             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Event Data           |Events have at least one time or sequence data   |Events being input have at least one time or sequence data                                            |120             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Metadata             |Engineering and scaling metadata conforms to UCUM| Engineering and scaling metadata in UCUM format is supported                                         |122             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Ref Data             |Asset composition can be drilled up              |Asset composition can be drilled  up ie explore the hierarchy above an asset.                         |139             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Ref Data             |Asset composition can be drilled down            |Asset composition can be drilled  up ie explore the hierarchy below an asset.                         |140             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Interchange Standards|RailML                                           |Data is in alignment with RailML                                                                      |133             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Datagram header is mandatory                     |Header is mandatory element of datagram and its presence is enforced                                  |124             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Datagram body is optional                        |Body is optional element of datagram and its presence is supported                                    |125             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Header must have a timestamp                     |Broker enforces that datagram header must have timestamp                                              |126             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Header must have source identification           |Broker enforces that datagram header must have source identification                                  |127             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Asset sensor identification is mandatory         |If datagram body is present then asset sensor identification is mandatory                             |128             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |All data interchange conforms to common schema   |All data interchange shall  conform to a common schema                                                |164             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Schema describes entire domain                   |The common schema shall describe all relevant data about all relevant entities in the prototype domain|165             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Schemas              |Specify response to missing input data           |User can specify broker response to missing input data                                                |182             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
   |Security             |Access is by key / secret                        |Access to the broker is restricted to authorised users with a key / secret                            |181             |
   +---------------------+-------------------------------------------------+------------------------------------------------------------------------------------------------------+----------------+
