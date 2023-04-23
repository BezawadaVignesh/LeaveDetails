import json
from datetime import date

from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LeaveRequestForm, SearchSIDFrom, HolidayForm, UserUpdateForm, ProfileUpdateForm, UserRegisterForm, \
    ProfileCreationForm, BaseHolidayFormSet
from django.contrib.auth import get_user_model

from .models import CLS, CCLS, SLS, CustomUser, Holidays, EPLS
from .verifier import get_cls_left, generate_leaves


def get_or_none(modelAny, **kwargs):
    try:
        return modelAny.objects.get(**kwargs)
    except modelAny.DoesNotExist:
        return None


def sep_leave_types(leaves):
    full = []
    half = []

    for l in leaves:
        if l.half:
            half.append(l)
        else:
            full.append(l)

    return full, half


#
# def postive_sum(aList):
#     s = 0
#     for x in aList:
#         if x > 0:
#             s = s + x
#     return s
#
#
# def get_cls_left(datelist, p_month):
#     reserve = 1.5
#     n_leaves = [-1 for _ in range(12)]
#     for d in datelist:
#         n_leaves[d.month] += 1
#
#     from_reserve = postive_sum(n_leaves)
#     left = reserve - from_reserve + p_month + 1.5 if p_month > 6 else 0
#
#     return left

def form_date(hly, cls, ccls, sls):
    h_dates = [(str(h.on_date), str(h.desc)) for h in hly]
    cls_full, cls_half = sep_leave_types(cls)
    ccls_full, ccls_half = sep_leave_types(ccls)
    sls_full, sls_half = sep_leave_types(sls)
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls_full], [str(ccl.on_date) for ccl in ccls_full], [
        str(sl.on_date)
        for sl in sls_full]
    h_cl_list, h_ccl_list, h_sl_list = [str(cl.on_date) for cl in cls_half], [str(ccl.on_date) for ccl in ccls_half], [
        str(sl.on_date)
        for sl in sls_half]
    return {"data": json.dumps(
        {"cls_list": cl_list, "h_cl_list": h_cl_list, "ccls_list": ccl_list, "h_ccl_list": h_ccl_list,
         "h_sl_list": h_sl_list, "sls_list": sl_list,
         "h_list": h_dates})}, cl_list, ccl_list, sl_list, h_cl_list, h_ccl_list, h_sl_list


