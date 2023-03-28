import json
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LeaveRequestForm, SearchSIDFrom, HolidayForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model

from .models import CLS, CCLS, SLS, CustomUser, Holidays
from .verifier import get_cls_left, generate_leaves


def get_or_none(modelAny, **kwargs):
    try:
        return modelAny.objects.get(**kwargs)
    except modelAny.DoesNotExist:
        return None


@login_required
def view_self(request):
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls], [str(ccl.on_date) for ccl in ccls], [str(sl.on_date)
                                                                                                       for sl in sls]
    holiday_dates = [h.on_date for h in Holidays.objects.all()]

    cls_left = get_cls_left(len([str(cl.on_date) for cl in cls if cl.on_date.month <= date.today().month]))
    sls_left = 5 - len(sl_list)
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)
        if l_form.is_valid():
            cd = l_form.cleaned_data
            from_date: date = cd.get('from_date')

            to_date = cd.get('to_date')
            no = (to_date - from_date).days + 1
            # no = cd.get('no_of_leaves')
            # no = int(no)
            # f_no = no % 1
            # no = no - f_no
            dates = generate_leaves(from_date, no, exclude=holiday_dates)

            l = 1
            count = 0
            for d in dates:
                if str(d) in cl_list or str(d) in ccl_list or str(d) in sl_list:
                    messages.add_message(request, messages.INFO, f"Leave is already applied on : {d}")
                    continue
                count += 1
                cls_left = get_cls_left(len(cl_list), d.month)
                if cls_left - l >= 0:
                    CLS.objects.create(on_date=d, user=user)
                    cl_list.append(str(d))
                elif user.profile.ccl_left - l >= 0:
                    CCLS.objects.create(on_date=d, user=user)
                    user.profile.ccl_left -= l
                    user.profile.save()
                elif sls_left - l >= 0:
                    SLS.objects.create(on_date=d, user=user)
                    sls_left -= l
                else:
                    messages.add_message(request, messages.INFO, f"Leaves limit exceeded")
                    break
            messages.info(request, f"Done! added {count} leaves ")
            return redirect(request.META['HTTP_REFERER'])

    else:
        l_form = LeaveRequestForm()

    return render(request, 'users/add_leave.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list, "h_list": h_dates}),
        "l_form": l_form,
        "user": user,
        "cls_left": cls_left,
    })


@login_required
def remove_leave(request):
    h_dates = [(str(h.on_date), str(h.desc)) for h in Holidays.objects.all()]
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls], [str(ccl.on_date) for ccl in ccls], [str(sl.on_date)
                                                                                                       for sl in sls]
    cls_left = get_cls_left(len([str(cl.on_date) for cl in cls if cl.on_date.month <= date.today().month]))

    # cls_left = get_cls_left(len(cl_list))
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)
        if l_form.is_valid():
            cd = l_form.cleaned_data
            from_date = cd.get('from_date')

            to_date = cd.get('to_date')
            no = (to_date - from_date).days + 1
            # no = cd.get('no_of_leaves')
            # no = int(no)  # for now
            print(f"{no=}")
            dates = generate_leaves(from_date, no)
            print(f"{dates=}")
            l = 1
            for d in dates:
                if str(d) in cl_list:
                    CLS.objects.filter(on_date=d, user=user).delete()
                elif str(d) in ccl_list:
                    CCLS.objects.filter(on_date=d, user=user).delete()
                    user.profile.ccl_left += l
                    user.profile.save()
                elif str(d) in sl_list:
                    SLS.objects.get(on_date=d, user=user).delete()
                else:
                    messages.add_message(request, messages.INFO, f"No leave to remove on : {d}")

            return redirect(request.META['HTTP_REFERER'])
    else:
        l_form = LeaveRequestForm()
    return render(request, 'users/delete_leave.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list, "h_list": h_dates}),
        "l_form": l_form,
        "ur": user,
        "cls_left": cls_left})


@login_required
def search_sid(request):
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


@login_required
def holiday_delete(request):
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
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls], [str(ccl.on_date) for ccl in ccls], [str(sl.on_date)
                                                                                                       for sl in sls]
    cls_left = get_cls_left(len([str(cl.on_date) for cl in cls if cl.on_date.month <= date.today().month]))

    ccls_left = user.profile.ccl_left
    sls_left = 5 - len(sl_list)
    if sid is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), sid=sid)

    return render(request, 'users/profile.html', {
        "user": user,
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list, "h_list": h_dates}),
        "cls_left": cls_left,
        "ccls_left": ccls_left,
        "sls_left": sls_left
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
