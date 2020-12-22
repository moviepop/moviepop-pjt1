searchImgs = document.querySelectorAll('.search-img')
searchBars = document.querySelectorAll('.search-bar')

function showSearchBar() {
  searchBars.forEach(searchBar => searchBar.classList.toggle('d-none'))
}

window.onkeydown = function(event) {
  if(event.keyCode == 27 && !searchBars.forEach(searchBar => searchBar.getAttribute('class', 'd-none'))) {
    searchBars.forEach(searchBar => searchBar.classList.toggle('d-none'))
  }
}

searchImgs.forEach(searchImg => searchImg.addEventListener('click', showSearchBar))