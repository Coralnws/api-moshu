# Generated by Django 4.0.3 on 2022-08-07 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_diagram_componentdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='isPublic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='document',
            name='version',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='document',
            name='belongTo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.project'),
        ),
        migrations.AlterField(
            model_name='document',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='DocumentChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(db_index=True, default=0)),
                ('requestId', models.CharField(max_length=64, unique=True)),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('parentVersion', models.IntegerField(default=0)),
                ('data', models.TextField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.document')),
            ],
            options={
                'unique_together': {('document', 'requestId', 'parentVersion'), ('document', 'version')},
            },
        ),
    ]