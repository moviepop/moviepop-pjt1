//const BASE_URL = 'http://127.0.0.1:8000'
const input = document.querySelector('#movie-input')
const button = document.getElementById('movie-button')
const movielist = document.querySelector('#movie-box')
// console.log(button)

// 영화 데이터 받아오기를 위한 ajax 요청

function addMovie(movie) {
  // console.log(movie.title)
  // console.log(movie.movie_id)
  const movieId = movie.movie_id
  const title = movie.title
  const a = document.createElement('a')
  a.innerText = title
  a.setAttribute('style', 'color: rgba(255, 255, 255, 1);')
  a.setAttribute('class', 'btn')
  a.setAttribute('href', `/community/create/${movieId}/`)
  movielist.appendChild(a)
}

function movieData () {
  const content = input.value
  axios.get(`/movies/search_title/${content}`)
    .then(res => {
      for (let movie in res.data) {
        addMovie(res.data[movie])
      }
    })
    .catch(err => {
      console.error(err)
    })
}

button.addEventListener('click', movieData)
input.addEventListener('keypress', function (event) {
  if (event.code === 'Enter') {
    movieData()
  }
})

const mouseoverFunc = function (event) {
    event.path[2].children[0].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[1].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[2].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[3].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[4].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[5].setAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
}

const mouseoutFunc = function (event) {
    event.path[2].children[0].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[1].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[2].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[3].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[4].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
    event.path[2].children[5].removeAttribute('style', 'background-color: rgba(255, 255, 255, 0.3);')
}

const movieReview = document.querySelectorAll('.review-movie')
movieReview.forEach(movie => {
  movie.addEventListener('mouseover', mouseoverFunc)
  movie.addEventListener('mouseout', mouseoutFunc)
})

const movieTitle = document.querySelectorAll('.review-title')
movieTitle.forEach(title => {
  title.addEventListener('mouseover', mouseoverFunc)
  title.addEventListener('mouseout', mouseoutFunc)
})

const movieReviewUser = document.querySelectorAll('.review-user')
movieReviewUser.forEach(user => {
  user.addEventListener('mouseover', mouseoverFunc)
  user.addEventListener('mouseout', mouseoutFunc)
})

const pageBtns = document.querySelectorAll('.page-btn')
pageBtns.forEach(btn => {
  btn.addEventListener('mouseover', event => {
    try {
      const pageBtn = event.path[0].children[0].children[1]
      //console.log(pageBtn)
      //console.log(event.path[0].children[0])
      pageBtn.removeAttribute('fill', '#c81912')
      pageBtn.setAttribute('fill', '#fdba9a')
    } catch (e) {
      //console.log('버튼위치가 잘못되었습니다.(예외처리)')
    }
  })
  btn.addEventListener('mouseout', event => {
    try {
    const pageBtn = event.path[0].children[0].children[1]
    pageBtn.removeAttribute('fill', '#fdba9a')
    pageBtn.setAttribute('fill', '#c81912')
    } catch (e) {
      //console.log('버튼위치가 잘못되었습니다.(예외처리)')
    }
  })
})

