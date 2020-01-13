Assumptions:

- Split Sensor apart from Control in order to store controls (inputs to system) seperately from sensors(data points)

- Used Address as a House identifier - many other fields could have been added

- Possible Improvements:
    - Do validation for valid control states/sensor values on the model instead of in save()
    - Show possible values in Django UI
 