def helper(request, user, sid, dates, half_day):
    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cls_full, cls_half = sep_leave_types(cls)
    context, cl_list, ccl_list, sl_list, h_cl_list, h_ccl_list, h_sl_list = form_date(Holidays.objects.all(), cls, ccls,
                                                                                      sls)
    l = 0.5 if half_day else 1
    count = 0
    for d in dates:
        s_d = str(d)
        if s_d in cl_list or s_d in ccl_list or s_d in sl_list or \
                s_d in h_cl_list or s_d in h_ccl_list or s_d in h_sl_list:
            messages.add_message(request, messages.INFO, f"Leave is already applied on : {d}")
            continue
        count += 1
        if half_day:
            cls_left = get_cls_left([cl.on_date for cl in cls_full], [cl.on_date for cl in cls_half] + [d],
                                    d.month)
        else:
            cls_left = get_cls_left([cl.on_date for cl in cls_full] + [d], [cl.on_date for cl in cls_half],
                                    d.month)
        if cls_left >= 0:
            CLS.objects.create(on_date=d, user=user, half=half_day)
            if half_day:
                cls_half.append(d)
            else:
                cls_full.append(d)

        elif user.profile.ccl_left - l >= 0:
            CCLS.objects.create(on_date=d, user=user, half=half_day)
            user.profile.ccl_left -= l
            user.profile.save()
        elif user.profile.ssl_left - l >= 0:
            SLS.objects.create(on_date=d, user=user, half=half_day)
            user.profile.ssl_left -= l
            user.profile.save()
        else:
            messages.add_message(request, messages.INFO, f"Leaves limit exceeded")
            break
    messages.info(request, f"Done! added {count} leaves ")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def view_self(request):
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls, epls = user.cls.all(), user.ccls.all(), user.sls.all(), user.epls.all()
    cls_full, cls_half = sep_leave_types(cls)
    ccls_full, ccls_half = sep_leave_types(ccls)
    sls_full, sls_half = sep_leave_types(sls)
    epls_full, epls_half = sep_leave_types(epls)
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls_full], [str(ccl.on_date) for ccl in ccls_full], [
        str(sl.on_date)
        for sl in sls_full]
    h_cl_list, h_ccl_list, h_sl_list = [str(cl.on_date) for cl in cls_half], [str(ccl.on_date) for ccl in ccls_half], [
        str(sl.on_date)
        for sl in sls_half]
    epl_list, h_epl_list = [str(epl.on_date) for epl in epls_full], [str(epl.on_date) for epl in epls_half]

    context = {"data": json.dumps(
        {"cls_list": cl_list, "h_cl_list": h_cl_list, "ccls_list": ccl_list, "h_ccl_list": h_ccl_list,
         "h_sl_list": h_sl_list, "sls_list": sl_list, "epl_list" :epl_list, "h_epl_list" : h_epl_list,
         "h_list": h_dates})}
    holiday_dates = [h.on_date for h in Holidays.objects.all()]

    cls_left = get_cls_left([cl.on_date for cl in cls_full], [cl.on_date for cl in cls_half], date.today().month)
    sls_left = user.profile.ssl_left
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)
        if l_form.is_valid():
            cd = l_form.cleaned_data
            from_date: date = cd.get('from_date')

            to_date = cd.get('to_date')
            half_day = cd.get('half') == "True"
            epls = cd.get('Type') == "True"
            no = (to_date - from_date).days + 1
            if no < 1:
                messages.error(request, f"Enter valid dates")
            else:
                dates = generate_leaves(from_date, no, exclude=holiday_dates)

                l = 0.5 if half_day else 1
                count = 0
                for d in dates:
                    s_d = str(d)

                    if s_d in cl_list or s_d in ccl_list or s_d in sl_list or \
                            s_d in h_cl_list or s_d in h_ccl_list or s_d in h_sl_list or \
                            s_d in epl_list or s_d in h_epl_list:
                        messages.add_message(request, messages.INFO, f"Leave is already applied on : {d}")
                        continue

                    if epls:
                        if user.profile.epl_left - l >= 0:
                            EPLS.objects.create(on_date=d, user=user, half=half_day)
                            user.profile.epl_left -= l
                            count += 1
                            continue
                        else:
                            messages.info(request, f"EPLs limit exceed")
                            break
                    count += 1
                    if half_day:
                        cls_left = get_cls_left([cl.on_date for cl in cls_full], [cl.on_date for cl in cls_half] + [d],
                                                d.month)
                    else:
                        cls_left = get_cls_left([cl.on_date for cl in cls_full] + [d], [cl.on_date for cl in cls_half],
                                                d.month)
                    if cls_left >= 0:
                        CLS.objects.create(on_date=d, user=user, half=half_day)
                        if half_day:
                            cls_half.append(d)
                        else:
                            cls_full.append(d)

                    elif user.profile.ccl_left - l >= 0:
                        CCLS.objects.create(on_date=d, user=user, half=half_day)
                        user.profile.ccl_left -= l

                    elif user.profile.ssl_left - l >= 0:
                        SLS.objects.create(on_date=d, user=user, half=half_day)
                        user.profile.ssl_left -= l

                    else:
                        messages.add_message(request, messages.INFO, f"Leaves limit exceeded")
                        break
                user.profile.save()
                messages.info(request, f"Done! added {count} leaves ")
                return redirect(request.META['HTTP_REFERER'])

    else:
        l_form = LeaveRequestForm()
    context["l_form"] = l_form
    context["user"] = user
    context["cls_left"] = cls_left
    context["epl_list"] = epl_list
    context["h_epl_list"] = h_epl_list
    return render(request, 'users/add_leave.html', context)


