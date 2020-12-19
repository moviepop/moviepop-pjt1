import random
import requests
from datetime import datetime

from .models import Movie, Genre
from .serializers import MovieSerializer

from django.shortcuts import render, redirect

from bs4 import BeautifulSoup
from django.views.decorators.http import require_http_methods, require_GET, require_POST
# from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated



# Create your views here.
def index(request):
    return render(request, 'movies/index.html')
    
# 0. 유저의 선호도를 분석해서 최적의 영화를 추천하는 알고리즘
# 1. 유저의 선호도 정보를 받는다.(문자열 형태 ex) 3333333333333333333)
# 2. 선호도 정보와 장르id 매칭
# => 선호도 우선순위(한국인이 좋아하는 영화장르 통계조사 참고)
# 통계: 액션, 드라마, 스릴러, 로코, SF, 판타지, 코미디, 느와르, 미스터리, 다큐, 공포, 멜로, 뮤지컬
# DB: 액션(28), 드라마(18), 스릴러(53), 로맨스(10749), 가족(10751), SF(878), 판타지(14),
#     모험(12), 코미디(35), 범죄(80), 미스터리(9648), 애니메이션(16), 다큐멘터리(99), 
#     역사(36), 전쟁(10752), 공포(27), 음악(10402), 서부(37), TV영화(10770) 
# 3. DB순서대로 각 index의 숫자가 사용자의 선호도 (3621763... 인 사용자는 액션:3, 드라마:6...)
# 4. for문을 활용해 선호도가 높은 순서대로 숫자를 하나씩 뽑아낸뒤 해당 장르의 코드를 뽑아낸다.
# 5. 연관성 최우선 으로 추출
# 6. 기타 영화는 선호장르에서 랜덤으로 뽑아서 제공


def recommend_preference_algorithm(code):
    match = [28, 18, 53, 10749, 10751,
                878, 14, 12, 35, 80,
                9648, 16, 99, 36, 10752, 
                27, 10402, 37, 10770
            ]

    pref_list = []

    # 선호도 코드에서 장르 뽑아내는 알고리즘(선호장르 5개)
    # 5개를 뽑는 이유는 평균적으로 영화가 2개정도의 장로가 혼합
    # 10개 정도의 장르적 특징을 가지는 영화를 제공 (5 Combination 2)
    for cnt in range(9, 0, -1):
        for prefer in range(len(code)):
            if int(code[prefer]) == cnt:
                pref_list.append(match[prefer])
            if len(pref_list) > 4:
                break
        if len(pref_list) > 4:
            break

    prefer_movie = [[] for _ in range(5)]  
    # 관심도가 유사한 장르를 뽑아서 보여주기
    movie_list = Movie.objects.all()
    for movie in movie_list:
        num = 0
        for gen in movie.genres.all():
            if gen.genre_id in pref_list:
                num += 1
        if num > 0:
            prefer_movie[num-1].append(movie)

    show_movie = []
    # 뽑아낸 선호장르 영화리스트에서 12개 뽑아내기
    for num in range(4, -1, -1):
        length = len(prefer_movie[num])
        if length > 0 and len(show_movie) + length <= 12:
            for mo in prefer_movie[num]:
                show_movie.append(mo)
        elif length > 0:
            # 12개를 초과한다면 12개를 맞추도록 랜덤으로 추출
            randomlist = random.sample(prefer_movie[num], 12 - len(show_movie))
            for rand in randomlist:
                show_movie.append(rand)

    return show_movie


def preference(request):
    # 승인된 유저라면 해당유저의 정보를 바탕으로 추천
    if request.user.is_authenticated:
        pref_code = request.user.preference_code
        recommend_movie_list = recommend_preference_algorithm(pref_code)
        
    # 승인되지 않은 유저라면 로그인 요청하기
    else:
        return redirect('accounts:login')

    comment = '취향에 맞춰 추천해요!'
    context = {
        'recommend_movie_list': recommend_movie_list,
        'comment': comment,
    }
    return render(request, 'movies/recommendation.html', context)


