from django.contrib import admin
from .models import Region, Department

# Настройка админки
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'region')                             # Указываю какие поля отображать
    search_fields = ('region',)                                 # Указываю по каким полям можно осуществлять поиск
    list_editable = ('region',)                                 # Возможность редактирования поля
    list_filter = ('region',)                                   # Возможность фильтровать поля

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_department', 'address',  'tel', 'website', 'email', 'fio_responsible', 'region_id')
    search_fields = ('name_of_department', 'address',  'tel', 'website', 'email', 'fio_responsible', 'region_id')
    list_editable = ('name_of_department', 'address',  'tel', 'website', 'email', 'fio_responsible', 'region_id')
    list_filter = ('name_of_department', 'address',  'tel', 'website', 'email', 'fio_responsible', 'region_id')


admin.site.register(Region, RegionAdmin)            #!!!Важно соблюдать последовательность регистрации модэлей
admin.site.register(Department, DepartmentAdmin)
