.. .. cssclass:: imprcm-wip

.. heading sequence */* = - ^ "


.. _information-framework:

*************************
Information Framework
*************************

Introduction
=============

.. figure:: https://www.lucidchart.com/publicSegments/view/7aeee2e7-c1ed-4465-9060-f411f9094304/image.png
  :alt: Frameworks overview
  :name: if_frameworks_overview

  Cross-industry RCM Project Framework Documents - Overview


The Information Framework defines the data requirements of the scheme in *business* terms - i.e. what is needed for the scheme to satisfy its business needs.

:numref:`if_frameworks_overview` shows how the Information Framework fits in with the other framework documentation:

- it is a key output of the :ref:`act-as-sponsor-for-an-xircm-scheme` and :ref:`set-up-technical-aspects-of-an-xircm-scheme` workstreams in the  :ref:`phase-investigation` and :ref:`phase-definition` of the scheme, in which the business need of the scheme is defined. 

- it sets out the *"what"* element of the information flows. The *"how"* element is then specified by the :ref:`technical-framework` and :ref:`operational-framework` and the schedules in the contract dealing with scope and service level agreements.

The :term:`T1010` documentation provides guidance on aspects of the Information Framework:

- it recommends some :ref:`guiding principles <intro-key-concepts>` for cross-industry data interchange to simplify and clarify legal and technical issues and improve re-usability of the data.
- The T1010-02 business process maps specify the content of the document and refer to the :term:`ISO 13374` data / processing model and maturity levels. [#]_
- The T1010-01 data architecture has requirements and recommendations about relevant data standards, data item formats, transfer methods, identification and keying, metadata and governance. [#]_

Relevant parts of that guidance are included in :ref:`tech-guidance-if`.  

Also included in the guidance are tips which reflect lessons learned during the development of the prototype data interchange via broker in :ref:`intro-IMPRCM`. 

The framework should have sections that cover the following aspects:

- :ref:`info-fw-data-items`: the data items required by the business process change supported by the scheme
- :ref:`info-fw-data-characteristics`: the important data availability and quality characteristics of the data
- :ref:`info-fw-data-volumes`: a consideration of the amount of data needed by the scheme, in terms of storage volume and transmission / processing bandwidth
- :ref:`info-fw-pipeline`: the processing steps to be carried out on the data to make it useful to the business process
- :ref:`info-fw-ip`: considerations of data ownership, licensing, intellectual propertya and permitted use.




.. _info-fw-data-items:

Data Items
===========

The Information Framework needs to define the data items to be included in the data flow.  This should be done in the form of a :term:`schema` listing the data items and defining for each one:

- **name** - the name of the data item. This should conform to a naming convention which makes the name usable in as many contexts as possible. Guidance: :ref:`if-naming`.  
- **title** - a descriptive title of the data item. This is a short phrase defining what the data item is. 
- **description** - a lengthier description of the data item containing contextual information such as source and meaning.
- **data type** - the type of the data item: numeric, string, date/time etc.  Should be defined as specifically as possible. Guidance: :ref:`if-data-types`.
- **format** - the format of the data item. Particularly important for items such as dates / times / geographical positions / track positions where standardisation is useful. Guidance: :ref:`if-formats`.
- **size** - the size of the data item in characters or bytes (if relevant). This is important for correct handling of textual ("string") data and for the calculation of data volumes (see :ref:`info-fw-data-volumes`). Guidance: :ref:`if-formats`.
- **unit of measure** - the engineering units in which the data item is measured. Should be :term:`SI` units where available, otherwise recognised rail industry standard units.  Guidance: :ref:`if-eng-units`.
- **uniqueness** - is the value of the data item unique - is it an identifier of, e.g. an asset?.  Guidance: :ref:`if-unique`.
- **mandatory/optional** - must the data item always be present.  Guidance: :ref:`if-unique`.
- **grain** - the level of detail of the data item. This typically relates to how frequently it is captured, or whether it appears at the level of "header" or "detail". This impacts the data volumes and storage - see :ref:`info-fw-data-volumes`; guidance: :ref:`if-grain`.
- **reference** - source or reference for the data item - such as any parent or shared schema that it belongs to.
- **notes** - any further notes or guidance to help providers or users of the data item.

The data items will fall into groups:

- the :term:`RCM` **metrics** being gathered or results of data processing
- identifiers of the **measuring equipment or processing agent** responsible for the data
- identifiers of the **asset being monitored**
- **time / date stamps** for the capture and processing of the data
- **contextual** data, for example about the measuring equipment, the surroundings, the train being operated etc
- **metadata** about the data and processing: file names, calibration data, ownership / licensing information, data quality indicators.
- **non-standard** data that may be added by equipment vendors or software suppliers.

It is important to identify which of the groups of data are required to meet the business goal. Most data flows will contain all the data groups. 

It is likely that some of the groups will be common across different data flows and there may have been a schema already defined for them and shared. In this case the shared schema should be used as a starting point.

The T1010-01 data architecture mandates some aspects of the data content: these are discussed in :ref:`if-guide-data-items` in the Guidance.


.. _info-fw-data-characteristics:

Data Flow Characteristics
==========================

To fulfil the goals of the scheme, the data flow will need to behave appropriately. The Information Framework should define what characteristics the flow should have. These include:

- **accuracy** - how close the readings or positions are to actual truth, within the stated precision
- **precision** - how precisely readings or positions are measured - e.g. 1 part per 1000, or to the nearest millisecond, or to the nearest 10cm
- **completeness** - how complete the data set needs to be; how tolerant the business process is of missing data; whether a complete record is needed or only the most recent reading(s)
- **consistency** - how well different aspects of the data stream agree with each other; whether the business process will tolerate repeated data or conflicting readings from different sensors
- **timeliness** - how up-to-date the data needs to be; how well the business process will tolerate data that arrives late; what sort of propagation time is acceptable from measurement of an event to the data about it being available
- **availability** - whether the data flow needs to occur 24 x 7 all days; how tolerant the business process is of an absence of data for a given number of minutes or hours per day or month
- **integrity** - how important it is to the business process that the data is not corrupted or observed en route
- **security** - how important it is that only authorised parties see the data or gain access to the equipment and processing steps involved in the data flow
- **openness** - how important it is that the data stream uses open standards and commonly-used formats
- **conditions of use** - what restrictions on the use of the data can be tolerated, directly or indirectly.

The T1010 commercial principles and data architecture mandate some of these characteristics: see :ref:`if-data-char-t1010-reqs` in the Guidance.

The more thought is put into defining these characteristics in the Information Framework, the more likely the technical solution addressed in the :ref:`technical-framework` will be correct.

.. _info-fw-data-volumes:

Data Volumes
=============

Data need to be stored after collection, during processing and for analysis purposes in most schemes. The type and size of data storage can have a large impact on the complexity and cost of the solution.

Two aspects of data volume need to be considered:

- **data in motion**: what is the rate of data generation / transmission? This governs bandwidth and processing capabilities of the solution.
- **data at rest**: how long does the data need to be stored for, at what level of detail? This governs data storage volume.

Detailed calculation of the sizing is a matter for the :ref:`technical-framework` (see :ref:`tf-sizing`), but the inputs to that calculation are business-driven. These include:

- the raw rate of data generation by the scheme's sensors. This may be measured in data points per second, per event or per metre of distance covered
- the number of data items in each data record
- the steps in the processing pipeline (see :ref:`info-fw-pipeline`). Each step may need input, internal and output data stores; and may result in significant changes to data rates - whether reducing them by e.g. summarising or feature detection; or increasing them by adding contextual or calculated information.
- the length of time data needs to be stored for. This may be for the immediate needs of the scheme; it may also be for later analysis of historic data or to make the data available for other purposes.
- how many copies of the data need to be kept - say for backup or disaster recovery purposes.

.. _info-fw-pipeline:

Data Processing Pipeline
==========================


Overview 
--------

The Information Framework needs to define any processing steps needed to transform the data from its initial state to the form required by the scheme.  Each such step needs the following to be considered:

- the :term:`RCM` data coming in to the step: items, formats, volume, timing. This consistutes a data interface: see :ref:`info-fw-pl-interfaces`.
- any contextual data required by the step to help it do its work: reference data, other data streams
- the processing being done by the step (see :ref:`info-fw-pl-steps`)
- the performance requirements of the step: how quickly does it need to run; how often; how much data can be batched up.
- the data coming out of the step. Again, an interface: :ref:`info-fw-pl-interfaces`.

T1010 recommends that pipelines are built in accordance with the principles set out in :term:`ISO 13374`. This defines levels of processing (also referred to as "maturity levels" and a clear distinction between these and the data flows between them). See the guidance in :ref:`if-pipeline-t1010-reqs`.


.. _info-fw-pl-steps:

Processing steps
---------------------

Any pipeline will have some processing steps which are standard and may be shared by other similar pipelines; and some which are specific to their own application.

Steps which may be done in a standard way include:

- outlier detection and removal
- calibration (scaling of sensor or location data to correct for incorrect or drifting readings)
- quality identification (detection of invalid data due to e.g. sensor error or missing values) 
- location referencing (establishing a track position from a geographical one)
- asset identification (including providing context data such as route section, train id etc)
- feature extraction (identifying events of interest from an othewise unremarkable data stream)
- aggregation (calculation of summaries such as averages, totals, standard deviations, exceedence counts)

Where the steps are standard, a module or algorithm may already be available and should be used in preference to creating a new one.

In a general case, different parties may be involved in carrying out different processing steps. This implies a possible need for a commercial / legal arrangement and a service level agreement with these parties: these should be included in the stakeholder matrix as described in :ref:`sponsor-scope`.

The provider of a processing stem may retain :term:`IP` rights in the algorithms or processes used. 


.. _info-fw-pl-interfaces:

Interfaces
-------------

T1010 requires that the interfaces into and out of processing steps are clearly documented and the data flows use standard data formats and interface methods. This is to ensure that the data travelling between steps is potentially accessible to other data users or for novel purposes; and to open the possibility of different algorithms, perhaps from different suppliers, to be used.

See the guidance in :ref:`if-pipeline-t1010-reqs`.


.. _info-fw-ip:

Ownership, IP, Liability
========================

The Information Framework needs to make clear who owns data and :term:`IP` at each stage in the data lifecycle; and where responsibility lies for the provision of data and conformance to any expected quality characteristics or for decisions taken based on the data. This information is fed into the commercial terms for each agreement between parties.

T1010 has principles and guidance in this area, introduced in brief in :ref:`intro-key-concepts` and detailed in the guidance: :ref:`if-ip-t1010-reqs`.


.. rubric:: Footnotes

.. [#] Source: `T1010-02 Process Map - C <_static/T1010/T1010-02/Appendix_C2_RCM_process_map.pdf#page=4>`_

.. [#] Source: `T1010-01 Data Architecture Requirements <_static/T1010/T1010-01/2015-03-report-t1010-RCM-architecture-requirements.pdf>`_



Linked pages
===============

.. toctree::
  technical_guidance
