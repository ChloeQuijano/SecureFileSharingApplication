# Generated by Django 3.2.8 on 2023-11-12 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='uploads')),
                ('file_key', models.CharField(max_length=500)),
                ('encrypted', models.BooleanField(default=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_shared', models.BooleanField(default=False)),
                ('file_size', models.PositiveIntegerField()),
                ('file_type', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shared_with', models.ManyToManyField(blank=True, related_name='shared_files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileIntegrity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sha256_hash', models.CharField(max_length=64)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileApp.file')),
            ],
        ),
        migrations.CreateModel(
            name='SharedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_date', models.DateTimeField(auto_now=True)),
                ('permission', models.CharField(max_length=50)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileApp.file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'file')},
            },
        ),
    ]
