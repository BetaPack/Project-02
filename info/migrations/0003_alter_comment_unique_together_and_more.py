# Generated by Django 4.2.7 on 2024-11-01 10:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("info", "0002_favcityentry_comment"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="comment",
            unique_together={("author", "comment")},
        ),
        migrations.AlterUniqueTogether(
            name="favcityentry",
            unique_together={("user", "city", "country")},
        ),
    ]
