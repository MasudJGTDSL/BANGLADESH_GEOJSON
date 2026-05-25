import logging
from django.conf import settings
# LOGGING = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "handlers": {
#             "file": {
#                 "level": "DEBUG",  # Set this to the desired log level.
#                 "class": "logging.FileHandler",
#                 "filename": "django.log",  # Provide the path to the log file.
#             },
#         },
#         "loggers": {
#             "django": {
#                 "handlers": ["file"],
#                 "level": "DEBUG",  # Set this to the desired log level.
#                 "propagate": True,
#             },
#         },
#         # "builtins": [
#         #     "fdr.fdr_tag",
#         # ],
#     }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": settings.BASE_DIR / "django_debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.security.csrf": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}