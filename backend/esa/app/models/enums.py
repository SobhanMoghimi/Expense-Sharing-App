from enum import Enum
from django.db import models


class RequestMethod(Enum):
    GET = 0
    POST = 1

class SplitType(models.TextChoices):
    EQUAL = 0
    EXACT = 1
    PERCENTAGE = 2