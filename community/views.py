from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

from django.core.paginator import Paginator

from .models import Article, Comment
from movies.models import Movie
from .forms import CommentForm, ArticleMovieCreationForm, ArticleUpdateForm

from django.http import JsonResponse

from rest_framework.decorators import api_view

match = [28, 18, 53, 10749, 10751,
            878, 14, 12, 35, 80,
            9648, 16, 99, 36, 10752, 
            27, 10402, 37, 10770
        ]


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    ARTICLE_FOR_PAGE = 8
    paginator = Paginator(articles, ARTICLE_FOR_PAGE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    startpostnumber = 1
    endpostnumber = len(articles)
    try:
        if int(page):
            if len(articles):
                startpostnumber = (int(page) - 1) * ARTICLE_FOR_PAGE + 1
                if len(articles) <= int(page) * ARTICLE_FOR_PAGE:
                    endpostnumber = len(articles)
                else:
                    endpostnumber = int(page) * ARTICLE_FOR_PAGE
            else:
                startpostnumber = endpostnumber = 0
        else:
            startpostnumber = endpostnumber = 0
            
    except:
        if len(articles):
            startpostnumber = 1
            if len(articles) <= ARTICLE_FOR_PAGE:
                endpostnumber = len(articles)
            else:
                endpostnumber = ARTICLE_FOR_PAGE
        else:
            startpostnumber = endpostnumber = 0

    context = {
        'articles': articles,
        'posts': posts,
        'startpostnumber': startpostnumber,
        'endpostnumber': endpostnumber,
    }
    return render(request, 'community/index.html', context)


# 점수 계산 함수(장르선호도, 평점)
def cal(genre_pref, sco):
    # 몫을 계산하는 이유는 float은 string으로 전환되지 않기 때문이다.
    genre_pref = (genre_pref + sco) // 2
    return str(genre_pref)


# 평점을 선호코드에 반영하는 알고리즘
def score_pref_algorithm(score, code, genres):
    # index 추출
    genre_idx = []
    for genre in genres:
        genre_idx.append(match.index(int(genre.genre_id)))
    for idx in genre_idx:
        code = code[:idx] + cal(int(code[idx]), score) + code[idx+1:]
    # 영화 한편 시청시 관련없는 장르는 관심도 1씩 감소
    # 이유) 최근 시청한 영화에 가중치를 주기위해서
    for code_seq in range(19):
        if int(code[code_seq]) > 3 and code_seq not in genre_idx:
            code = code[:code_seq] + str(int(code[code_seq])-1) + code[code_seq+1:]
    return code


@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    if request.method == 'POST':
        form = ArticleMovieCreationForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.movie = Movie.objects.get(movie_id=movie_id)
            article.save()
            # 2-1. 유저정보에서 필요한 정보를 추출(평점, 선호코드)
            user_score = article.score
            user_pref_code = request.user.preference_code
            movie_genres = article.movie.genres.all()
            # 2-2. 평점 => 선호도 반영 알고리즘에 넣기
            new_pref_code = score_pref_algorithm(
                user_score,
                user_pref_code,
                movie_genres
            )
            request.user.preference_code = new_pref_code
            request.user.save()
            return redirect('community:detail', article.pk)
    else:
        form = ArticleMovieCreationForm()
        # 1-1. 폼에 입력
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'community/create.html', context)


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    movie = article.movie
    score_1 = '🌕' * (article.score//2)
    score_2 = '🌑' * (5-(article.score//2))
    if article.score % 2:
        score_half = '🌗'
        score_2 = '🌑' * ((5-(article.score//2))-1)
        score = score_1 + score_half + score_2
    else:
        score = score_1 + score_2
    
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
        'movie': movie,
        'score': score,
    }
    return render(request, 'community/detail.html', context)


# prev_score => new_score 반영함수
def update_cal(genre_pref, prev, new):
    genre_pref *= 2
    # 기존 점수가 높았는데 한동안 해당 장르를 안보다가 평점을 낮게 수정하면 오류발생
    # ex) 9점 부여 => 이후에 관심도 3까지 떨어졌을때 글의 평점을 2점으로 수정
    # (3 - 9 + 2) // 2 => -2 이므로 오류 발생 => 음수일 경우 0으로 변경
    if (genre_pref - prev + new) // 2 < 0:
        new_pref = 0
    else:
        new_pref = (genre_pref - prev + new) // 2
    return str(new_pref)


# 업데이트된 스코어 => 선호코드 반영 함수
def updated_score_pref(prev, new, code, genres):
    # 1. 기존 선호코드 idx 추출
    # 2. idx별 장르 선호도에 2를 곱한뒤 prev_score를 뺀다.
    # 3. new_score를 더한뒤 2로 나눈다.
    # 4. 몫을 반영한다.
    genre_idx = []
    for genre in genres:
        genre_idx.append(match.index(int(genre.genre_id)))
    for idx in genre_idx:
        code = code[:idx] + update_cal(int(code[idx]), prev, new) + code[idx+1:]
    return code


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # 기존 리뷰 스코어, 장르 담기
    prev_rvw_score = article.score
    movie_genres = article.movie.genres.all()
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleUpdateForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                # 새로운 리뷰 스코어, 사용자 선호코드
                new_rvw_score = article.score
                prev_user_pref = request.user.preference_code
                # 함수실행
                new_user_pref = updated_score_pref(
                    prev_rvw_score,
                    new_rvw_score,
                    prev_user_pref,
                    movie_genres
                )
                # 저장하기
                request.user.preference_code = new_user_pref
                request.user.save()
                return redirect('community:detail', article.pk)
        else:
            form = ArticleUpdateForm(instance=article)
    else:
        return redirect('community:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'community/update.html', context)


@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if request.user == article.user:
            article.delete()
            return redirect('community:index')
    return redirect('community:detail', article.pk)

def number_length(num):
    if len(str(num)) == 1:
        num = '0' + str(num)
    return num

def transtime(year, month, day, hour, minute):
    # 월별 마지막 일
    monthday = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # 윤달인 경우
    if (year % 4 == 0 and year % 100) or year % 400 == 0:
        monthday[2] = 29
    # 영국시간 => 한국시간
    hour += 9
    # 날짜가 달라질 경우
    if hour >= 24:
        day += 1
        hour -= 24
        if monthday[month] < day:
            day -= monthday[month]
            month += 1
            if month > 12:
                year += 1
                month -= 12

    # 기존 형식과 동일한 두자릿 수로 바꿔주기
    month = number_length(month)
    day = number_length(day)
    hour = number_length(hour)
    minute = number_length(minute)
    
    print(year, month, day, hour, minute)
    return f'{year}/{month}/{day} {hour}:{minute}'
        
        


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article_id = article.pk
            comment.save()
        # year, month, day, hour, minute
        created_at = transtime(comment.created_at.year, comment.created_at.month, comment.created_at.day, comment.created_at.hour, comment.created_at.minute)
        updated_at = transtime(comment.updated_at.year, comment.updated_at.month, comment.updated_at.day, comment.updated_at.hour, comment.updated_at.minute)        
        data = {
            'id': comment.id,
            'article_id': article.id,
            'username': comment.user.username,
            'content': comment.content,
            'count': article.comment_set.all().count(),
            'created_at': created_at,
            'updated_at': updated_at,
        }
        return JsonResponse(data)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            data = {
                'id': comment.id,
                'article_id': article.id,
                'username': comment.user.username,
                'content': comment.content,
                'count': article.comment_set.all().count(),
            }
            comment = comment.delete()
            return JsonResponse(data)


@require_POST
def like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        user = request.user
        print('a')

        if article.like_users.filter(pk=user.pk).exists():
            article.like_users.remove(user)
            liked = False
        else:
            article.like_users.add(user)
            liked = True
        
        like_status = {
            'liked': liked,
            'count': article.like_users.count(),
        }
        return JsonResponse(like_status)
    return redirect('accounts:login')


@api_view(['POST'])
def comments_update(request, article_pk, comment_pk):
    print(request.data)
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment_form = CommentForm(request.data, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article_id = article.pk
            comment.save()
        created_at = '댓글 생성 ' + transtime(comment.created_at.year, comment.created_at.month, comment.created_at.day, comment.created_at.hour, comment.created_at.minute)
        updated_at = '최근 수정 ' + transtime(comment.updated_at.year, comment.updated_at.month, comment.updated_at.day, comment.updated_at.hour, comment.updated_at.minute)        
        print(created_at, updated_at)
        data = {
            'id': comment.id,
            'article_id': article.id,
            'username': comment.user.username,
            'content': comment.content,
            'created_at': created_at,
            'updated_at': updated_at,
        }
        return JsonResponse(data)