import uuid

from django.db import models


class DeletableModelManager(models.Manager):
    def get_queryset(self):
        return super(DeletableModelManager, self).get_queryset().filter(is_deleted=False)


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}-{self.created_at}"


class DeletableEntity(BaseEntity):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = DeletableModelManager()  # just not deleted
    objects_all = models.Manager()  # deleted and not deleted

    def delete(self, hard_delete: bool = False, **kwargs):
        if hard_delete:
            super(DeletableEntity, self).delete(**kwargs)
        else:
            self.is_deleted = True
            self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{super.__str__()}{self.is_deleted}"


class TimestampEntity():
    last_update_time = models.DateTimeField(auto_now=True)


class CommonEntity(TimestampEntity, DeletableEntity):
    class Meta:
        abstract = True
