# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import crypto

from datetime import datetime

from manager.models import Voucher, CustomUser


import json

# Create your views here.

def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)

    return render(request, 'login.html')

@login_required(login_url='/')
def getVoucher(request, my_code=None):
    print request.user
    print Voucher.objects.filter(user=request.user)

    context = {}
    if my_code:
        context["code"] = my_code
        voucher = Voucher.objects.filter(code=my_code)
    else:
        voucher = Voucher.objects.filter(user=request.user)
        if voucher:
            context["code"] = voucher[0].code
        else:
            return redirect('/')
    if voucher:
        if not voucher[0].shared:
            newUser = CustomUser(username=crypto.get_random_string(length=12), full_name="Shared by"+voucher[0].user.first_name)
            newUser.save()
            newVoucher=Voucher.objects.get(user=newUser)
            voucher[0].shared=True
            voucher[0].shared_voucher = newVoucher
            voucher[0].save()

        if not voucher[0].shared_voucher.used:
            context["share"] = True
            context["share_code"] = voucher[0].shared_voucher.code
        else: 
            context["share"] = False


        if voucher[0].used:
            context["message"] = "koda je uporabljena :D"
            context["stamp_me"] = False
            
        else:
            context["message"] = "uporabi me"
            context["stamp_me"] = True
    else:
        context["message"] = "imas fejk kodo?"
        context["stamp_me"] = False
        context["share"] = False


    #ofni page za stempilko
    return render(request, 'stamp.html', context)

@login_required(login_url='/')
def getVoucher2(request, my_code=None):
    voucher = None
    context = {}
    if not my_code:
        print "kode ni "
        #Check if looged user has voucher
        voucher = Voucher.objects.filter(user=request.user)
        if voucher:
            voucher = voucher[0]
        else:
            voucher = Voucher.create()
            voucher.user = request.user
            voucher.save()
            context["alert"] = "Naredl smo ti recept"
    else:
        print "kode je"
        voucher = Voucher.objects.filter(user=request.user)
        if voucher:
            print "voucher je"
            voucher = voucher[0]
            if voucher.code != my_code:
                print "not my code"
                context["alert"] = "Že imaš recept, ne se slepomišit"
        else:  
            #logiran user nima voucherja
            voucher = Voucher.objects.filter(code=my_code)
            if voucher:
                voucher = voucher[0]
                if voucher.user:
                    if voucher.user == request.user:
                        context["alert"] = "PIJ"
                    else:
                        context["alert"] = "Nekdo ze ima za voucher, ne se slepomišit"
                else:
                    voucher.user = request.user
                    voucher.save()
            else:
                context["alert"] = "zmislu si si kodo, ne se slepomišit"

    if not voucher.shared:
        newVoucher=Voucher.create()
        voucher.shared=True
        voucher.shared_voucher = newVoucher
        voucher.save()
        context["share_code"] = voucher.shared_voucher.code

    if voucher.shared_voucher.used:
        context["share"] = False
    else:
        context["share"] = True
        context["share_code"] = voucher.shared_voucher.code

    if voucher.used:
            context["message"] = "koda je uporabljena XD"
            context["stamp_me"] = False
            
    else:
        context["message"] = "uporabi me"
        context["stamp_me"] = True

    return render(request, 'stamp.html', context)




def useVoucher(request, my_code):
    context = {}
    voucher = Voucher.objects.filter(code=my_code)
    if voucher:
        if voucher[0].used:
            context["alert"] = "Voucher je ze uproablen WTF?"
            context["drink"] = False
        else:
            voucher[0].used = True
            voucher[0].save()
            context["alert"] = "Tuk pejan pa se kr zejan"
            context["drink"] = True
    return JsonResponse(context)

@login_required(login_url='/')
def logout(request):
    auth_logout(request)
    return redirect('/')
