from django.db import models
from django.db.models import Model
from django.template.base import logger
from django.utils import timezone

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
    _last_state = None

    def save(self, *args, **kwargs):
        if self.state is not self._last_state and self.state in CONTROL_TYPES[self.control_type]
            super().save(*args, **kwargs)
            self._last_state = self.state
            cs = ControlState(control=self, state=self.state, timestamp=timezone.now())
            cs.save()
        else:
            self.state = self._last_state
            logger.debug("No changes detected in control ".format(self))


class ControlState(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    state = models.CharField(max_length=16)
    timestamp = models.DateTimeField("Update Time")

# Create your models here.
