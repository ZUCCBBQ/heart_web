from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from detetction.models import users
from detetction.detection_form import registerForm
import os
from detetction.heart_prepocess import video_to_frame
from detetction.heart_function import class_function,detection_function
# Create your views here.


def index(request):
    return  render(request,'index.html')

def single(requset):
    return render(requset,"single.html")

def login(request):
    return  render(request,"login.html")

def register(request):
    return render(request,"register.html")

def upload(request):
    return render(request,"upload2.html")

def login_process(request):
    if request.session.get('is_login', None):
        return redirect("/index")
    username = request.POST.get('name')
    password = request.POST.get('password')
    # print(username,password)
    context = {}
    print(username,password)
    if password and username:
        username = username.strip()
        try:
            user_info = users.objects.get(name=username)
            if user_info.password == password:
                request.session['is_login'] = True
                request.session["user_name"] = username
                return redirect('index')
            else:
                context["warning"] = 'wrong password'
                return render(request, 'login.html',context)
        except Exception:
            context["warning"] = 'user have not been resigted'
            return render(request, 'login.html', context)
    else:
        context["warning"] = 'name or password can not be empty'
        return render(request,'login.html',context)


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('index')
    request.session.flush()
    return redirect('index')
def result(request):
    if os.path.exists("F:\\heart_upload\\"+request.session["user_name"]+"\\result"):
        result_location = "F:\\heart_upload\\"+request.session["user_name"]+"\\result"
        file_list = os.listdir(result_location)
        back_local = []
        pre = "image/" + str(request.session["user_name"]) + "/result/"
        print(pre)
        for i in file_list:
            filename_1 = i.split("_")[2]
            # filename = filename_1.split(".")[0]
            back_local.append({"location":pre+i,"filename":filename_1})
        return render(request, 'result.html', {"imgs":back_local})
    else:
        return render(request,"result.html")

def heartregister(request):
    if request.session.get('is_login', None):
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("name")
        emails = request.POST.get("email")
        password = request.POST.get("password_1")
        password_com = request.POST.get("password_2")
        reason = request.POST.get("message")
        print(username,emails,password,password_com,reason)
        if len(username) >16 or len(username)<5:
            username_msg="Illegal username: the username too short or too long"
            return  render(request,"register.html",locals())
        if password != password_com:
            password_msg = "the password should be the same"
            return  render(request,"register.html",locals())
        else:
            same_name = users.objects.filter(name = username)
            if same_name:
                username_msg = "the user name has been used"
                return render(request,"register.html",locals())
            same_emails = users.objects.filter(mails=emails)
            if same_emails:
                emails_msg = "the email has been used"
                return render(request,"register.html",locals())

            new_user = users.objects.create(name=username,password=password,mails=emails,reason=reason)

            return redirect('login')
def video_upload(request):
    video = request.FILES.get("video_file")
    if request.method=="GET":
        return render(request,"upload")
    if request.method=="POST":

        if video == None:
            file_msg = "empty file"
            return render(request, "upload2.html", locals())
        else:
            file_type = video.name.split(".")[1]
            if file_type == "avi":
                user_file = request.session["user_name"]
                location  = "F:\\heart_upload\\"+user_file+"\\video\\"
                filename= os.path.join(location,video.name)
                if os.path.exists(location):
                    pass
                else:
                    os.makedirs(location)
                with open(filename, 'wb+') as f:
                    data = video.read()
                    f.write(data)
                crop_location=video_to_frame("F:\\heart_upload\\"+user_file+"\\video")
                class_location = class_function(crop_location)
                result_location = detection_function(class_location)
                file_list = os.listdir(result_location)
                back_local = []
                pre = "image/" + str(request.session["user_name"]) + "/result/"
                print(pre)
                for i in file_list:
                    filename_1= i.split("_")[2]
                    filename = filename_1.split(".")[0]
                    back_local.append({"location": pre + i,"filename":filename})
                return render(request, 'result.html', {"imgs": back_local})
            else:
                file_msg = "invalid file"
                return render(request,"upload2.html",locals())
    # result_location="F:\\heart_upload\\admin\\result"
    # file_list = os.listdir(result_location)
    # print(file_list)
    # content = {
    #     'imgs': file_list,
    # }
    # return render(request, 'result', content)