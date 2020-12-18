const background = document.querySelector('#vote-data')
const voteData = background.innerText
const voteNum = parseFloat(voteData)
const backgroundImg = document.querySelector('.bg-img')
backgroundImg.setAttribute('style', `background: url(${ backgroundImg.dataset.backgroundimg }) no-repeat fixed 50% 50%/ 100% 100%`)
console.log(voteNum)
for (let step = 2; step < voteNum; step++) {
  const star = document.querySelector(`#star-${step}`)
  star.setAttribute('class', 'fa fa-star checked')
  console.log(step)
  step++
}