from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 
from imprcm_uuid_server.models.entity_schema_with_uuid import EntitySchemaWithUuid  # noqa: E501
from imprcm_uuid_server.models.entity_schema_no_uuid import EntitySchemaNoUuid  # noqa: E501
import re
from datetime import datetime
import uuid

# db layer for API
# has classes for the 3 tables, plus relationships between them
# also has functions to reflect the API operations: 
#  get(uuid) returns matching items
#  get(name [, scheme]) returns uuid
#  put(entity, scheme, date, uuid) returns link
#  post(entity, scheme, data) returns item with uuid and link



the_db = SQLAlchemy()

def setup_app_db(flask_app, db_url):  # the 
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    the_db.init_app(flask_app)
    print('db initialised: {0}'.format(db_url))

#  the database layer classes
class Scheme(the_db.Model):
    # naming schemes for things - e.g. European Vehicle Numbers or ELR/Track IDs
    __tablename__ = 'schemes'
    scheme_url = the_db.Column(the_db.String(80), primary_key=True)
    scheme_name = the_db.Column(the_db.String(80), nullable=False)

    def __repr__(self):
        return '<Scheme {0!r} name {1!r}>'.format(self.scheme_url, self.scheme_name)


class Entity(the_db.Model):
    # entities - uuids defining unique items.  Each may have several names in different schemes
    __tablename__ = 'entities'
    uuid = the_db.Column(the_db.String(36), primary_key=True)

    def __repr__(self):
        return '<Entity with uuid: {0!r}>'.format(self.uuid)


class EntityName(the_db.Model):
    # table for the linkage. Each uuid item can have one name at a time in each naming scheme.
    __tablename__ = 'entity_names'
    entity_id = the_db.Column(the_db.String(36), the_db.ForeignKey('entities.uuid'), primary_key=True)
    scheme_id = the_db.Column(the_db.String(80), the_db.ForeignKey('schemes.scheme_url'), primary_key=True)
    fromtimestamp = the_db.Column(the_db.String(25), nullable=False, primary_key=True)
    name_url = the_db.Column(the_db.String(80), nullable=False)
    name = the_db.Column(the_db.String(80), nullable=False)
    totimestamp = the_db.Column(the_db.String(25))

    def __repr__(self):
        return '<EntityName uuid: {0!r} Scheme: {1!r} Name: {2!r} Fromtimestamp: {3!r}>'.format(self.entity_id, self.scheme_id, self.name_url, self.fromtimestamp)


def raise_error(detail, type='about:blank'):
    # build an error detail dict per RFC 7807
    return {'detail': detail, 'type': type}

# validation for timestamps

# regex from https://gist.github.com/marcelotmelo/b67f58a08bee6c2468f8, amended so years must have 4 digits and must be UTC = Z or +/- 00:00. named groups ts, fs, tz added
RFC3339_REGEX = '^(?P<ts>(?P<dp>([0-9]{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]))(?P<tp>[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(?P<fs>\.[0-9]+)?)?)(?P<tz>([Zz])|([\+|\-])(00:00))?$'
re_rfc_3339 = re.compile(RFC3339_REGEX)

def isValidTimestamp(timestamp):
    # formatted ok?
    match_ts = re_rfc_3339.fullmatch(timestamp)
    is_ok = bool(match_ts)
    if is_ok:
        # valid date_time? Strip the timezone bit first
        ts = match_ts.groupdict()['ts']
        #print(match_ts.groupdict())
        #print(ts)
        try:
            if match_ts.groupdict()['tp']: # it has a time part
                if match_ts.groupdict()['fs']:
                    datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f') # has fractional seconds
                else:
                    datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S') # no fractional seconds
            else:
                datetime.strptime(ts, '%Y-%m-%d') # no time part

        except ValueError:
           is_ok = False

    return is_ok


