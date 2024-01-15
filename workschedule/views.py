from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PersonalinfoModelForm, ShiftAvailabilityForm, SurveyCalendarForm, DefinitionDateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import PersonalinfoModel, SurveyCalendar, ForbiddenPair,DefinitionDate
from .forms import PersonalinfoModelForm
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages

import datetime

from itertools import combinations	
from django.contrib.auth import get_user_model	
UserModel = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to your desired page after login
            return redirect('home')
        else:
            error_message = "username または passwordが間違っています"
    else:
        error_message = ""
        login_user = request.user
    return render(request, 'login.html', {'error_message': error_message, 'login_user': login_user})


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def home(request):

    #未承認の場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect("login")
    
    return render(request, 'home.html', {'user': request.user})


def personalinfo_input(request):

    #未承認の場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_info = PersonalinfoModel.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if user_info:
            form = PersonalinfoModelForm(request.POST, instance=user_info)
        else:
            form = PersonalinfoModelForm(request.POST)

        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = request.user
            user_info.save()
            return redirect('home')
    else:
        if user_info:
            form = PersonalinfoModelForm(instance=user_info)
        else:
            form = PersonalinfoModelForm()

    return render(request, 'personalinfo.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


#@login_required
def form_input(request):

    #未承認の場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect("login")
    
    print("form_input view reached")
    if request.method == 'POST':
        form = ShiftAvailabilityForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合、データを保存
            shift_availability = form.save(commit=False)
            shift_availability.user = request.user  # ログインユーザーを関連付け
            shift_availability.save()
            return redirect('shift_availability_input')  # フォームの再表示
    else:
        form = ShiftAvailabilityForm()

    return render(request, 'availability.html', {'form': form})


def surveyCalendar_view(request):
   
    #未承認の場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect("login")

    form = SurveyCalendarForm()
    # デフォルトのフォームを表示させるため、このuser_infoもコンテキストに入れる。
    user_info = PersonalinfoModel.objects.filter(user=request.user).first()

    if request.method == 'POST':

        #TODO:ここでname="id"の値を取り出し、編集対象のオブジェクトを指定。（新規作成の場合はidの未指定を確認し、オブジェクトの指定はなし。）
        if request.POST["id"] == "":
            #新規作成
            survey_calendar = SurveyCalendar()
        else:
            #編集
            survey_calendar = SurveyCalendar.objects.filter(id=request.POST["id"]).first()


        # 編集の場合は、編集対象のモデルオブジェクトを指定する。（HTML側から編集したいSurveyCalenderのidを送信するようにする。）
        # instance引数に指定をする。
        form = SurveyCalendarForm(request.POST, instance=survey_calendar)

        if form.is_valid():

            print("保存")

            if DefinitionDate.objects.filter(start__lte=form.cleaned_data["date"], end__gte=form.cleaned_data["date"]).exists():
                print("確定済みの日付につき、保存は受け付けない。")

                messages.error(request, "確定済みの日付につき、保存は受け付けない。")

                return redirect('surveyCalendar')

        

            calendar_personal_info = form.save(
                commit=False)  # モデルオブジェクトを作成し、コミットを保留
            calendar_personal_info.user = request.user  # ユーザーを設定
            calendar_personal_info.save()  # データベースに保存
            return redirect('surveyCalendar')
    else:
        if user_info:
            form = SurveyCalendarForm(instance=user_info)
        else:
            form = SurveyCalendarForm()

    return render(request, "surveyCalendar.html", {'form': form, "user_info":user_info})

from .forms import DateSearchForm


def schedule_data(request):
    # FullCalendarの表示範囲のみ表示
    #print(request.GET["start"])
    #print(request.GET["end"])

    form    = DateSearchForm(request.GET)

    if form.is_valid():

      start = form.cleaned_data["start"]

      while True:	
        if start.day == 1:	
          break	

      start += datetime.timedelta(days=1)	
      print(start)

      holidays = []	
     
      while True:
        if start.weekday() == 6 or start.weekday() == 5:	
            holidays.append(start)

        start += datetime.timedelta(days=1)
        if start.day == 1:
            break

        events = SurveyCalendar.objects.filter(date__in=holidays)	
        print(events)

      events = SurveyCalendar.objects.filter(date__gte=form.cleaned_data["start"], date__lte=form.cleaned_data["end"])
    else:
        events = SurveyCalendar.objects.all()

    # fullcalendarのため配列で返却
    list = []

    for event in events:
        

        is_over    = False
        last_day = event.date - datetime.timedelta(days=3)
        next_day = event.date + datetime.timedelta(days=3)

        total    = SurveyCalendar.objects.filter(user=event.user, date__gte=last_day, date__lte=next_day).count()

        if total > 2:
            is_over = True

        bad_pairs = False

        survey_calendars = SurveyCalendar.objects.filter(date=event.date)

        users = []
        for survey_calendar in survey_calendars:
        

         if survey_calendar.user not in users:	
             users.append(survey_calendar.user)

        if len(users) >= 2:
            pairs    = combinations(users, 2)
            
            pairs = [pair for pair in pairs if event.user in pair]
            for pair in pairs:
                forbidden_pairs = ForbiddenPair.objects.all()
                for user in pair:
                    
                    forbidden_pairs = [forbidden_pair for forbidden_pair in forbidden_pairs if user in forbidden_pair.user.all()]

                    if len(forbidden_pairs) > 0:
                        bad_pairs = True

                        break

        if bad_pairs:
            bg_color = "red"
        else:
            bg_color = "green"
        
            if is_over:
             bg_color = "orange"

        if event.date in holidays:

            found   = False

            for holidays_result in holidays_results:
                if holidays_result["title"] == f"{event.user.first_name}{event.user.last_name}":
                    holidays_result["id"].append(str(event.id))
                    found   = True

                    break

            if not found:
                holidays_results.append({ "title":f"{event.user.first_name}{event.user.last_name}", "id":[ str(event.id) ] })



        list.append({
                "id": str(event.id),
                "title": f"{event.user.first_name} {event.user.last_name}",
                "start": event.date,
                "end": event.date,
                "color": bg_color,
                "extendedProps": {
                    "item1": event.item1,
                    "item2": event.item2,
                    "item3": event.item3,
                    "item4": event.item4,
                    "item5": event.item5,
                    "item6": event.item6,
                    "item7": event.item7,
                    "item8": event.item8,
                    }
            }
        )


    print("=====土日のデータの集計結果=====")
    print(holidays_results)
    

    holidays_results    = [ holidays_result for holidays_result in holidays_results if len( holidays_result["id"] ) >= 3 ]

    print("===土日に3回以上====")
    
    print(holidays_results)

   
    warning_list    = []
    for holidays_result in holidays_results:
        warning_list += holidays_result["id"]

     
    for w in warning_list:
        for l in list:
            if w == l["id"]:
                l["color"]  = "orange"
                break
            
        return JsonResponse(list, safe=False)



# 確定処理を受け付けるビュー
def definition_view(request):

    # 未認証の場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect("login")

    # 指定されている日付をバリデーションし、保存する。
    if request.method == 'POST':

        form    = DefinitionDateForm(request.POST)

        if form.is_valid():
            print("確定")
            form.save()

    return redirect("surveyCalendar")


