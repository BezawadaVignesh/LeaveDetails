import json
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LeaveRequestForm
from django.contrib.auth import get_user_model

from .models import CLS, CCLS, SLS
from .verifier import get_cls_left, generate_leaves


@login_required
def view_self(request):
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls], [str(ccl.on_date) for ccl in ccls], [str(sl.on_date)
                                                                                                       for sl in sls]

    cls_left = get_cls_left(len(cl_list))
    sls_left = 5 - len(sl_list)
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)
        if l_form.is_valid():
            cd = l_form.cleaned_data
            from_date: date = cd.get('from_date')
            no = cd.get('no_of_leaves')

            dates = generate_leaves(from_date, no)
            print(f"{sls_left=}")
            for d in dates:
                if str(d) in cl_list or str(d) in ccl_list or str(d) in sl_list:
                    messages.add_message(request, messages.INFO, f"Leave is already applied on : {d}")
                    continue
                if cls_left - 1 >= 0:
                    CLS.objects.create(on_date=d, user=user)
                    cls_left -= 1
                elif user.ccl_left - 1 >= 0:
                    CCLS.objects.create(on_date=d,  user=user)
                    user.ccl_left -= 1
                elif sls_left - 1 >= 0:
                    SLS.objects.create(on_date=d, user=user)
                    sls_left -= 1
                else:
                    messages.add_message(request, messages.INFO, f"Leaves limit exceeded")
                    break
            return redirect(request.META['HTTP_REFERER'])

    else:
        l_form = LeaveRequestForm()

    return render(request, 'users/view_self.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list}),
        "l_form": l_form,
        "ur": user,
        "cls_left": cls_left})


@login_required
def remove_leave(request):
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [str(cl.on_date) for cl in cls], [str(ccl.on_date) for ccl in ccls], [str(sl.on_date)
                                                                                                       for sl in sls]

    cls_left = get_cls_left(len(cl_list))
    if request.method == 'POST':
        l_form = LeaveRequestForm(request.POST)
        if l_form.is_valid():
            cd = l_form.cleaned_data
            from_date = cd.get('from_date')
            no = cd.get('no_of_leaves')

            dates = generate_leaves(from_date, no)

            for d in dates:
                if str(d) in cl_list:
                    CLS.objects.filter(on_date=d, user=user).delete()
                elif str(d) in ccl_list:
                    CCLS.objects.filter(on_date=d, user=user).delete()
                elif str(d) in sl_list:
                    SLS.objects.filter(on_date=d, user=user).delete()
                else:
                    messages.add_message(request, messages.INFO, f"No leave to remove on : {d}")

            return redirect(request.META['HTTP_REFERER'])
    else:
        l_form = LeaveRequestForm()
    return render(request, 'users/delete_leave.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list}),
        "l_form": l_form,
        "ur": user,
        "cls_left": cls_left})


@login_required
def home(request):
    cls = request.user.cls.all()
    cl_list, ccl_list, sl_list = [], [], []
    for cl in request.user.cls.all():
        cl_list.append(str(cl.on_date))
    for ccl in request.user.ccls.all():
        ccl_list.append(str(ccl.on_date))
    for sl in request.user.sls.all():
        sl_list.append(str(sl.on_date))
    return render(request, 'users/home.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list})})
