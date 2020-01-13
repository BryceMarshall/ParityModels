from django.test import TestCase

from house_models import models
from house_models.models import House, Room, Control, ControlState, Sensor


class ModelsTestCase(TestCase):
    def setUp(self):
        house = House.objects.create(address='123 Example Drive')

        room1 = Room.objects.create(house=house, name='Kitchen')
        room2 = Room.objects.create(house=house, name='Living Room')
        room3 = Room.objects.create(house=house, name='Bedroom')

        Control.objects.create(room=room1, control_type='switch', state='off')
        Control.objects.create(room=room1, control_type='switch', state='off')

        Control.objects.create(room=room2, control_type='switch', state='off')
        Sensor.objects.create(room=room2, sensor_type='indoor_temperature', value=23)
        Control.objects.create(room=room2, control_type='thermostat', state='off')

        Control.objects.create(room=room3, control_type='switch', state='off')

    def test_thermostat(self):
        thermostat = Control.objects.filter(control_type="thermostat").first()
        valid_states = models.CONTROL_TYPES["thermostat"]

        thermostat.state = "on"
        thermostat.save() #invalid state

        for state in valid_states:
            thermostat.state = state
            thermostat.save()

        thermostat.state = "on"
        thermostat.save() #invalid state

        thermostat.state = "off"
        thermostat.save()

        control_states = ControlState.objects.filter(control=thermostat)
        assert [ctrl_state.state for ctrl_state in control_states] == ["off"] + list(valid_states) + ["off"]



    def test_temperature_sensor(self):
        indoor_sensor = Sensor.objects.filter(sensor_type="indoor_temperature").first()

        indoor_sensor.value = 23
        indoor_sensor.save()
        indoor_sensor.value = -1000000
        indoor_sensor.save()
        print(indoor_sensor.value)
        assert indoor_sensor.value == 23
        indoor_sensor.value = 100000
        indoor_sensor.save()



    def test_switch(self):
        switch = Control.objects.first()
        switch.state = "on"
        switch.save()

        switch.state = "off"
        switch.save()

        switch.state = "halfway"
        switch.save()
        assert switch.state == 'off'

        control_states = ControlState.objects.filter(control=switch)
        assert [ctrl_state.state for ctrl_state in control_states] == ["off", "on", "off"]
