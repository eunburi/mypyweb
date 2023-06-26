from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'board/index.html')
    # return HttpResponse("<h1>웹 메인 페이지 입니다.</h1>")

#질문 목록
def question_list(request):
    #오름차순
    #question_list = Question.objects.all()
    question_list = Question.objects.order_by('-create_date')  #내림차순
    #페이지 처리
    page = request.GET.get('page', '1')
    paginator = Paginator(question_list, 10) #페이지당 게시글 -10
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    #404페이지처리
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'board/detail.html', context)

#질문등록
@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST": #소문자 post 일경우 > 등록안됨
        form = QuestionForm(request.POST) # 입력된 데이터가 있는 폼
        if form.is_valid(): # 폼이 유효성 검사를 통과했다면
            question = form.save(commit=False) #가짜저장
            question.author = request.user  # 세션권한이 있는 (로그인한) 글쓴이
            question.create_date = timezone.now() # 등록일 생성
            form.save() # 진짜 저장
            return redirect('board:question_list') #질문목록 페이지로 이동 
            
    else: #get방식       
        form = QuestionForm() #폼 객체 생성(빈 폼 생성)
    context = {'form': form}
    return render(request, 'board/question_form.html', context) # get방식

#답변등록
@login_required(login_url='common:login') #로그인 페이지 이동
def answer_create(request, question_id):
    #질문이 1개 있어야 답변을 등록할 수 있음
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False) # content만 저장
            answer.author = request.user
            answer.create_date = timezone.now() #답변등록일
            answer.question = question #외래 키 달성
            form.save()
            return redirect('board:detail', question_id=question.id) #question.id

    else:
        form = AnswerForm()  #빈 폼 생성
    context = {'question' : question, 'form':form}
    return render(request, 'board/detail.html',context)

#질문수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    #수정을 위해서 질문 1개 가져옴
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) #커밋이 아직 안됨
            question.modify_date = timezone.now() # 수정일
            question.author = request.user
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) # 데이터가 이미 있는 폼
    context = {'form' : form}
    return render(request, 'board/question_form.html', context)



# 질문삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    # question = Question.objects.get(id=question_id)
    # 모델에서 데이터가 있으면 가져오고 없으면 404 오류처리
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('board:question_list')

#답변삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('board:detail', question_id=answer.question.id)
