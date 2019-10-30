from django.shortcuts import render
from django.shortcuts import render, redirect 
from .forms import Newform
from .models import Imgs

# Create your views here.

def home(request):
    return render(request,'cddd_app/home.html')
    
    
def ip(request):
    if request.method == "POST":
        # display = Imgs.objects.get()
        ipt = Newform(request.POST,request.FILES)  
        if ipt.is_valid():
            # n = ipt.cleaned_data['name']
            # ln = ipt.cleaned_data['lname']
            # p = ipt.cleaned_data['pwd']
            t = Imgs()
            t.img = ipt.cleaned_data['image']
            k = t.img
            t.save()
            # ipt.save()
            # return redirect('image upload success')
            # d = {"name":n,"lname":ln,"pwd":p}
            return render(request,'cddd_app/disp.html',{"k":k})
        else:
            d = {"name":"XXX","lname":"XXX","pwd":"XXX"}
            return render(request,'cddd_app/disp.html',{'data':d})
    else:
        ipform = Newform() 
        return render(request,'cddd_app/ip.html',{'form':ipform})

def disp(request):
    return render(request,'cddd_app/disp.html')