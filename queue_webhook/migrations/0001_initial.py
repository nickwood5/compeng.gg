# Generated by Django 4.2.5 on 2023-11-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Queued'), (2, 'In Progress'), (3, 'Success'), (4, 'Failure')])),
                ('project_id', models.IntegerField()),
                ('ref', models.TextField()),
                ('before', models.CharField(max_length=40)),
                ('after', models.CharField(max_length=40)),
            ],
        ),
    ]