# database operation handlers
def put_item_with_uuid_as_json(scheme_url, name_url, fromtimestamp, uuid_url, new_entity_with_uuid):

    # PUT an item specified by scheme / name / date / uuid
    '''
    PUT a new item
    the logic goes: 
        if uuid exists
            does entry exist for scheme / date
            if so
                update the name / scheme / date entry
                status = update
            else
                does the scheme exist
                if not
                    error - unknown naming scheme
                    status = error
                if so
                    create new entry 
                    status = new
        else
            does the scheme exist
            if so
                create new entry
                status = new
            if not
                error - unknown naming scheme
                status = error
    '''
    error = {}
    # is the fromtimestamp valid RFC3339
    if not isValidTimestamp(fromtimestamp):
        return None, 'invalid', raise_error(detail='fromtimestamp "{}" is not in RFC3339 format'.format(fromtimestamp)) 

    # is the totimestamp valid
    if new_entity_with_uuid.entity_detail.totimestamp:    
        if not isValidTimestamp(new_entity_with_uuid.entity_detail.totimestamp):
            return None, 'invalid', raise_error(detail='totimestamp "{}" is not in RFC3339 format'.format(new_entity_with_uuid.entity_detail.totimestamp)) 

    # does the naming scheme exist
    scheme = Scheme.query.filter_by(scheme_url=scheme_url).first()
    if scheme is None:
        # badly-formed request
        # print('no scheme')
        return None, 'invalid', raise_error(detail='scheme "{}" not known'.format(scheme_url)) 

    # has the uuid been encountered before
    the_entity = Entity.query.filter_by(uuid=uuid_url).first()
    if the_entity is None:
        # new entry. Create Entity and EntityName records and the relationship between them
        entity = Entity(uuid=uuid_url)
        the_db.session.add(entity)
        entity_name = EntityName(
            entity_id = uuid_url,
            scheme_id = scheme_url,
            fromtimestamp = fromtimestamp,
            name_url = name_url,
            name = name_url,
            #name = new_entity_with_uuid.entity_detail.entity,
            totimestamp = new_entity_with_uuid.entity_detail.totimestamp
            )
        the_db.session.add(entity_name)
        the_db.session.commit()
        #return_entity = EntitySchemaWithUuid(uuid=uuid_url, EntitySchemaNoUuid(entity=))
        return uuid_url, 'new', {}
    else:
        # existing uuid - check to see if we have an existing name entry
        entity_name = EntityName.query.filter_by(entity_id=uuid_url, scheme_id=scheme_url, fromtimestamp=fromtimestamp).first()
        if entity_name is None:
            # new entry
            entity_name = EntityName(
                entity_id = uuid_url,
                scheme_id = scheme_url,
                fromtimestamp = fromtimestamp,
                name_url = name_url,
                name = name_url,
                #name = new_entity_with_uuid.entity_detail.entity,
                totimestamp = new_entity_with_uuid.entity_detail.totimestamp
                #totimestamp = totimestamp
                )
            the_db.session.add(entity_name)
            the_db.session.commit()
            return the_entity.uuid, 'new', {}
        else:
            # existing entry - update it. At the moment this is trivial but may not be in future
            # entity_name()
            entity_name.name_url = name_url
            #entity_name.name = new_entity_with_uuid.entity_detail.entity
            entity_name.totimestamp = new_entity_with_uuid.entity_detail.totimestamp
            the_db.session.commit()
            return the_entity.uuid, 'update', {}
    
    return None, 'invalid', error
    

