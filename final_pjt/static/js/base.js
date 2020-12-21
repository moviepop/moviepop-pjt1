searchImgs = document.querySelectorAll('.search-img')
searchBars = document.querySelectorAll('.search-bar')

function showSearchBar() {
  searchImgs.forEach(searchImg => searchImg.classList.toggle('d-none'))
  searchBars.forEach(searchBar => searchBar.classList.toggle('d-none'))

  // searchImg.setAttribute('class', 'd-none')
  // searchBar.removeAttribute('class', 'd-none')
}

window.onkeydown = function(event) {
  if(event.keyCode == 27) {
    searchImgs.forEach(searchImg => searchImg.removeAttribute('class', 'd-none'))
    searchBars.forEach(searchBar => searchBar.setAttribute('class', 'd-none'))
  }
}

searchImgs.forEach(searchImg => searchImg.addEventListener('click', showSearchBar))