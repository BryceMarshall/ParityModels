from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

CONTROL_TYPES = {"switch": ("off", "on"),
                 "indoor_temperature": range(-40, 60),  # Example range for Celcius sensor
                 "thermostat": ('off', 'cool', 'heat', 'fan-on', 'auto')
                 }


class House(models.Model):
    address = models.CharField(max_length=80)


class Room(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)


def control_type_validator(control_type):
    return control_type in CONTROL_TYPES


class Control(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    control_type = models.CharField(max_length=32, validators=[control_type_validator])
    state = models.CharField(max_length=8)


@receiver(pre_save, sender=Control)
def control_handler(sender, instance=None, **kwargs):
    if validateState(instance.state, instance.control_type):
        print("validated")
    else:
        instance.state = CONTROL_TYPES[instance.control_type][0]
        raise ValueError("Invalid state for control")


def validateState(state, control_type=""):
    return state in CONTROL_TYPES[control_type]


class ControlState(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    state = models.CharField(max_length=16)
    timestamp = models.DateTimeField("Update Time")

# Create your models here.
