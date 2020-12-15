from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm


# 인덱스별 장르 id(인기순위 순서)
match = [28, 18, 53, 10749, 10751,
        878, 14, 12, 35, 80,
        9648, 16, 99, 36, 10752, 
        27, 10402, 37, 10770]


# 선호도를 기준으로 선호도코드를 만드는 함수
def make_code(lis):
    idx_list = []
    for li in lis:
        idx_list.append(match.index(int(li)))
    code = '3333333333333333333'
    for idx in idx_list:
        code = code[:idx] + '5' + code[idx+1:]
    return code


# Create your views here.
@require_http_methods((['GET', 'POST']))
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 선호장르 리스트를 선호도 코드에 넣기
            # 1. 밑의 함수에 넣을 변수를 user.preference에서 뽑아낸다.
            pre_list = user.preference
            # 2. 여기서 user의 preference_code 속성에 넣어줄 값을 계산(함수를 호출)
            pre_code = make_code(pre_list)
            # 3. 다시 저장한다.
            user.preference_code = pre_code
            user.save()
            
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('community:index')


def update_code(pre, new, code):
    pre_idx = []
    new_idx = []
    for li in pre:
        pre_idx.append(match.index(int(li)))
    for li in new:
        new_idx.append(match.index(int(li)))
    # 이전 선호도 초기화
    for idx in pre_idx:
        # 에러 방지(2보다 작을 때 2를 빼면 필드범위를 벗어남 [1~9])
        if int(code[idx]) > 2:
            code = code[:idx] + str(int(code[idx]) - 2) + code[idx+1:]
    # 새로운 선호도 반영
    for idx in new_idx:
        if int(code[idx]) < 8:
            code = code[:idx] + str(int(code[idx]) + 2) + code[idx+1:]
    return code


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        # 유저의 이전 선호도
        pre_pref = request.user.preference

        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            
            # preference_code 업데이트 
            new_pref = user.preference
            pre_code = user.preference_code
            new_code = update_code(pre_pref, new_pref, pre_code)
            # print(new_code, '#############')

            user.preference_code = new_code
            user.save()    

            return redirect('community:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('community:index')


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('community:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def show_pref(code):
    pref_list = []
    for co in code:
        pref_list.append(int(co))
    return pref_list


@login_required
@require_http_methods(['GET'])
def detail(request, user_pk):
    # 1. user id, nickname
    # 2. 작성한 글, 댓글, 추천
    article_user = User.objects.get(pk=user_pk)
    request_user = request.user
    # 둘이 같은지 비교
    if article_user == request_user:
        # 같다면
        user = request_user
    else:
        # 다르다면
        user = article_user
        
    articles = user.article_set.all()
    comments = user.comment_set.all()
    like_articles = user.like_articles.all()
    genre_code = user.preference_code
    context = {
        'user': user,
        'articles': articles,
        'comments': comments,
        'like_articles': like_articles,
        'genre_code': genre_code,
        'article_user': article_user,
    }
    return render(request, 'accounts/detail.html', context)