@login_required
def remove_leave(request):
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls, epls = user.cls.all(), user.ccls.all(), user.sls.all(), user.epls.all()
    cls_full, cls_half = sep_leave_types(cls)
    ccls_full, ccls_half = sep_leave_types(ccls)
    sls_full, sls_half = sep_leave_types(sls)
    epls_full, epls_half = sep_leave_types(epls)
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls_full], [str(ccl.on_date) for ccl in ccls_full], [
        str(sl.on_date)
        for sl in sls_full]
    h_cl_list, h_ccl_list, h_sl_list = [str(cl.on_date) for cl in cls_half], [str(ccl.on_date) for ccl in ccls_half], [
        str(sl.on_date)
        for sl in sls_half]
    epl_list, h_epl_list = [str(epl.on_date) for epl in epls_full], [str(epl.on_date) for epl in epls_half]

    context = {"data": json.dumps(
        {"cls_list": cl_list, "h_cl_list": h_cl_list, "ccls_list": ccl_list, "h_ccl_list": h_ccl_list,
         "h_sl_list": h_sl_list, "sls_list": sl_list, "epl_list": epl_list, "h_epl_list": h_epl_list,
         "h_list": h_dates})}

    cls_left = get_cls_left([cl.on_date for cl in cls_full], [cl.on_date for cl in cls_half], date.today().month)

    # cls_left = get_cls_left(len(cl_list))
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)

        if l_form.is_valid():
            print("form is rready for validation")
            cd = l_form.cleaned_data
            from_date: date = cd.get('from_date')

            to_date = cd.get('to_date')

            no = (to_date - from_date).days + 1
            if no < 1:
                messages.error(request, f"Enter valid dates")
            else:
                dates = generate_leaves(from_date, no)
                print(dates)
                for d in dates:
                    if str(d) in cl_list or str(d) in h_cl_list:
                        CLS.objects.filter(on_date=d, user=user).delete()
                    elif str(d) in epl_list:
                        EPLS.objects.filter(on_date=d, user=user).delete()
                        user.profile.epl_left += 1
                    elif str(d) in h_epl_list:
                        EPLS.objects.filter(on_date=d, user=user).delete()
                        user.profile.epl_left += 0.5
                    elif str(d) in ccl_list:
                        CCLS.objects.filter(on_date=d, user=user).delete()
                        user.profile.ccl_left += 1
                    elif str(d) in h_ccl_list:
                        CCLS.objects.filter(on_date=d, user=user).delete()
                        user.profile.ccl_left += 0.5
                    elif str(d) in sl_list:
                        SLS.objects.get(on_date=d, user=user).delete()
                        user.profile.ssl_left += 0.5
                    elif str(d) in h_sl_list:
                        SLS.objects.get(on_date=d, user=user).delete()
                        user.profile.ssl_left += 0.5
                    else:
                        messages.add_message(request, messages.INFO, f"No leave to remove on : {d}")
                user.profile.save()

                return redirect(request.META['HTTP_REFERER'])
    else:
        l_form = LeaveRequestForm(initial={'half': "True", 'Type': "False"})

    context["l_form"] = l_form
    context["user"] = user
    context["cls_left"] = cls_left
    context["epl_list"] = epl_list
    context["h_epl_list"] = h_epl_list
    print(h_epl_list)
    return render(request, 'users/delete_leave.html', context)


@login_required
def search_sid(request):
    if not request.user.is_superuser:
        messages.warning(request, "login as admin to view")
        return redirect('login')
    if request.method == 'POST':
        form = SearchSIDFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sid = cd.get('sid')
            if get_or_none(CustomUser, sid=sid) is None:
                messages.warning(request, '⚠️ Enter a valid user sid')
            else:
                # next_page = request.GET.get('next')
                # base_url = reverse(next_page) if next_page is not None else reverse('view_self')
                base_url = reverse('profile')
                return redirect(base_url + f'?sid={sid}')
    else:
        form = SearchSIDFrom()
    return render(request, 'users/search_sid.html', {'form': form})


