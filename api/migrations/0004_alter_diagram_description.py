# Generated by Django 4.0.3 on 2022-08-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_diagram_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagram',
            name='description',
            field=models.TextField(max_length=10000, null=True),
        ),
    ]
