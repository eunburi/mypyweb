from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from board.models import Question
from common.foms import Userform

from django.contrib.auth.decorators import login_required


#회원가입
def signup(request):
    if request.method == "POST":
        form = Userform(request.POST) # 데이터 입력된 폼
        if form.is_valid():
            form.save() #회원가입 db에 저장
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) # 자동 로그인
            return redirect('/') #index 페이지
    else:
        form = Userform() #빈폼생성
        return render(request, 'common/signup.html')
    context = {'form':form}
    return render(request, 'common/signup.html', context)





