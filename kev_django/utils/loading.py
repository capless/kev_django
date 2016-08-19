'''
Created on Sep 17, 2014

@author: brian
'''
import sys

from django.conf import settings

from kev.loading import KevHandler

if 'test' in sys.argv:
    kev_handler = KevHandler(settings.KEV_TEST)
else:
    kev_handler = KevHandler(settings.KEV)
get_db = kev_handler.get_db