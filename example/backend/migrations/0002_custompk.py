# Generated by Django 3.0.8 on 2020-09-25 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPk',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
    ]