# Generated by Django 3.1 on 2020-08-15 23:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jawanndenn", "0002_django_extensions_3_0_0"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="expires_at",
            field=models.DateTimeField(null=True),
        ),
    ]