def post_item_as_json(new_entity):
    # POST a new entity and return its uuid
    # - if an item matching the provided details already exists, return it
    # - otherwise create the new item with a new uuid and return it
    # returns uuid, status, item, error

    # extract the data items from the incoming entity
    name_url = new_entity.name_url
    scheme_url = new_entity.scheme_url
    fromtimestamp = new_entity.fromtimestamp
    totimestamp = new_entity.totimestamp

    # the_uuid = uuid.uuid4()

    # check the parameters
    # is the fromtimestamp valid RFC3339
    if not isValidTimestamp(fromtimestamp):
        return None, 'invalid', {}, raise_error(detail='fromtimestamp "{}" is not in RFC3339 format'.format(fromtimestamp)) 

    # is the totimestamp valid
    if totimestamp:    
        if not isValidTimestamp(totimestamp):
            return None, 'invalid', {}, raise_error(detail='totimestamp "{}" is not in RFC3339 format'.format(totimestamp)) 

    # does the naming scheme exist
    scheme = Scheme.query.filter_by(scheme_url=scheme_url).first()
    if scheme is None:
        # badly-formed request
        # print('no scheme')
        return None, 'invalid', {}, raise_error(detail='scheme "{}" not known'.format(scheme_url)) 

    # does the item exist
    the_entity_name = EntityName.query.filter_by(scheme_id = scheme_url, fromtimestamp = fromtimestamp, name_url = name_url).first()
    if the_entity_name:
        return the_entity_name.entity_id, 'invalid', EntitySchemaWithUuid(
            uuid=the_entity_name.entity_id,
            entity_detail = EntitySchemaNoUuid(
                name_url = the_entity_name.name_url,
                scheme_url = the_entity_name.scheme_id,
                fromtimestamp = the_entity_name.fromtimestamp,
                totimestamp = the_entity_name.totimestamp
                )
            ), raise_error(detail='item already exists with uuid {}'.format(the_entity_name.entity_id)) 

    # create the new item
    the_uuid = uuid.uuid4()
    entity = Entity(uuid=str(the_uuid))
    the_db.session.add(entity)
    the_entity_name = EntityName(
        entity_id = str(the_uuid),
        scheme_id = scheme_url,
        fromtimestamp = fromtimestamp,
        name_url = name_url,
        name = name_url,
        #name = new_entity_with_uuid.entity_detail.entity,
        totimestamp = totimestamp
        )
    the_db.session.add(the_entity_name)
    the_db.session.commit()
    return the_entity_name.entity_id, 'new', EntitySchemaWithUuid(
        uuid=the_entity_name.entity_id,
        entity_detail = EntitySchemaNoUuid(
            name_url = the_entity_name.name_url,
            scheme_url = the_entity_name.scheme_id,
            fromtimestamp = the_entity_name.fromtimestamp,
            totimestamp = the_entity_name.totimestamp
            )
        ), {}

def get_item_by_uuid_as_json(the_uuid):
    # returns a list of entries matching the given uuid, status, error
    #return {}, 'not implemented', raise_error('GET by uuid not yet implemented')

    # query the entitynames that share the provided uuid
    results = EntityName.query.filter_by(entity_id=the_uuid).all()
    return_list = []
    if results:
        # convert results into list of EntitySchemaWithUUID:
        for result in results:
            return_list.append(EntitySchemaWithUuid(
                uuid=the_uuid,
                entity_detail = EntitySchemaNoUuid(
                    name_url = result.name_url,
                    scheme_url = result.scheme_id,
                    fromtimestamp = result.fromtimestamp,
                    totimestamp = result.totimestamp
                    )
                ))

        # print(return_list)
        return return_list, 'data', {}
    else:
        return {}, 'no data', raise_error('No data for entity with uuid {}'.format(the_uuid))


def get_matching_details_as_json(scheme_url, name_url, effective_timestamp):
    #return {}, 'not implemented', raise_error('GET uuid for details not yet implemented')

    # return a list of entitynames that meet the provided criteria
    # noting that scheme and timestamp may be null, but name should not be

    if not name_url:
        return {}, 'invalid', raise_error('query must at least specify an entity name')

    the_query = the_db.session.query(EntityName).filter_by(name_url=name_url)
    if scheme_url:
        the_query = the_query.filter_by(scheme_id=scheme_url)

    # effective timestamp between fromdatestamp and todatestamp. todatestamp could be null: if so use max date 
    if effective_timestamp:
        if not isValidTimestamp(effective_timestamp):
            return None, 'invalid', raise_error(detail='fromdate "{}" is not in RFC3339 format'.format(effective_timestamp)) 

        the_query = the_query.filter(EntityName.fromtimestamp <= effective_timestamp)
        the_query = the_query.filter(func.coalesce(EntityName.totimestamp, datetime.max) >= effective_timestamp)

    results = the_query.all()
    if results:
        return [EntitySchemaWithUuid(
                    uuid=result.entity_id,
                    entity_detail = EntitySchemaNoUuid(
                        name_url = result.name_url,
                        scheme_url = result.scheme_id,
                        fromtimestamp = result.fromtimestamp,
                        totimestamp = result.totimestamp
                        )
                    ) for result in results], 'data', {}
    else:
         return {}, 'no data', raise_error('No data for entity "{}"'.format(name_url))
       