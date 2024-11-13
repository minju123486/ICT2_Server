from django.contrib import admin


from .models import User_data, Tour_place, Check, StampTable,  history
# Register your models here. 
admin.site.register(User_data)
admin.site.register(Tour_place)
admin.site.register(Check)
admin.site.register(StampTable)
admin.site.register(history)