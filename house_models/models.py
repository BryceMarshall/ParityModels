from django.db import models
from django.db.models import Model
from django.template.base import logger
from django.utils import timezone

CONTROL_TYPES = {"switch": ("off", "on"),
                 "thermostat": ('off', 'cool', 'heat', 'fan-on', 'auto')
                 }

SENSOR_TYPES = {"indoor_temperature": (-40, 40)}


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
        if self.state is not self._last_state and self.state in CONTROL_TYPES[self.control_type]:
            super().save(*args, **kwargs)
            self._last_state = self.state
            cs = ControlState(control=self, state=self.state, timestamp=timezone.now())
            cs.save()
        else:
            self.state = self._last_state
            logger.debug("No changes detected in control ".format(self))

    def __str__(self):
        return "{} {} : State {}".format(self.room, self.control_type, self.state)


class ControlState(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    state = models.CharField(max_length=16)
    timestamp = models.DateTimeField("Update Time")

    def __str__(self):
        return "{} changed to state {} at {}".format(self.control, self.state, self.timestamp)


def sensor_type_validator(sensor):
    return sensor in SENSOR_TYPES


class Sensor(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=32, validators=[sensor_type_validator])
    value = models.IntegerField()  # Could go to float if higher precision needed
    _last_value = None

    def valid_value(self):
        low, hi = SENSOR_TYPES[self.sensor_type]
        return low <= self.value < hi

    def save(self, *args, **kwargs):
        if self.value is not self._last_value and self.valid_value():
            super().save(*args, **kwargs)
            self._last_value = self.value
            ss = SensorState(sensor=self, value=self.value, timestamp=timezone.now())
            ss.save()
        else:
            self.value = self._last_value
            logger.debug("No changes detected in sensor ".format(self))


class SensorState(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateTimeField("Update Time")

    def __str__(self):
        return "{} recorded value {} at {}".format(self.sensor, self.value, self.timestamp)