def naver_link(request, title, date):
    
    BASE_URL = "http://search.naver.com/search.naver?query="
    url = BASE_URL + title + '%20' + str(date)
    print('###############')
    print(url)
    
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    try:
        search_link = soup.find("div", class_="title_area")
        detail_link = search_link.find("a")["href"]

        return redirect(detail_link)

    except AttributeError as e:
        url = BASE_URL + title
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            search_link = soup.find("div", class_="title_area")
            detail_link = search_link.find("a")["href"]
            print(e)
            return redirect(detail_link)
        
        except (TypeError, AttributeError):
            url = BASE_URL + '영화 ' + title
            print(url)
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
            try:
                search_link = soup.find("div", class_="title_area")
                detail_link = search_link.find("a")["href"]
                return redirect(detail_link)

            # 다음링크
            except AttributeError:
                DAUM_URL = "http://search.daum.net/search?q="
                url = DAUM_URL + title + str(date)
                req = requests.get(url)
                html = req.text
                soup = BeautifulSoup(html, "html.parser")
                try:
                    search_link = soup.find("div", class_="link_tit")
                    detail_link = search_link.find("a")["href"]
                    print(detail_link)
                    return redirect(detail_link)

                except AttributeError:
                    detail_link = BASE_URL + title
                    return redirect(detail_link)
                
    return redirect(detail_link)


def return_link(title, date):
    
    BASE_URL = "http://search.naver.com/search.naver?query="
    url = BASE_URL + title + '%20' + str(date)
    print('###############')
    print(url)
    
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    try:
        search_link = soup.find("div", class_="title_area")
        detail_link = search_link.find("a")["href"]
        req2 = requests.get(detail_link)
        html2 = req2.text
        soup2 = BeautifulSoup(html2, "html.parser")
        overview = soup2.find("p", class_="con_tx")

        return overview

    except AttributeError as e:
        url = BASE_URL + title
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            search_link = soup.find("div", class_="title_area")
            detail_link = search_link.find("a")["href"]
            req2 = requests.get(detail_link)
            html2 = req2.text
            soup2 = BeautifulSoup(html2, "html.parser")
            overview = soup2.find("p", class_="con_tx")

            return overview
        
        except (TypeError, AttributeError):
            url = BASE_URL + '영화 ' + title
            print(url)
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
            try:
                search_link = soup.find("div", class_="title_area")
                detail_link = search_link.find("a")["href"]
                req2 = requests.get(detail_link)
                html2 = req2.text
                soup2 = BeautifulSoup(html2, "html.parser")
                overview = soup2.find("p", class_="con_tx")

                return overview

            # 다음링크
            except AttributeError:
                DAUM_URL = "http://search.daum.net/search?q="
                url = DAUM_URL + title + str(date)
                req = requests.get(url)
                html = req.text
                soup = BeautifulSoup(html, "html.parser")
                try:
                    search_link = soup.find("div", class_="link_tit")
                    detail_link = search_link.find("a")["href"]
                    print(detail_link)
                    return detail_link

                except AttributeError:
                    detail_link = BASE_URL + title
                    return detail_link
                
    return detail_link


def detail(request, movie_id):
    # 0. reco.html페이지에서 버튼을 클릭시 movie.movie_id를 url에 담아서 보내기
    # 1. movie 인스턴스 생성
    # 2. movie.article.all() ? 로 전부 불러와서 article_list형태로 넘겨주기
    movie = Movie.objects.get(movie_id=movie_id)
    if len(movie.overview):
        link = ''
    else:
        link = return_link(movie.title, movie.release_date.year)
    # API 요청
    import requests
    BASE_URL = 'https://www.googleapis.com/youtube/v3/search?'
    API_KEY = os.environ.get('API_KEY')
    REQUEST_URL = BASE_URL + 'part=snippet' + f'&key={API_KEY}' + f'&q=movie%20{movie.original_title}%20trailer'  
    response = requests.get(REQUEST_URL)
    response = response.json()
    videoID = response["items"][0]["id"]["videoId"]
    print(videoID)

    VIDEO_URL = 'www.youtube.com/embed/' + videoID
    print(VIDEO_URL)

    articles = movie.article_set.all()
    context = {
        'movie': movie,
        'articles': articles,
        'link': link,
        'VIDEO_URL': VIDEO_URL,
    }
    return render(request, 'movies/movie_detail.html', context)