@login_required
def home(request):
    if not request.user.is_superuser:
        messages.warning(request, "login as admin to view")
        return redirect('login')

    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            from_date = cd.get('from_date')
            no = int(cd.get('no_of_leaves'))
            desc = cd.get('desc')
            dates = generate_leaves(from_date, no)
            h = [i.on_date for i in Holidays.objects.all()]
            for d in dates:
                if d not in h:
                    Holidays.objects.create(on_date=d, desc=desc)
                else:
                    messages.error(request, f"Holiday not added on {d} as it is already a holiday")
            return redirect('home')

    else:
        form = HolidayForm()
    return render(request, 'users/home.html', {
        "data": json.dumps({"h_list": h_dates}),
        "form": form})
    '''HolidayFormSet = formset_factory(HolidayForm, formset=BaseHolidayFormSet)

    return render(request, "users/test.html", {'formset': HolidayFormSet()})'''


@login_required
def holiday_delete(request):
    if not request.user.is_superuser:
        messages.warning(request, "login as admin to view")
        return redirect('login')
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            from_date = cd.get('from_date')
            to_date = cd.get('to_date')
            no = (to_date - from_date).days + 1
            # no = int(cd.get('no_of_leaves'))
            desc = cd.get('desc')
            dates = generate_leaves(from_date, no)
            h = [i.on_date for i in Holidays.objects.all()]
            for d in dates:
                if d in h:
                    Holidays.objects.filter(on_date=d).delete()
                else:
                    messages.error(request, f"No Holiday to remove on {d}")
            return redirect('remove_holiday')

    else:
        form = LeaveRequestForm()
    return render(request, 'users/holiday_delete.html', {
        "data": json.dumps({"h_list": h_dates}),
        "form": form})


@login_required
def profile(request):
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    sid = request.GET.get('sid')
    user = get_or_none(get_user_model(), sid=sid)
    if user == None:
        user = request.user

    cls, ccls, sls, epls = user.cls.all(), user.ccls.all(), user.sls.all(), user.epls.all()
    cls_full, cls_half = sep_leave_types(cls)
    ccls_full, ccls_half = sep_leave_types(ccls)
    sls_full, sls_half = sep_leave_types(sls)
    epls_full, epls_half = sep_leave_types(epls)
    epl_list, h_epl_list = [str(epl.on_date) for epl in epls_full], [str(epl.on_date) for epl in epls_half]

    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls_full], [str(ccl.on_date) for ccl in ccls_full], [
        str(sl.on_date)
        for sl in sls_full]
    h_cl_list, h_ccl_list, h_sl_list = [str(cl.on_date) for cl in cls_half], [str(ccl.on_date) for ccl in ccls_half], [
        str(sl.on_date)
        for sl in sls_half]
    cls_left = get_cls_left([cl.on_date for cl in cls_full], [cl.on_date for cl in cls_half], date.today().month)

    if sid is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), sid=sid)

    return render(request, 'users/profile.html', {
        "user": user,
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list, "h_list": h_dates,
                            "h_cl_list": h_cl_list, "h_ccl_list": h_ccl_list, "h_sl_list": h_sl_list,
                            "epl_list": epl_list, "h_epl_list": h_epl_list}),
        "cls_left": cls_left,

    })


@login_required
def profile_edit(request):
    sid = request.GET.get('sid')
    if sid is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), sid=sid)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            base_url = reverse('profile')
            return redirect(base_url + f'?sid={user.sid}')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_edit.html', context)


@login_required
def register(request):
    if not request.user.is_superuser:
        messages.warning(request, "login as admin to view")
        return redirect('login')
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileCreationForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            prof = p_form.save(commit=False)
            prof.user = user
            prof.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} is created successfully')
            return redirect('home')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileCreationForm()

    return render(request, 'users/register.html', {'u_form': u_form, 'p_form': p_form})
