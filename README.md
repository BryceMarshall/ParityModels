Assumptions:

- Split Sensor apart from Control in order to store controls (inputs to system) seperately from sensors (data points)

- Used Address as an example House identifier

- Used sqlite database for convenience - would use Postgres in production environment 

- Next Improvements:
    - Do validation for valid control states/sensor values on the model instead of in save()
    - Show possible control values in Django UI (had trouble populating 'choices' field dynamically - should they have been another table?)
 