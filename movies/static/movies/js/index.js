const searchForm = document.getElementById('navSearchForm')
searchForm.style.display = 'none';

const mouseOut = function() {
  const ment = document.getElementById('ment')
  ment.innerText = ""
}

// 사용자 맞춤 추천 영화
const selfPreference = document.getElementById('selfPreference')
selfPreference.addEventListener('click', function() {
  location.href = "/movies/preference/"
})
selfPreference.addEventListener('mouseover', function() {
  const ment = document.getElementById('ment')
  ment.innerText = "사용자 맞춤 추천 영화"
})
selfPreference.addEventListener('mouseout', mouseOut)

// 올해 개봉한 영화
const newMovies = document.getElementById('newMovies')
newMovies.addEventListener('click', function() {
  location.href = "/movies/released_thisyear/"
})
newMovies.addEventListener('mouseover', function() {
  const ment = document.getElementById('ment')
  ment.innerText = "올해 개봉한 영화"
})
newMovies.addEventListener('mouseout', mouseOut)

// 혼자 보기 좋은 영화
const alonePreference = document.getElementById('alonePreference')
alonePreference.addEventListener('click', function() {
  location.href = "/movies/alone/"
})
alonePreference.addEventListener('mouseover', function() {
  const ment = document.getElementById('ment')
  ment.innerText = "혼자 보기 좋은 영화"
})
alonePreference.addEventListener('mouseout', mouseOut)

// 연인과 함께 보기 좋은 영화
const couplePreference = document.getElementById('couplePreference')
couplePreference.addEventListener('click', function() {
  location.href = "/movies/couple/"
})
couplePreference.addEventListener('mouseover', function() {
  const ment = document.getElementById('ment')
  ment.innerText = "연인과 함께 보기 좋은 영화"
})
couplePreference.addEventListener('mouseout', mouseOut)

// 가족과 함께 보기 좋은 영화
const familyPreference = document.getElementById('familyPreference')
familyPreference.addEventListener('click', function() {
  location.href = "/movies/together/"
})
familyPreference.addEventListener('mouseover', function() {
  const ment = document.getElementById('ment')
  ment.innerText = "가족과 함께 보기 좋은 영화"
})
familyPreference.addEventListener('mouseout', mouseOut)