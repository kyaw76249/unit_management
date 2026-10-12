from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UnitsCommandHq, UnitsTatma, UnitsSkkh, UnitsInfantry, UnitsLightInfantry, UnitsArmsHQ, \
    UnitsArtillery, UnitsArmored, UnitsSignals, UnitsTraining

# Models များကို Admin တွင် Register လုပ်ခြင်း
admin.site.register(UnitsCommandHq)
admin.site.register(UnitsTatma)
admin.site.register(UnitsSkkh)
admin.site.register(UnitsInfantry)
admin.site.register(UnitsLightInfantry)
admin.site.register(UnitsArmsHQ)
admin.site.register(UnitsArtillery)
admin.site.register(UnitsArmored)
admin.site.register(UnitsSignals)
admin.site.register(UnitsTraining)
# မူလ UserAdmin ကို Custom လုပ်ပြီး Name နဲ့ Email တွေ ပေါ်လာစေရန်
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name','last_name', 'email', 'is_staff', 'is_active') # Admin စာရင်းဇယားမှာ ပြမည့် fields များ
    search_fields = ('username', 'first_name','last_name', 'email') # ရှာဖွေလိုရမည့် fields များ

# မူလ User အား unregister လုပ်ပြီး CustomAdmin ဖြင့် ပြန်လည် ချိတ်ဆက်ခြင်း
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)