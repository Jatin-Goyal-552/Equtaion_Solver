from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
import re
from io import BytesIO
from PIL import Image
import re
import base64
import os
from PIL import Image
from itertools import groupby
import numpy as np
import keras
from math import *
import json
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.conf import settings
from django.contrib import messages

# Create your views here.

def register(request):
    global username,email,password,OTP
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password1')
            print("email",email)
            OTP = np.random.randint(100000, 999999)
            email_subject = "OTP varification for Your account"
            email_body = "Thanks for showing intrest in Survelon Series products. OTP for your account is {}".format(OTP)
            print(send_mail( email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False))
            return render(request, 'otp2.html')
            # form.save()
            # user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            # return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)

def check_otp(request):
    global username,email,password,OTP
    if request.method == 'POST':
        otp = request.POST['otp']
        print(OTP, otp)
        if OTP==int(otp):
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            print('user created')
            messages.info(request,"You are now registered... Please login to continue.")
            return redirect('login')
        else:
            messages.info(request,"OTP didn't match, Please register again.")
            return render(request, 'otp2.html')

def login1(request):
    if request.method == 'POST':
        username  = request.POST.get('your_name')
        print(username )
        password =request.POST.get('your_pass')
        print(password)
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                # internship=Internships.objects.all()
                # # print(internship[0].iid)
                # context={
                #     'name':request.user,
                #     'internships':internship,
                #     'user_id':request.user.id
                # }
                # print(context)
                # return render(request, 'admin_home.html',context)
                return redirect('admin_home')
            global name
            name=username
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    
    return render(request,'login.html')

def logout1(request):
    logout(request)
    return redirect('login')


def home(request):
    # if request.method == 'POST':
    #     link=request.POST.get('data')
    #     # print("hello",link)
    #     datauri = link

    #     image_data = re.sub("^data:image/png;base64,", "", link)
    #     image_data = base64.b64decode(image_data)
    #     image_data = BytesIO(image_data)
    #     # print(image_data)
    #     im = Image.open(image_data)
    #     try:
    #         im.save('test_image/output.png')
    #     except:
    #         os.remove("test_image/output.png")
    #         im.save('test_image/output.png')
    #     image = Image.open("test_image/output.png").convert("L")
    #     w = image.size[0]
    #     h = image.size[1]
    #     r = w / h 
    #     new_w = int(r * 28)
    #     new_h = 28
    #     new_image = image.resize((new_w, new_h))
    #     new_image_arr = np.array(new_image)

    #     new_inv_image_arr = 255 - new_image_arr

    #     final_image_arr = new_inv_image_arr / 255.0
    #     m = final_image_arr.any(0)
    #     out = [final_image_arr[:,[*g]] for k, g in groupby(np.arange(len(m)), lambda x: m[x] != 0) if k]
    #     num_of_elements = len(out)
    #     elements_list = []
    #     for x in range(0, num_of_elements):
    #         img = out[x]
            
    #         width = img.shape[1]
    #         filler = (final_image_arr.shape[0] - width) / 2
            
    #         if filler.is_integer() == False:    
    #             filler_l = int(filler)
    #             filler_r = int(filler) + 1
    #         else:                              
    #             filler_l = int(filler)
    #             filler_r = int(filler)
            
    #         arr_l = np.zeros((final_image_arr.shape[0], filler_l))
    #         arr_r = np.zeros((final_image_arr.shape[0], filler_r)) 
            
    #         help_ = np.concatenate((arr_l, img), axis= 1)
    #         element_arr = np.concatenate((help_, arr_r), axis= 1)
            
    #         element_arr.resize(28, 28, 1) 
    #         elements_list.append(element_arr)
    #     elements_array = np.array(elements_list)
    #     elements_array = elements_array.reshape(-1, 28, 28, 1)
    #     model = keras.models.load_model("model_scratch.h5")
    #     elements_pred =  model.predict(elements_array)
    #     elements_pred = np.argmax(elements_pred, axis = 1)
    #     dic={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:'/',11:'+',12:'-',13:'*'}
    #     eqt=""
    #     for i in elements_pred:
    #         eqt+=str(dic[i])+""
    #         print(dic[i],end=" ")
    #     print()
    #     print(eqt)
        
    #     print(eval(eqt))
    #     ans=eval(eqt)

    context={'user':request.user.id,'name':request.user}
    return render(request, "home.html",context)

def predict(request):
    print("hrrlo")
    ans="hello"
    eqt="hello"
    if request.method == 'POST':
        print("hello again")
        link=request.POST['operation']
        print("hello",link)
        datauri = link

        image_data = re.sub("^data:image/png;base64,", "", link)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        # print(image_data)
        im = Image.open(image_data)
        try:
            im.save('test_image/output.png')
        except:
            os.remove("test_image/output.png")
            im.save('test_image/output.png')
        image = Image.open("test_image/output.png").convert("L")
        r = image.size[0] / image.size[1] 
        width = int(r * 28)
        height = 28
        temp = image.resize((width, height))
        array = np.array(temp)

        inverse_final = (255 - array)/ 255.0
        lst= inverse_final.any(0)
        individual_array = [inverse_final[:,[*value]] for key, value in groupby(np.arange(len(lst)), lambda x: lst[x] != 0) if key]
        num_of_digits = len(individual_array)
        digits = []
        for x in range(0, num_of_digits):
            img = individual_array[x]
                    
            width = img.shape[1]
            space_to_fill= (28 - width) / 2
                    
            if space_to_fill.is_integer() == False:    
                space_to_fill_l = int(space_to_fill)
                space_to_fill_r = int(space_to_fill) + 1
            else:                              
                space_to_fill_l = int(space_to_fill)
                space_to_fill_r = int(space_to_fill)
                    
            space_to_fill_arr_l = np.zeros((28, space_to_fill_l))
            space_to_fill_arr_r = np.zeros((28, space_to_fill_r)) 
                    
            left = np.concatenate((space_to_fill_arr_l, img), axis= 1)
            digit = np.concatenate((left, space_to_fill_arr_r), axis= 1)
                    
            digit.resize(28, 28, 1) 
            digits.append(digit)
        digit_array = np.array(digits)
        digit_array = digit_array.reshape(-1, 28, 28, 1)
        model = keras.models.load_model("model_scratch2.h5")
        digits_pred =  model.predict(digit_array)
        digits_pred = np.argmax(digits_pred, axis = 1)
        dic={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:'/',11:'+',12:'-',13:'*'}
        eqt=""
        for i in digits_pred:
            eqt+=str(dic[i])+""
            print(dic[i],end=" ")
        print()
        print(eqt)
        
        print(eval(eqt))
        ans=eval(eqt)
        print("-"*20)
        print(ans)
    return HttpResponse(json.dumps({'ans':ans,'eqt':eqt}), content_type="application/json")