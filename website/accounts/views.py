from django.shortcuts import render,redirect,render_to_response
from accounts.forms import RegistrationForm,EditProfileForm
from django.http import HttpResponse,HttpResponseRedirect,request
from accounts.forms import Calc,ProfileForm
import functools
import requests, pickle
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = 'accounts/profile_details.html'

    def get(self, request):
        form = ProfileForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('/account/form')

        args={'form':form}
        return render(request,self.template_name,args)


def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login/')
    else:
        form=RegistrationForm()
        args={'form':form}
        return render(request,'accounts/reg_form.html',args)



def profile(request):
    args = {'user':request.user}
    return render(request,'accounts/profile.html',args)


def edit_profile(request):
    if request.method == 'POST':
        form=EditProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form=EditProfileForm(instance=request.user)
        args={'form':form}
        return render(request,'accounts/edit_profile.html',args)


def testprofile(request):
    if request.user.usertype == 'platinum':
        if request.user.userprofile.total_usage < 7:
            return 1
        else:
            return 0
    elif request.user.usertype == 'gold':
        if request.user.userprofile.total_usage < 5:
            return 1
        else:
            return 0
    else:
        if request.user.userprofile.total_usage < 3:
            return 1
        else:
            return 0


x=0

def CalcView(request):
    tup2=Calc(request.POST)
    global x

    if request.method == 'POST':
        if 'input_times' in request.COOKIES:
            x=request.COOKIES['input_times']
            x=int(x)+1
            if request.user.is_authenticated:
                temp = request.user.userprofile.total_usage
                request.user.userprofile.total_usage = temp+1
                request.user.userprofile.save()

    if tup2.is_valid():
        value=request.POST.get('tup')
        vl=[int(a) for a in value.split(',')]
        vs=set(vl)
        lst = list(filter(lambda y: y >= 0 and y <= 10, vs))
        op_file=open('pkldb.pkl','wb')
        pickle.dump(lst,op_file)
        op_file.close()
        value_sum=sum(lst)
        value_avg=value_sum/len(lst)
        length=len(lst)
        pro=functools.reduce(lambda a,b:a*b, lst)
        key_with_index=[]
        for i in range(length):
            data_to_send={
                "key":lst[i],
                "index":i
            }
            key_with_index.append(data_to_send)

        args={'list1':key_with_index,'sum':value_sum,'avg':value_avg,'pro':pro,'length':length}
        return render(request,'accounts/results.html',args)
    if request.user.is_authenticated:
        t=testprofile(request)
    elif x<2:
        t=1
    else:
        t=0
    response=render(request,'accounts/CalcView.html',{'form':tup2,'x':x,'t':t})
    response.set_cookie('input_times', x)
    return response


def result(request):
    op_file = open('pkldb.pkl', 'rb')
    value=pickle.load(op_file)
    vs=value
    lst = list(filter(lambda y: int(y) >= 0 and int(y) <= 10, vs))
    value_sum = sum(lst)
    value_avg = value_sum / len(lst)
    length = len(lst)
    pro = functools.reduce(lambda a, b: a * b, lst)
    op_file.close()

    key_with_index = []
    for i in range(length):
        data_to_send = {
            "key": lst[i],
            "index": i
        }
        key_with_index.append(data_to_send)

    args = {'list1': key_with_index, 'sum': value_sum, 'avg': value_avg, 'pro': pro, 'length': length}
    return render(request, 'accounts/results.html', args)


def drop_val(request,index):
    file_name=open("pkldb.pkl",'rb')
    value=pickle.load(file_name)
    del value[int(index)]
    file_name.close()
    file_name = open("pkldb.pkl", 'wb')
    pickle.dump(value,file_name)
    file_name.close()
    return HttpResponseRedirect('/account/result')


def temperature(request):
    zipcode = request.POST.get('zip')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',in&appid=8d8aed89449f29a30a4ff1acf6152dc0')
    json_object=r.json()
    temp_k=float(json_object['main']['temp'])
    temp_c=temp_k - 273.15
    temp_f=((temp_c * 1.8) + 32)
    temp_c=round(temp_c,2)
    temp_f=round(temp_f,2)
    return render(request,'accounts/temperature.html',{'temp':temp_f,'tempc':temp_c})


def index(request):
    return render(request,'accounts/index.html')

