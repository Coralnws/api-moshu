# Generated by Django 4.0.3 on 2022-08-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_customuser_is_active_alter_document_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='content',
            field=models.TextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(max_length=10000),
        ),
    ]