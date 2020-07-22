from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

##########################################
###休暇情報管理画面 使用DB(model)MDayoff - TMembers
###一覧 新規追加
##########################################

def dayoffallfunc(request):
    context = {
        'dayoff_list':MDayoff.objects.filter(delete_flg = 0)
    }
    return render(request, 'dayoffall.html',context)

def dayoffcreatefunc(request):
    if request.method == 'POST':
        #TODO：休暇等IDはオートインクリメントさせたいからそのようにしたい:OK!

        dayoff_Name = request.POST['dayoff_Name']
        dayoff_Attribute = request.POST['dayoff_attribute']
        work_Time = request.POST['work_time']
        dt_now = datetime.datetime.now()

        newDayoff = MDayoff.objects.create(dayoff_name = dayoff_Name,dayoff_attribute=dayoff_Attribute,work_time = work_Time,
                        create_date = dt_now,create_by = 1 ,update_date=dt_now,update_by = 1)

        newDayoff.save()
        return render(request,'login.html')

    return render(request,'dayoffcreate.html')




##########################################
###ログイン画面 使用DB(model)TMembes
##########################################

def loginfunc(request):
    if  request.method == 'POST':

        members_id2 = request.POST['members_Id']
        password2 = request.POST['password']

        if type(request.POST['members_Id'])is str == True:#is strが（）の外になかったため比較ができていなかった
            error = {'error':'members_Idは半角数字で入力してください'} #todo:各種エラーが表示されないが他のメイン機能優先する
            return render(request,'login.html',error)

        try:
            entries = TMembers.objects.get(members_id=members_id2,password=password2)

            if entries is not None:
                return redirect('eturan')
            else:
                print(entries)
                return render(request,'login.html', {'error':'入力されたユーザーは登録されていません'})
        ##entriesに何も入ってなかった場合
        except:
            return redirect('login')

    return render(request,'login.html')

##########################################
###社員情報管理画面　使用DB(model)TMembers
# 閲覧/追加/更新/削除
##########################################

# def getformdata():        まとめておいて使いたい
#         members_Id = request.POST['members_Id']
#         members_Name = request.POST['members_Name']
#         password = request.POST['password']
#         admin_Flg = request.POST['admin_Flg']
#         allpayd_Days = request.POST['allpayd_Days']
#         dt_now = datetime.datetime.now()

#         return members_Id,members_Name,password,admin_Flg,allpayd_Days,dt_now

####
#一覧閲覧
####
def eturanfunc(request):
    context = {
        'members_list':TMembers.objects.all()
    }
    return render(request, 'eturan.html',context)

####
#新規追加
####
def createfunc(request):
    if request.method == 'POST':

        #TODO:メンバーズIDはオートインクリメントしてほしいナ……
        members_Id = request.POST['members_Id']
        members_Name = request.POST['members_Name']
        password = request.POST['password']
        admin_Flg = request.POST['admin_Flg']
        allpayd_Days = request.POST['allpayd_Days']

        dt_now = datetime.datetime.now()
        try:
            member = TMembers.objects.get(members_id = members_Id)
            error = {'error':'このユーザーは登録されています'}
            return render(request, 'eturan.html',error)
        except:
            user = TMembers(members_id = members_Id,members_name = members_Name,password = password,
                            admin_flg = admin_Flg,allpayd_days = int(allpayd_Days),create_date = dt_now,
                            create_by = "仮",update_date=dt_now,update_by = "仮")

            user.save()
            return render(request,'login.html')

    return render(request,'createmembers.html')

####
#更新
####
def updatemembersfunc(request):
    if request.method == 'POST':
        members_Id = request.POST['members_Id']
        members_Name = request.POST['members_Name']
        password = request.POST['password']
        admin_Flg = request.POST['admin_Flg']
        allpayd_Days = request.POST['allpayd_Days']

        create_Date = TMembers.objects.values_list('create_date', flat=True).get(pk = members_Id)
        create_By   = TMembers.objects.values_list('create_by', flat=True).get(pk = members_Id)
        dt_now = datetime.datetime.now()
        user = TMembers(members_id = members_Id,members_name = members_Name,password = password,
                        admin_flg = admin_Flg,allpayd_days = int(allpayd_Days),create_date = create_Date,
                        create_by = create_By,update_date=dt_now,update_by = "仮")

        try:
            member = TMembers.objects.get(members_id = members_Id)
            user.save()
            return render(request,'login.html')
        except:
            error = {'error':'このユーザーは登録されていません'}
            return render(request, 'eturan.html',error)    

    return render(request,'updatemembers.html')

####
#削除
####
def deletemembersfunc(request):
    if request.method == 'POST':
        members_Id = request.POST['members_Id']
        delete_Flg = request.POST['delete_Flg']

        try:
            member = TMembers.objects.get(members_id = members_Id)
            if delete_Flg == "1":
                member.delete()
                message = {'message':'削除しました'}
                print("削除しました")
            else:
                message = {'message':'削除キャンセルしました'}
                print("削除キャンセルしました")
            return render(request,'login.html',message)

        except:
            error = {'error':'このユーザーは登録されていません'}
            return render(request, 'eturan.html',error)    

    return render(request,'deletemembers.html')
