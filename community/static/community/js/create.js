// 제목 입력 폼
const inputForm = document.querySelector('#inputForm')
console.log(inputForm)
const titleForm = inputForm.children[1]
console.log(titleForm)
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
const aHover = document.querySelectorAll('#hover')