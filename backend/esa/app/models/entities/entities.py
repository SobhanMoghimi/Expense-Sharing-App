from _decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from esa.app.helpers.entities.base_entities import DeletableEntity
from django.core.validators import MinValueValidator
from django.db import models

from esa.app.helpers.entities.base_entities import CommonEntity



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        values = [email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f"The {field_name} value must be set")

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, password, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(password=password, email=email, **extra_fields)


class UserEntity(AbstractBaseUser, PermissionsMixin, DeletableEntity):
    email = models.EmailField(max_length=80, unique=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32)

    friends = models.ManyToManyField("self", blank=True, symmetrical=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        app_label = 'app'

    def __str__(self):
        return self.email


class GroupEntity(CommonEntity):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    members = models.ManyToManyField(UserEntity)
    created_by = models.ForeignKey(UserEntity, related_name="created_by", on_delete=models.DO_NOTHING)

class ExpenseEntity(CommonEntity):
    amount = models.IntegerField()
    created_by = models.ForeignKey(UserEntity, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=1024)
    group = models.ForeignKey(GroupEntity, on_delete=models.DO_NOTHING, null=True, db_constraint=False)
