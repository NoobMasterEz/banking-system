import os
from .base import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS =  [ os.path.join(BASE_DIR, 'banking/static/') ]
STATIC_URL =  BASE_DIR + '/banking/static/'
