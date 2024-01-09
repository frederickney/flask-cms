# coding: utf-8


__author__ = 'Frederick NEY'


import logging


try:
    from .ADLoginController import Controller as ADLoginController
except AttributeError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
except ImportError as e:
    logging.warning(e)
    import traceback
    traceback.print_tb(e.__traceback__)
    pass
#try:
from .OpenIdLoginController import Controller as OpenIdLoginController
#except AttributeError as e:
#    logging.warning(e)
#    import traceback
#    traceback.print_tb(e.__traceback__)
#    pass
#except ImportError as e:
#    logging.warning(e)
#    import traceback
#    traceback.print_tb(e.__traceback__)
#    pass
from .LocalLoginController import Controller as LocalLoginController
