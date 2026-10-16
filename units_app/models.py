from django.db import models
from django.contrib.auth.models import User

# ၁။ ကွပ်ကဲမှုဌာနချုပ် (HQ)
class UnitsCommandHq(models.Model):
    badge = models.ImageField(upload_to='badges/', null=True, blank=True)
    command_name = models.CharField(max_length=100, verbose_name="တပ်ဖွဲ့အမည်")
    location = models.CharField(max_length=100, verbose_name="တည်နေရာ")
    superior_command = models.CharField(max_length=100, blank=True, null=True, verbose_name="ကွပ်ကဲမှုဌာနချုပ်")

    def __str__(self):
        return self. command_name

    class Meta:
        verbose_name = "တိုင်းစစ်ဌာနချုပ်"
        verbose_name_plural = "တိုင်းစစ်ဌာနချုပ်များ"
        db_table = "units_commandhq"


# 2. ခြေလျင်တပ်ရင်းများ
class UnitsInfantry(models.Model):
    unit_name = models.CharField(max_length=100, verbose_name="တပ်ဖွဲ့အမည်")
    location = models.CharField(max_length=100, verbose_name="တည်နေရာ")
    superior_command = models.CharField(max_length=100, blank=True, null=True, verbose_name="ကွပ်ကဲမှုဌာနချုပ်")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "ခြေလျင်တပ်ရင်း"
        verbose_name_plural = "ခြေလျင်တပ်ရင်းများ"
        db_table = "units_infantry"


# ၃။ ခြေမြန်တပ်ရင်းများ (မခလ)
class UnitsLightInfantry(models.Model):
    unit_name = models.CharField(max_length=100, verbose_name="တပ်ဖွဲ့အမည်")
    location = models.CharField(max_length=100, verbose_name="တည်နေရာ")
    superior_command = models.CharField(max_length=100, blank=True, null=True, verbose_name="ကွပ်ကဲမှုဌာနချုပ်")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "ခြေမြန်တပ်ရင်း"
        verbose_name_plural = "ခြေမြန်တပ်ရင်းများ"
        db_table = "units_light_infantry"

# ၄။ စစ်ဆင်ရေးကွပ်ကဲမှုဌာနချုပ် (စကခ)
class UnitsSkkh(models.Model):
    badge = models.ImageField(upload_to='badges/', null=True, blank=True)
    unit_name = models.CharField(max_length=100, verbose_name="တပ်ဖွဲ့အမည်")
    location = models.CharField(max_length=100, verbose_name="တည်နေရာ")
    superior_command = models.CharField(max_length=100, blank=True, null=True, verbose_name="ကွပ်ကဲမှုဌာနချုပ်")
    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "စကခဌာနချုပ်"
        verbose_name_plural = "စကခဌာနချုပ်များ"
        db_table = "units_skkh"

# ၅။ တပ်မဌာနချုပ်များ
class UnitsTatma(models.Model):
    badge = models.ImageField(upload_to='badges/', null=True, blank=True)
    unit_name = models.CharField(max_length=100, verbose_name="တပ်ဖွဲ့အမည်")
    location = models.CharField(max_length=100, verbose_name="တည်နေရာ")
    superior_command = models.CharField(max_length=100, blank=True, null=True, verbose_name="ကွပ်ကဲမှုဌာနချုပ်")
    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "တပ်မဌာနချုပ်"
        verbose_name_plural = "တပ်မဌာနချုပ်များ"
        db_table = "units_tatma"

class UnitsArmsHQ(models.Model):
    badge = models.ImageField(upload_to='badges/', null=True, blank=True)
    arm_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255,default='နေပြည်တော်')
    superior_command = models.CharField(max_length=100, default='ကက(ကြည်း)')

    def __str__(self):
        return self.arm_name
    class Meta:
        verbose_name = "လက်ရုံးတပ်ဖွဲ့"
        verbose_name_plural = "လက်ရုံးတပ်ဖွဲ့များ"
        db_table = 'units_arms_hq'
class UnitsArtillery(models.Model):
    id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=100) # လိုင်းဆင်းရန် TextField သုံးနိုင်ပါသည်
    location = models.CharField(max_length=255)
    superior_command = models.CharField(max_length=100)
    command_hq = models.CharField(max_length=100)
    def __str__(self):
        return self.unit_name
    class Meta:
        verbose_name = "အမြောက်တပ်ဖွဲ့"
        verbose_name_plural = "အမြောက်တပ်ဖွဲ့များ"
        db_table = 'units_artillery'


class UnitsArmored(models.Model):
    id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=100)  # လိုင်းဆင်းရန် TextField သုံးနိုင်ပါသည်
    location = models.CharField(max_length=255)
    superior_command = models.CharField(max_length=100)
    command_hq = models.CharField(max_length=100)

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "သံချပ်ကာတပ်ဖွဲ့"
        verbose_name_plural = "သံချပ်ကာတပ်ဖွဲ့များ"
        db_table = 'units_armored'# 💡 Database ရှိ Table နာမည်အတိုင်း ချိတ်ဆက်ရန်

class UnitsSignals(models.Model):
    id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=100)  # လိုင်းဆင်းရန် TextField သုံးနိုင်ပါသည်
    location = models.CharField(max_length=255)
    superior_command = models.CharField(max_length=100)
    command_hq = models.CharField(max_length=100)

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "ဆက်သွယ်ရေးတပ်ဖွဲ့"
        verbose_name_plural = "ဆက်သွယ်ရေးတပ်ဖွဲ့များ"
        db_table = 'units_signals'




class UnitsTraining(models.Model):
    id = models.AutoField(primary_key=True)
    badge = models.ImageField(upload_to='badges/', null=True, blank=True)
    unit_name = models.CharField(max_length=100)  # လိုင်းဆင်းရန် TextField သုံးနိုင်ပါသည်
    location = models.CharField(max_length=255)
    superior_command = models.CharField(max_length=100)
    command_hq = models.CharField(max_length=100)

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "သင်တန်းကျောင်း"
        verbose_name_plural = "သင်တန်းကျောင်းများ"
        db_table = 'units_training'



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bc_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="ပြန်တမ်းဝင်အမှတ်")
    rank = models.CharField(max_length=50, blank=True, null=True, verbose_name="အဆင့်")
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name="အမည်")
    unit = models.CharField(max_length=150, blank=True, null=True, verbose_name="တပ်")
    location = models.CharField(max_length=150, blank=True, null=True, verbose_name="တည်နေရာ")
    command = models.CharField(max_length=150, blank=True, null=True, verbose_name="ကွပ်ကဲမှု")
    military_command = models.CharField(max_length=150, blank=True, null=True, verbose_name="တိုင်းစစ်ဌာနချုပ်")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="ဖုန်းနံပါတ်")
    address = models.TextField(blank=True, null=True, verbose_name="နေရပ်လိပ်စာ")

    def __str__(self):
        return self.user.username

