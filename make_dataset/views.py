import requests
from django.shortcuts import render
from movies.models import Movie, Genre

# Create your views here.
# Create your views here.

BASE_URL = 'https://api.themoviedb.org/3/'
API_KEY = 'api_key=abddd3146f211e9145e4b82871c4ed45'
MOVIE_URL = BASE_URL + 'movie/top_rated?' + API_KEY + '&language=ko-KR'
GENRE_URL = BASE_URL + 'genre/movie/list?' + API_KEY + '&language=ko-KR'

# 장르데이터를 받는다.
# movie데이터를 받는다.
# 무비 데이터를 받기위해서는 for 반복문을 통해 반복을 시행
# 페이지 반복문
# response의 반복문(20개)
# response의 각 객체별로 데이터를 추출해 movie인스턴스에 담는다.


def update_dataset(request):
    movietitles = [] 
    # 장르 항목 요청
    response_gens = requests.get(GENRE_URL)
    response_gens = response_gens.json()
    print(GENRE_URL)
    # print(response_gens, '####')

    for gen in response_gens['genres']:
        print(gen)
        genre_instance = Genre()
        genre_instance.genre_id = gen['id']
        genre_instance.name = gen['name']
        genre_instance.save()
    

    # 요청 보내기 (1, 25페이지 까지)
    for page in range(1, 25):
        REQ_URL = MOVIE_URL + f'&page={page}'
        print(REQ_URL)
        response = requests.get(REQ_URL)
        response = response.json()

        # response에서 20개의 자료 추출하기
        for num in range(0, 20):
            # movie 인스턴스 호출하고 DB에 저장하기
            movie = Movie()
            movie.movie_id = response['results'][num]['id']
            movie.popularity = response['results'][num]['popularity']
            movie.vote_count = response['results'][num]['vote_count']
            movie.poster_path = response['results'][num]['poster_path']
            movie.backdrop_path = response['results'][num]['backdrop_path']
            movie.original_language = response['results'][num]['original_language']
            movie.original_title = response['results'][num]['original_title']
            movie.title = response['results'][num]['title']
            movie.vote_average = response['results'][num]['vote_average']
            movie.overview = response['results'][num]['overview']
            movie.release_date = response['results'][num]['release_date']

            # # movie detail api요청 및 저장(오래걸림)
            # movie_id = movie.movie_id
            # DETAIL_URL = BASE_URL + f'movie/{movie_id}?' + API_KEY + '&language=ko-KR'
            # detail_res = requests.get(DETAIL_URL).json()
            # # runtime 데이터 저장
            # movie.runtime = detail_res['runtime']
            movie.save()

            # # production country data DB에 저장
            # for country_data in detail_res['production_countries']:
            #     country = Country()
            #     country.iso = country_data['iso_3166_1']
            #     country.name = country_data['name']
            #     country.save()

            # M2M 관계 중계테이블에 저장(영화-국가)
            # for country_data in detail_res['production_countries']:
            #     iso = country_data['iso_3166_1']
            #     country = Country.objects.get(iso=iso)
            #     country.movies.add(movie)

            # M2M 관계 중계테이블에 저장(영화-장르)
            for genid in response['results'][num]['genre_ids']:
                # print(genid)
                genre = Genre.objects.get(genre_id=genid)
                genre.movies.add(movie)

            # 제대로 받아지는지 확인한다.
            print(movie.title)
            # movietitles에 담아서 template에 출력해보자.
            movietitles.append(movie.title)

    # 완료시 success문구 출력
    print('success')

    context = {
        'movietitles': movietitles,
    }
    return render(request, 'make_dataset/update_dataset.html', context)