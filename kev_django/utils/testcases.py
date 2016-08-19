from django.test import TransactionTestCase
from django.conf import settings

from kev_django.utils.loading import kev_handler


class KevTestCase(TransactionTestCase):

    def _post_teardown(self):
        super(KevTestCase,self)._post_teardown()
        for db_label in settings.KEV_TEST.keys():
            resp = kev_handler.get_db(db_label).flush_db()

        
