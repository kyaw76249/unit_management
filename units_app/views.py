from django.contrib.admin import display
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import UnitsCommandHq, UnitsInfantry, UnitsLightInfantry, UnitsSkkh, UnitsTatma, UnitsArmsHQ, \
    UnitsArtillery, UnitsArmored, UnitsSignals, UnitsTraining
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import re
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UsernameChangeForm, UserProfileForm
from .models import UserProfile



# Category အလိုက် Model များကို ချိတ်ဆက်ပေးသော Map
MODEL_MAP = {
    'HQ': UnitsCommandHq,
    'Division': UnitsTatma,
    'SKK': UnitsSkkh,
    'Infantry': UnitsInfantry,
    'LightInfantry': UnitsLightInfantry,
    'ArmsHQ': UnitsArmsHQ,
    'Artillery': UnitsArtillery,
    'Armored': UnitsArmored,
    'Signals': UnitsSignals,

    'Training': UnitsTraining,
}

from functools import wraps

def profile_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile
                print(f"User: {request.user.username}, Name: {profile.name}, Rank: {profile.rank}")
                # အကယ်၍ အမည် (name) သို့မဟုတ် အရေးကြီး အချက်အလက် ကွက်လ่างနေလျှင်
                if not profile.name or not profile.rank:
                    messages.warning(request, 'ကျေးဇူးပြု၍ ပထမဦးစွာ ကိုယ်ရေးအချက်အလက်များ ဖြည့်စွက်ပါ။')
                    return redirect('profile_edit')
            except UserProfile.DoesNotExist:
                return redirect('profile_edit')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# ၁။ စာရင်းကြည့်ရန်နှင့် ရှာဖွေရန် (List & Search)
# ၁။ စာရင်းကြည့်ရန်နှင့် ရှာဖွေရန် (List & Search)
@login_required(login_url='login')
@profile_required
def unit_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('cat', '').strip()
    query = " ".join(query.split())
    query = re.sub(r'([ခဂတပစ][က-ဪဿ]+)(\d+)', r'\1 \2', query)
    units = []
    sub_units = []
    display_units = []
    is_search = False
    page_title = " "
    page_obj = ""

    # 1. တိုက်ရိုက် Search လုပ်လျှင် (q ပါလာလျှင်)
    if query:
        is_search = True
        category = " "

        if 'လကခ' in query or 'သင်တန်း' in query:
            category = 'Training'
        command_shortname = ['တမခ','စကခ','တမခ','နပတ','မပခ','ရမခ','တသခ','ရပခ','ရတခ','ကရခ','နတခ','နပခ','ရကတ','နမခ','လပခ','တပခ','ကကမ', 'ကကသံ','ကကဆက်','လကခ']
        if 'ခလရ' in query or 'ခမရ' in query:
            page_title = f"{query} အချက်အလက်များ"
        elif any(keyword in query for keyword in command_shortname):
            page_title = f"{query} လက်အောက်ရှိတပ်များ"
        elif 'မြို့' in query:
            page_title = f"{query} တွင် ရှိသောတပ်များ"
        else:
            page_title = f"{query} အတွက် ရှာဖွေတွေ့ရှိချက်များ"

        target_keys = ['Infantry', 'LightInfantry','ArmsHQ', 'Artillery', 'Armored', 'Signals', 'Training','Antiaircraft']

        for mod_key, mod in MODEL_MAP.items():
            if mod_key in target_keys:
                try:
                    m_filters = Q()
                    if hasattr(mod, 'superior_command'):
                        m_filters |= Q(superior_command__icontains=query)
                    if hasattr(mod, 'unit_name'):
                        m_filters |= Q(unit_name__iexact=query)
                    if hasattr(mod, 'location'):
                        m_filters |= Q(location__icontains=query)
                    if hasattr(mod, 'command_hq'):
                        m_filters |= Q(command_hq__icontains=query)
                    if hasattr(mod, 'arm_name'):
                        m_filters |= Q(arm_name__iexact=query)

                    matched = mod.objects.filter(m_filters)
                    for obj in matched:
                        if obj not in sub_units:
                            sub_units.append(obj)
                except Exception:
                    pass

        display_units = sub_units

    # 2. Category အလိုက် ကြည့်လျှင်
    elif category:
        if category in MODEL_MAP:
            units = MODEL_MAP[category].objects.all()
            if category == 'HQ':
                page_title = "တိုင်းစစ်ဌာနချုပ်များ"
            elif category == 'Division':
                page_title = "တပ်မဌာနချုပ်များ(တမခ)"
            elif category == 'SKK':
                page_title = "စစ်ဆင်ရေးကွပ်ကဲမှုဌာနချုပ်များ(စကခ)"
            elif category == 'Infantry':
                page_title = "ခြေလျင်တပ်ရင်း အချက်အလက်များ"
            elif category == 'LightInfantry':
                page_title = "ခြေမြန်တပ်ရင်း အချက်အလက်များ"
            elif category == 'Artillery':
                page_title = "အမြောက်တပ်ဖွဲ့ အချက်အလက်များ"
            elif category == 'ArmsHQ':
                page_title = "ညွှန်ကြားရေးမှူးရုံးများ"
            elif category == 'Armored':
                page_title = "သံချပ်ကာတပ်ဖွဲ့ အချက်အလက်များ"
            elif category == 'Signals':
                page_title = "ဆက်သွယ်ရေးတပ်ဖွဲ့ အချက်အလက်များ"
            elif category == 'Training':
                page_title = "သင်တန်းကျောင်းများ"
        display_units = units

    # 3. ဘာမှ မလုပ်ရသေးလျှင် (Default)
    else:
        display_units = []
        # Search လုပ်ထားခြင်း ရှိ၊ မရှိ အပေါ် မူတည်၍ paginator ဖြင့် စာမျက်နှာခွဲခြင်း


    paginator = Paginator(display_units, 15)  # တစ်မျက်နှာလျှင် ဒေတာ ၁၅ ခုပြရန်
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 💡 Category များ၏ အစဉ်လိုက် စာရင်း
    category_order = ['HQ', 'Division', 'SKK', 'Infantry', 'LightInfantry', 'ArmsHQ', 'Artillery', 'Armored', 'Signals',
                      'Training']

    next_category = ""
    prev_category = ""

    if category in category_order:
        curr_index = category_order.index(category)
        if curr_index < len(category_order) - 1:
            next_category = category_order[curr_index + 1]
        if curr_index > 0:
            prev_category = category_order[curr_index - 1]
        # 💡 Category တစ်ခုချင်းအလိုက် စုစုပေါင်း အရေအတွက်များ တွက်ချက်ခြင်း


    category_counts = {
         'total_units': sum(model.objects.count() for model in MODEL_MAP.values()),
         'HQ_count': MODEL_MAP['HQ'].objects.count(),
        'Division_count': MODEL_MAP['Division'].objects.count(),
        'SKK_count': MODEL_MAP['SKK'].objects.count(),
        'Infantry_count': MODEL_MAP['Infantry'].objects.count(),
        'LightInfantry_count': MODEL_MAP['LightInfantry'].objects.count(),
        'ArmsHQ_count': MODEL_MAP['ArmsHQ'].objects.count(),
        'Artillery_count': MODEL_MAP['Artillery'].objects.count(),
        'Armored_count': MODEL_MAP['Armored'].objects.count(),
        'Signals_count': MODEL_MAP['Signals'].objects.count(),
        'Training_count': MODEL_MAP['Training'].objects.count(),
    }
    context = {
        'units': units,
        'sub_units': sub_units,
        'display_units': page_obj,
        'query': query,
        'current_category': category,
        'is_search': is_search,
        'page_title': page_title,
        'page_obj': page_obj,
        'next_category' : next_category,
        'prev_category' : prev_category,
        **category_counts
    }
    return render(request, 'units_app/unit_list.html', context)

