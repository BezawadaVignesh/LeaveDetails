import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CLSAddForm, CCLSAddForm, SLSAddForm
from django.contrib.auth import get_user_model


@login_required
def view_self(request):
    sid = request.GET.get('sid')
    user = get_object_or_404(get_user_model(), sid=sid)

    cls, ccls, sls = user.cls.all(), user.ccls.all(), user.sls.all()
    cl_list, ccl_list, sl_list = [], [], []
    for cl in cls:
        cl_list.append(str(cl.on_date))
    for ccl in ccls:
        ccl_list.append(str(ccl.on_date))
    for sl in sls:
        sl_list.append(str(sl.on_date))

    if request.method == 'POST':
        cls_add_form = CLSAddForm(request.POST)
        ccls_add_form = CCLSAddForm(request.POST)
        sls_add_form = SLSAddForm(request.POST)
        l = None
        if cls_add_form.is_valid():
            l = cls_add_form.save(commit=False)
        elif ccls_add_form.is_valid():
            l = ccls_add_form.save(commit=False)
        elif sls_add_form.is_valid():
            l = sls_add_form.save(commit=False)
        if l is not None:
            l.user = user
            l.save()
    else:
        cls_add_form = CLSAddForm()
        ccls_add_form = CCLSAddForm()
        sls_add_form = SLSAddForm()

    return render(request, 'users/view_self.html', {
        "data": json.dumps({"cls_list": cl_list, "ccls_list": ccl_list, "sls_list": sl_list}),
        "cls_form": cls_add_form,
        "ccls_form": ccls_add_form,
        "sls_form": sls_add_form,
        "ur": user})


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
