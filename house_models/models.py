from django.db import models

class House(models.Model):
    address = models.CharField(max_length=80)

class Room(models.Model):
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

class Control(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

# class State(models.Model):
#     control = models.ForeignKey(Control, on_delete=models.CASCADE)
#     prev_state =
#     next_state =




# Create your models here.