# ၂။ အချက်အလက်အသစ်ထည့်ရန် (Add)
@login_required(login_url='login')
def unit_add(request):
    category = request.GET.get('cat', 'Infantry')
    model_class = MODEL_MAP.get(category, UnitsInfantry)

    if request.method == 'POST':
        name = request.POST.get('unit_name')
        location = request.POST.get('location')
        superior_command = request.POST.get('superior_command')
        badge = request.FILES.get('badge')
        command_hq = request.POST.get('command_hq')

        if category == 'HQ':
            model_class.objects.create(
                command_name=name,
                location=location,
                superior_command=superior_command,
                badge=badge
            )
        elif category == 'ArmsHQ':
            model_class.objects.create(
                arm_name=name,
                location=location or 'နေပြည်တော်',
                superior_command=superior_command or 'ကက(ကြည်း)',
                badge=badge
            )
        elif category in ['Artillery', 'Armored', 'Signals', 'Training']:
            if category == 'Armored':
                default_cup_cmd = superior_command or 'ကကသံ'
            else:
                default_cup_cmd = superior_command or 'ကကမ'
            model_class.objects.create(
                unit_name=name,
                location=location,
                superior_command=default_cup_cmd,
                command_hq=command_hq
            )
        else:
            kwargs = {
                'location': location,
                'superior_command': superior_command
            }

            if category in ['Command', 'Division', 'SKK', 'ArmsHQ', 'Training']:
                if hasattr(model_class, 'badge') and badge:
                    kwargs['badge'] = badge

            if hasattr(model_class, 'command_name'):
                kwargs['command_name'] = name
            elif hasattr(model_class, 'unit_name'):
                kwargs['unit_name'] = name

            model_class.objects.create(**kwargs)

        return redirect(f"/?cat={category}")

    context = {'current_category': category}
    return render(request, 'units_app/unit_add.html', context)


