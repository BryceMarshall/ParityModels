from django.test import TestCase

from house_models.models import House, Room, Control


class ModelsTestCase(TestCase):
    def setUp(self):
        house = House.objects.create(address='123 Example Drive')

        room1 = Room.objects.create(house=house, name='Kitchen')
        room2 = Room.objects.create(house=house, name='Living Room')
        room3 = Room.objects.create(house=house, name='Bedroom')

        Control.objects.create(room=room1, control_type='switch', state='off')
        Control.objects.create(room=room1, control_type='switch', state='off')

        Control.objects.create(room=room2, control_type='switch', state='off')
        Control.objects.create(room=room2, control_type='indoor_temperature', state=23)
        Control.objects.create(room=room2, control_type='thermostat', state='off')

        Control.objects.create(room=room3, control_type='switch', state='off')

    def testThermostat(self):
        pass

    def testTemperatureSensor(self):
        pass

    def testSwitch(self):
        switch = Control.objects.first()
        switch.state = "on"
        switch.save()
        switch.state = "off"
        switch.save()

        switch.state = "halfway"
        self.assertRaises(ValueError, switch.save)

        print(switch.state)
        assert switch.state == 'off'


