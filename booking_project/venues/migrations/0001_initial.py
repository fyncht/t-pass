# Generated by Django 4.2.8 on 2023-12-09 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=300)),
                ('services', models.JSONField()),
                ('availability', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user_contact', models.CharField(max_length=200)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='venues.venue')),
            ],
        ),
    ]