from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

controlTypes = {"switch": ("off", "on"),
                "indoor_temperature": range(-40, 60),  # Example range for Celcius sensor
                "thermostat": ('off', 'cool', 'heat', 'fan-on', 'auto')
                }


class House(models.Model):
    address = models.CharField(max_length=80)


class Room(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)


class Control(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    control_type = models.CharField(max_length=32, validators=[lambda control: control in controlTypes])
    state = models.CharField(max_length=8)


@receiver(pre_save, sender=Control)
def control_handler(sender, instance=None, **kwargs):
    if validateState(instance.state, instance.control_type):
        print("validated")
    else:
        instance.state = controlTypes[instance.control_type][0]
        raise ValueError("Invalid state for control")


def validateState(state, control_type=""):
    return state in controlTypes[control_type]


class Control_State(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    state = models.CharField(max_length=16)
    timestamp = models.DateTimeField("Update Time")

# Create your models here.