def search(request):
    keyword = str(request.GET.get('search'))
    # 1. 키워드 - 제목 필터링(title-str)
    title_related = Movie.objects.filter(title__contains=keyword)
    # 2. 키워드 - 줄거리 필터링(overview-str)
    overview_related = Movie.objects.filter(overview__contains=keyword)
    # 3. 키워드 - 개봉일 필터링(release_date.-str로 변환해서 사용?)
    date_related = Movie.objects.filter(release_date__contains=keyword)

    context = {
        'title_related': title_related,
        'overview_related': overview_related,
        'date_related': date_related,
    }
    return render(request, 'movies/search.html', context)


@api_view(['GET'])
def search_title(request, searchword):
    movies = Movie.objects.filter(title__contains=searchword)
    serializer = MovieSerializer(movies, many=True)

    return Response(data=serializer.data)


# 규칙 1. comment로 멘트 넘겨주기(어떤 알고리즘인지 표시)
# 규칙 2. 영화목록은 recommend_movie_list 로 넘겨주기
def released_thisyear(request):
    # 현재년도 가져오기
    this_year = datetime.now().year
    movies = Movie.objects.filter(release_date__contains=this_year)
    movie_list = []
    random_list = []
    # 3개씩 끊어서 보여주기(1~2개 단위로 끊기지 않게)
    if len(movies) % 3:
        random_list = random.sample(range(len(movies)), len(movies) - (len(movies) % 3))
    else:
        random_list = random.sample(range(len(movies)), len(movies))
    for num in random_list:
        movie_list.append(movies[num])
    comment = '올해 개봉한 영화에요!'
    context = {
        'recommend_movie_list': movie_list,
        'comment': comment,
    }
    return render(request, 'movies/recommendation.html', context)
    

# 장르별로 영화를 추출해 랜덤으로 12개씩 반환하는 함수
def collect_genre_movie(genre_list):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        for gen in movie.genres.all():
            if gen.genre_id in genre_list:
                movie_list.append(movie)
                break
    movie_list = random.sample(movie_list, 12)
    return movie_list


# 혼자보기 좋은영화 : 액션, SF, 다큐, 미스터리, 서부, 범죄, 전쟁
def alone(request):
    genre_alone = [28, 878, 99, 9648, 37, 80, 10752]
    movie_list = collect_genre_movie(genre_alone)
    comment = '혼자있다면 이 영화를 추천해요!'
    context = {
        'recommend_movie_list': movie_list,
        'comment': comment,
    }
    return render(request, 'movies/recommendation.html', context)


# 커플 : 로맨스, 코미디, 공포, 드라마, 스릴러, 음악
def couple(request):
    genre_couple = [10749, 35, 27, 10402, 18, 53]
    movie_list = collect_genre_movie(genre_couple)
    comment = '연인과 함께 있다면?'
    context = {
        'recommend_movie_list': movie_list,
        'comment': comment,
    }
    return render(request, 'movies/recommendation.html', context)


# 가족 : 드라마, 코미디, 가족, TV영화, 애니메이션, 판타지, 모험, 역사
def together(request):
    genre_together = [18, 35, 10751, 10770, 16, 14, 12, 36]
    movie_list = collect_genre_movie(genre_together)
    comment = '가족과 함께라면 이 영화를 추천해요!'
    context = {
        'recommend_movie_list': movie_list,
        'comment': comment,
    }
    return render(request, 'movies/recommendation.html', context)