# ၃။ အချက်အလက်ပြင်ဆင်ရန် (Update)
@login_required(login_url='login')
def unit_update(request, pk):
    category = request.GET.get('cat', 'Infantry')
    model_class = MODEL_MAP.get(category, UnitsInfantry)
    unit = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('unit_name')
        location = request.POST.get('location')
        superior_command = request.POST.get('superior_command')
        command_hq = request.POST.get('command_hq')
        badge = request.FILES.get('badge')

        if category == 'HQ' and hasattr(unit, 'command_name'):
            unit.command_name = name
        elif category == 'ArmsHQ' and hasattr(unit, 'arm_name'):
            unit.arm_name = name
        elif hasattr(unit, 'unit_name'):
            unit.unit_name = name

        unit.location = location
        if hasattr(unit, 'superior_command'):
            unit.superior_command = superior_command
        if hasattr(unit, 'command_hq'):
            unit.command_hq = command_hq

        if hasattr(unit, 'badge') and badge:
            unit.badge = badge
        unit.save()
        return redirect(f"/?cat={category}")

    context = {'unit': unit, 'current_category': category}
    return render(request, 'units_app/unit_add.html', context)

    # ၄။ အချက်အလက်တစ်ခုချင်း ဖျက်ရန် (Delete)
@login_required(login_url='login')
def unit_delete(request, pk):
        if not request.user.is_staff:
            return redirect('unit_list')

        category = request.GET.get('cat', 'Infantry')
        model_class = MODEL_MAP.get(category, UnitsInfantry)
        unit = get_object_or_404(model_class, pk=pk)

        unit.delete()
        return redirect(f"/?cat={category}")

    # ၅။ ယခု Category ထဲရှိ အချက်အလက်အားလုံးကို ရှင်းလင်းဖျက်ဆီးရန် (Clear All)
@login_required(login_url='login')
def unit_clear(request):
        if not request.user.is_staff:
            return redirect('unit_list')

        category = request.GET.get('cat', 'Infantry')
        model_class = MODEL_MAP.get(category, UnitsInfantry)
        model_class.objects.all().delete()

        return redirect(f"/?cat={category}")

def custom_logout(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # 👈 Built-in UserCreationForm ကို သုံးပါ
        if form.is_valid():
            user = form.save(commit=False)# username နဲ့ password ကို အလိုအလျောက် သိမ်းပေးပါမည်
            user.is_active = False
            user.save()
            messages.success(request, 'အကောင့်ဖွင့်ခြင်း အောင်မြင်ပါသည်။ ကျေးဇူးပြု၍ Login ဝင်ပါ။')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'units_app/register.html', {'form': form})




@login_required
def profile_edit_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=profile)
            password_form = PasswordChangeForm(request.user)

            if profile_form.has_changed() or username_form.has_changed():
                if username_form.is_valid() and profile_form.is_valid():
                    username_form.save()
                    profile_form.save()
                    messages.success(request, 'Profile အချက်အလက်များ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။')
                     # 💡 အချက်အလက် အကုန်ဖြည့်ပြီး သိမ်းလိုက်တာနဲ့ Home သို့ တိုက်ရိုက်ရောက်သွားပါမည်
                    return redirect('profile_edit')
            else:
                messages.info(request, 'အချက်အလက်များဖြည့်သွင်းပါ။')
                return redirect('profile_edit')
        elif 'change_password' in request.POST:
            username_form = UsernameChangeForm(instance=request.user)
            profile_form = UserProfileForm(instance=profile)
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'စကားဝှက် (Password) အောင်မြင်စွာ ပြောင်းလဲပြီးပါပြီ။')
                return redirect('profile_edit')
    else:
        username_form = UsernameChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    context = {
        'username_form': username_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'units_app/profile_edit.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('unit_list')  # အောင်မြင်ပါက ရောက်ရမည့် home url name
    else:
        form = AuthenticationForm()

    return render(request, 'units_app/login.html', {'form': form})



@login_required
def home_view(request):
    try:
        profile = request.user.userprofile

        # အချက်အလက် မပြည့်စုံသေးပါက Profile ဖြည့်ရန် ပို့မည်
        if not profile.name or not profile.gazette_no:
            messages.warning(request, 'ကျေးဇူးပြု၍ ပထမဦးစွာ ကိုယ်ရေးအချက်အလက်များကို ပြည့်စုံစွာ ဖြည့်စွက်ပါ။')
            return redirect('profile_edit')

    except UserProfile.DoesNotExist:
        return redirect('profile_edit')

    # အချက်အလက် ပြည့်စုံပြီးသားဆိုရင် Home စာမျက်နှာကို ပြမည်
    return render(request, 'units_app/unit_list.html')


# တပ်ဖွဲ့ဝင်များ စာရင်းပြမည့် View
@login_required
def profile_list_view(request):

    profiles = UserProfile.objects.all().order_by('bc_no')
    context = {'profiles': profiles}
    return render(request, 'units_app/profile_list.html', context)

# တစ်ယောက်ချင်းစီ၏ အသေးစိတ် အချက်အလက်ပြမည့် View
@login_required
def profile_detail_view(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    context = {'profile': profile}
    return render(request, 'units_app/profile_detail.html', context)

