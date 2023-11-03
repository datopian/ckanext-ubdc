import datetime

from sqlalchemy import types, Column, Table, desc
from sqlalchemy.dialects.postgresql import JSONB

from ckan.model import meta
from ckan.model import core
from ckan.model import types as _types
from ckan.model import domain_object


log = __import__("logging").getLogger(__name__)


def setup():
    if request_data_access_table.exists():
        log.info("request_data_access table already exists")
        return
    else:
        log.info("Creating request_data_access table")
        request_data_access_table.create()


request_data_access_table = Table(
    "request_data_access",
    meta.metadata,
    Column("id", types.UnicodeText, primary_key=True, default=_types.make_uuid),
    Column("firstname", types.UnicodeText),
    Column("surname", types.UnicodeText),
    Column("organization", types.UnicodeText),
    Column("email", types.UnicodeText),
    Column("telephone", types.UnicodeText),
    Column("country", types.UnicodeText),
    Column("summary_of_project", types.UnicodeText),
    Column("project_funding", types.UnicodeText),
    Column("funding_information", types.UnicodeText),
    Column("wish_to_use_data", types.ARRAY(types.UnicodeText)),
    Column("document_url", types.UnicodeText),
    Column("created", types.DateTime, default=datetime.datetime.utcnow),
    Column("updated", types.DateTime, default=datetime.datetime.utcnow),
    Column("deleted", types.Boolean, default=False),
)


class RequestDataAccess(core.StatefulObjectMixin, domain_object.DomainObject):
    @classmethod
    def get_by_id(cls, id):
        return meta.Session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_all(cls):
        return meta.Session.query(cls).order_by(desc(cls.created)).all()

    @classmethod
    def create(cls, data_dict):
        data = cls(**data_dict)
        meta.Session.add(data)
        meta.Session.commit()
        return data

    @classmethod
    def delete(cls, id):
        data = cls.get_by_id(id)
        if data:
            meta.Session.delete(data)
            meta.Session.commit()
        return data

    @classmethod
    def update(cls, data_dict):
        data = cls.get_by_id(data_dict["id"])
        if data:
            meta.Session.query(cls).filter(cls.id == data_dict["id"]).update(data_dict)
            meta.Session.commit()
        return data


meta.mapper(RequestDataAccess, request_data_access_table)
