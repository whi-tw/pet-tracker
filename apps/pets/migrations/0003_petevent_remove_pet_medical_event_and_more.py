# Generated by Django 4.0.3 on 2022-04-09 21:36

import apps.pets.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_alter_pet_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Date')),
            ],
        ),
        migrations.RemoveField(
            model_name='pet',
            name='medical_event',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='vet_visits',
        ),
        migrations.AlterField(
            model_name='pet',
            name='picture',
            field=models.ImageField(blank=True, default='default_pet_photos/15.jpg', upload_to=apps.pets.models.Pet.pet_photo_file_name),
        ),
        migrations.CreateModel(
            name='HealthEvent',
            fields=[
                ('petevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pets.petevent')),
            ],
            bases=('pets.petevent',),
        ),
        migrations.CreateModel(
            name='VetAppointment',
            fields=[
                ('petevent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pets.petevent')),
            ],
            bases=('pets.petevent',),
        ),
        migrations.DeleteModel(
            name='MedicalEvent',
        ),
        migrations.DeleteModel(
            name='VetVisit',
        ),
        migrations.AddField(
            model_name='petevent',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet'),
        ),
    ]