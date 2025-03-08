# Generated by Django 4.1.4 on 2022-12-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=10)),
                ('code_id', models.CharField(max_length=6)),
                ('title', models.CharField(max_length=30)),
                ('code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('server_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('secret_key', models.CharField(max_length=20)),
            ],
        ),
    ]
