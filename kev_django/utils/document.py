from kev.document import Document as KevDoc
from .loading import get_db


class Document(KevDoc):
    
    @classmethod
    def get_db(cls):
        return get_db(cls.Meta.use_db)