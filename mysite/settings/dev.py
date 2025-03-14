from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!=r5%c#ur+fz1rb(hen#q6h5*4nx@691$+l@m#*m%1sub+u8kj"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_SSL = True  # Enable SSL
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_HOST_USER = "info@teravolt.com.bo"
EMAIL_HOST_PASSWORD = "N4Be3FCj7nVE"



try:
    from .local import *
except ImportError:
    pass
