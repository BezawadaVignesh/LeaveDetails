import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import CLSAddForm, CCLSAddForm, SLSAddForm, LeaveRequestForm
from django.contrib.auth import get_user_model

from .models import CLS
from .verifier import get_cls_left, generate_leaves


@login_required
def view_self(request):
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

            dates = generate_leaves(str(from_date), no)
            if no > cls_left:
                print('------------habebe---------')
                NotImplementedError
            else:
                for d in dates:
                    if str(d) not in cl_list and str(d) not in ccl_list and str(d) not in sl_list:
                        CLS.objects.create(on_date=d, user=user)
                    else:
                        messages.add_message(request, messages.INFO, f"Leave is already applied on : {d}")
                return redirect(request.META['HTTP_REFERER'])
    else:
        l_form = LeaveRequestForm()

    # if request.method == 'POST':
    #     cls_add_form = CLSAddForm(request.POST)
    #     ccls_add_form = CCLSAddForm(request.POST)
    #     sls_add_form = SLSAddForm(request.POST)
    #     l = None
    #     if cls_add_form.is_valid():
    #         l = cls_add_form.save(commit=False)
    #     elif ccls_add_form.is_valid():
    #         l = ccls_add_form.save(commit=False)
    #     elif sls_add_form.is_valid():
    #         l = sls_add_form.save(commit=False)
    #     if l is not None:
    #         l.user = user
    #         l.save()
    # else:
    #     cls_add_form = CLSAddForm()
    #     ccls_add_form = CCLSAddForm()
    #     sls_add_form = SLSAddForm()
    #
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

            dates = generate_leaves(str(from_date), no)

            for d in dates:
                if str(d) not in cl_list and str(d) not in ccl_list and str(d) not in sl_list:
                    messages.add_message(request, messages.INFO, f"No leave to remove on : {d}")
                else:
                    CLS.objects.filter(on_date=d, user=user).delete()

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
