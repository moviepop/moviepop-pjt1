from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from allauth.socialaccount.forms import SignupForm
from multiselectfield import MultiSelectField
from django.db import models


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('nickname', 'preference', )

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('nickname', 'preference', )


class MyCustomSocialSignupForm(SignupForm):
    GENRES = (
        (12, '모험'),
        (14, '판타지'),
        (16, '애니메이션'),
        (18, '드라마'),
        (27, '공포'),
        (28, '액션'),
        (35, '코미디'),
        (36, '역사'),
        (37, '서부'),
        (53, '스릴러'),
        (80, '범죄'),
        (99, '다큐멘터리'),
        (878, 'SF'),
        (9648, '미스터리'),
        (10402, '음악'),
        (10749, '로맨스'),
        (10751, '가족'),
        (10752, '전쟁'),
        (10770, 'TV영화')
    )
    preference = MultiSelectField(choices = GENRES, verbose_name="선호하는 영화 장르")
    preference_code = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10, verbose_name="닉네임")

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.preference = self.cleaned_data['preference']
        user.preference_code = '3333333333333333333'
        user.nickname = self.cleaned_data['nickname']
        user.save()
        return user