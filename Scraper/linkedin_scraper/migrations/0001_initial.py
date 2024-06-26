# Generated by Django 3.0 on 2024-01-09 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('company_name', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=2000)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
