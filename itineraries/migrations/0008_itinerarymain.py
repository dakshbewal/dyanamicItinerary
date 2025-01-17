# Generated by Django 4.2.11 on 2024-05-31 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0007_itinerarytemp_alter_itinerarymaster_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItineraryMain',
            fields=[
                ('master_id', models.AutoField(primary_key=True, serialize=False)),
                ('travel_destination', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'master_itinerary',
                'managed': False,
            },
        ),
    ]
