// 제목 입력 폼
const inputForm = document.querySelector('#updateInputForm')
// console.log(inputForm)
const titleForm = inputForm.children[1]
// console.log(titleForm)
titleForm.setAttribute('class', 'form-control')
titleForm.setAttribute('id', 'formTitle')
titleForm.setAttribute('placeholder', '제목을 입력해주세요.')

// 내용 입력 폼
const contentForm = inputForm.children[4]
contentForm.setAttribute('class', 'form-control')
contentForm.setAttribute('id', 'formContent')
contentForm.setAttribute('rows', '9')
contentForm.setAttribute('placeholder', '내용을 입력해주세요.')

// 평점 입력 폼
const scoreForm = inputForm.children[6]
scoreForm.setAttribute('class', 'form-control m-0')
scoreForm.setAttribute('style', 'width: 232.5px; display: inline-block;')
scoreForm.setAttribute('placeholder', '평점을 입력해주세요.')


// 버튼 호버링
const aHover = document.querySelector('#a-hover')
const bHover = document.querySelector('#b-hover')

// a 버튼
const mouseoverFunca = function (event) {
  console.log(event)
  aHover.setAttribute('style', 'color: rgba(246, 75, 60, 1);')
}
const mouseoutFunca = function (event) {
  //console.log(event)
  aHover.removeAttribute('style', 'color: rgba(246, 75, 60, 1);')
}

aHover.addEventListener('mouseover', mouseoverFunca)
aHover.addEventListener('mouseout', mouseoutFunca)

// b버튼
const mouseoverFuncb = function (event) {
  console.log(event)
  bHover.setAttribute('style', 'color: rgba(246, 75, 60, 1);')
}
const mouseoutFuncb = function (event) {
  //console.log(event)
  bHover.removeAttribute('style', 'color: rgba(246, 75, 60, 1);')
}

bHover.addEventListener('mouseover', mouseoverFuncb)
bHover.addEventListener('mouseout', mouseoutFuncb)
