from django.shortcuts import render,redirect,HttpResponsePermanentRedirect
from django.contrib.auth import logout,login,authenticate,update_session_auth_hash
from .models import Product, Contact, Order, OrderUpdate,ProjectSetting,UserProfile
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignupForm,UserUpdateForm,ProfileUpdateForm

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# Create your views here.
from django.http import HttpResponse
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'



def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    setting = ProjectSetting.objects.get(pk=1)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {
    'allProds':allProds,
    'setting':setting,
    
    }
    return render(request, 'shop/index.html', params)

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    setting = ProjectSetting.objects.get(pk=1)
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {
    'allProds': allProds,
    "msg": "",
    'setting':setting,
    }
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)



def about(request):
    setting = ProjectSetting.objects.get(pk=1)
    params = {
    
    'setting':setting,
    }
    return render(request, 'shop/about.html',params)


def contact(request):
    setting = ProjectSetting.objects.get(pk=1)
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, '" Your message has been sent successfully . We will inform you soon"')
        return redirect('ShopHome')
    context={
    'setting':setting,
    }
    return render(request, 'shop/contact.html',context)


def tracker(request):
    setting = ProjectSetting.objects.get(pk=1)
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        print(f'{orderId}{email}')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timesetup})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                                          default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"noitem"}')
    context={
    'setting':setting,
    }
    
    return render(request, 'shop/tracker.html',context)





def productView(request, myid):

    # Fetch the product using the id
    setting = ProjectSetting.objects.get(pk=1)
    product = Product.objects.filter(id=myid)
    current_user=request.user
    profile=UserProfile.objects.get(user_id=current_user.id)
    context={
    'setting':setting,
    'product':product[0],
    'profile':profile,
    }
    return render(request, 'shop/prodView.html', context)


def checkout(request):
    setting = ProjectSetting.objects.get(pk=1)
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    
        param_dict={

                'MID': 'WorldP64425807474247',
                'ORDER_ID': 'str(order.order_id)',
                'TXN_AMOUNT': 'str(amount)',
                'CUST_ID': 'email',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
    context={
    'setting':setting,
    
    }
    return render(request, 'shop/checkout.html',context)

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def paytm(request):
    param_dict={

    'MID': 'WorldP64425807474247',
    'ORDER_ID': 'str(order.order_id)',
    'TXN_AMOUNT': 'str(amount)',
    'CUST_ID': 'email',
    'INDUSTRY_TYPE_ID': 'Retail',
    'WEBSITE': 'WEBSTAGING',
    'CHANNEL_ID': 'WEB',
    'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

    }
    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
    return  render(request, 'shop/paytm.html', {'param_dict': param_dict})

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, '" You Have Successfully Logged in to Mr. Pharmacy"')
            return redirect('ShopHome')
            
        else:
            messages.error(request, '  Your username or password is invalid.. Please Try Again..! ')
    
    setting = ProjectSetting.objects.get(id=1)
    context={
        
        'setting':setting,
    }
    return render(request,'shop/user_login.html',context)


def user_logout(request):
    logout(request)
    messages.error(request, '  "You Have Successfully Logged Out From Mr. Pharmacy "')
    return redirect('ShopHome')



def user_register(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="user_img/avatar.png"
            data.save()
            messages.info(request, '" You Have Successfully Registered an Account in Mr. Pharmacy"')
            return redirect('ShopHome')
        else:
            messages.error(request, '  Something went wrong...! Please try again...   ')

    else:
        form=SignupForm()
    
    setting = ProjectSetting.objects.get(id=1)
    context={
        
        'setting':setting,
        'form':form,
    }
    return render(request,'shop/user_register.html',context)


def user_profile(request):
    
    setting = ProjectSetting.objects.get(id=1)
    current_user=request.user
    profile=UserProfile.objects.get(user_id=current_user.id)
    context={
        
        'setting':setting,
        'profile':profile,
    }
    return render(request,'shop/user_profile.html',context)

@login_required(login_url='/user/login')
def user_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '" Your account has been updated successfully"')
            return redirect('user_profile')

    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user)
        
        setting = ProjectSetting.objects.get(id=1)

        current_user=request.user
        profile=UserProfile.objects.get(user_id=current_user.id)
        context={
        'user_form':user_form,
        'profile_form':profile_form,
        'setting':setting,
        'profile':profile,    
        }
        return render(request,'shop/user_update.html',context)


@login_required(login_url='/user/login')
def user_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request, '" Your password has been changed successfully"')
            return redirect('user_profile')
        else:
            messages.error(request, '" Please correct the error below."<br>'+str(form.errors))
            return redirect('user_password')
    else:
        
        setting = ProjectSetting.objects.get(id=1)
        form=PasswordChangeForm(request.user)
        context={
        'form':form,
        
        'setting':setting,
                
        }
        return render(request,'shop/userpasswordupdate.html',context)

