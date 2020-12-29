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


# 인덱스별 장르 id
# 인덱스에 따른 배치순서는 좋아하는 장르 통계 참고
match = [28, 18, 53, 10749, 10751,
            878, 14, 12, 35, 80,
            9648, 16, 99, 36, 10752, 
            27, 10402, 37, 10770
        ]


# 선호도 코드는 스트링형태로 저장
# 코드변환시에 int형태로 변환 후 수정
def make_pref_code(lis):
    idx_list = []
    for li in lis:
        idx_list.append(match.index(int(li)))
    code = '3333333333333333333'
    for idx in idx_list:
        code = code[:idx] + '5' + code[idx+1:]
    return code


@require_http_methods((['GET', 'POST']))
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            print('~~~~~~~~~~~~~~~~')
            print(form)
            print('##################')
            print(user.image)
            # 1. user.preference => 리스트 자료형
            pre_list = user.preference
            # 2. 리스트 자료형 => 선호도 문자열 코드로 변환
            pre_code = make_pref_code(pre_list)
            # 3. 사용자 정보에 저장
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
    # 리스트 형태로 전달된 이전, 이후 선호도의 idx를 추출
    for li in pre:
        pre_idx.append(match.index(int(li)))
    for li in new:
        new_idx.append(match.index(int(li)))
    # 추출된 인덱스 부분을 수정한다.
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
        # 1. 유저의 이전 선호도를 변수에 저장
        pre_pref = request.user.preference
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        print('################################')
        if form.is_valid():
            # 2. form에 새로 기입된 선호도가 user정보에 반영
            user = form.save()
            print('------------------------')
            print(user.image)
            # 3. user.preference는 새로반영된 선호도
            new_pref = user.preference
            pre_code = user.preference_code
            # 4. 이전 선호도 초기화 => 새로운 선호도 반영
            new_code = update_code(pre_pref, new_pref, pre_code)
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


@login_required
@require_http_methods(['GET'])
def detail(request, user_pk):
    # 1. user id, nickname
    # 2. 작성한 글, 댓글, 추천
    article_user = User.objects.get(pk=user_pk)
    request_user = request.user
    # 사용자, 글쓴이 정보 구별
    if article_user == request_user:
        user = request_user
    else:
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
