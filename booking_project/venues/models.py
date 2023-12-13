from django.db import models


# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    services = models.JSONField()  # требует PostgreSQL
    availability = models.JSONField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    venue = models.ForeignKey(Venue, related_name='bookings', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_contact = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.venue.name} booking from {self.start_time} to {self.end_time}'


