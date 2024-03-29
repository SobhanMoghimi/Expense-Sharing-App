# Generated by Django 4.0.4 on 2024-01-30 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import esa.app.helpers.entities.base_entities
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=256)),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=1024)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='expense_created_by', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.groupentity')),
                ('other_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_other_user', to=settings.AUTH_USER_MODEL)),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(esa.app.helpers.entities.base_entities.TimestampEntity, models.Model),
        ),
        migrations.CreateModel(
            name='SplitEntity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('percentage', models.FloatField(null=True)),
                ('share', models.IntegerField()),
                ('split_type', models.CharField(choices=[('0', 'Equal'), ('1', 'Exact'), ('2', 'Percentage')], max_length=32)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.expenseentity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(esa.app.helpers.entities.base_entities.TimestampEntity, models.Model),
        ),
    ]
