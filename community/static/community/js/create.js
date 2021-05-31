// 제목 입력 폼
const inputForm = document.querySelector('#inputForm')
const titleForm = inputForm.children[1]
titleForm.setAttribute('class', 'form-control')
titleForm.setAttribute('id', 'formTitle')
titleForm.setAttribute('placeholder', '제목을 입력해주세요.')
//hi
// 내용 입력 폼
const contentForm = inputForm.children[4]
contentForm.setAttribute('class', 'form-control')
contentForm.setAttribute('id', 'formContent')
contentForm.setAttribute('rows', '9')
contentForm.setAttribute('placeholder', '내용을 입력해주세요.')

// 평점 입력 폼
const scoreForm = inputForm.children[6].children[0]
scoreForm.setAttribute('class', 'dropdown form-control m-0 col-6')
scoreForm.setAttribute('style', 'display: inline-block;')
scoreForm.setAttribute('placeholder', '평점을 입력해주세요.')

// 사진 입력 폼
const imageForm = inputForm.children[6].children[1]
imageForm.setAttribute('class', 'btn m-0 p-0 col-5')
imageForm.setAttribute('style', 'display: inline-block;')

// 버튼 호버링
const aHover = document.querySelectorAll('#hover')