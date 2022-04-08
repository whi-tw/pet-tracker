# Generated by Django 4.0.3 on 2022-04-08 12:25

import apps.pets.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.IntegerField(choices=[(1, 'Cat'), (2, 'Dog')])),
                ('breed', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name='Date of Birth')),
                ('sex', models.IntegerField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Unknown')], default=3)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VetVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to=apps.pets.models.Pet.pet_photo_file_name)),
                ('animal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pets.animal', verbose_name='Animal Details')),
                ('medical_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pets.medicalevent')),
                ('vet_visits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pets.vetvisit')),
            ],
        ),
    ]