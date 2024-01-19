from enum import Enum
from django.db import models


class RequestMethod(Enum):
    GET = 0
    POST = 1