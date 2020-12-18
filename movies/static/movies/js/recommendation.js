const movieCards = document.querySelectorAll('.movie-card')
movieCards.forEach(card => {
  card.addEventListener('mouseover', event => {
    console.log(event)
  })
})