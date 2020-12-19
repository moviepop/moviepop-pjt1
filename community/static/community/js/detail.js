const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// 좋아요 기능
const like_form = document.querySelector('.like-form')
like_form.addEventListener('submit', function (event) {
  event.preventDefault()
  const articleId = event.target.dataset.articleId

  axios.post(`/community/${articleId}/like/`, {}, {
    headers: {
        'X-CSRFToken': csrftoken
    }
  })
  .then(res => {
    const count = res.data.count
    const liked = res.data.liked

    const likeIcon = document.querySelector(`#like-${articleId}`)
    const likeCount = document.querySelector(`#like-count-${articleId}`)

    likeCount.innerText = `${count}명이 이 글을 추천합니다.`

    if (liked) {
      likeIcon.classList.remove('far')
      likeIcon.classList.add('fas')
    } else {
      likeIcon.classList.remove('fas')
      likeIcon.classList.add('far')
    }
  })
})

// 댓글 삭제
const commentDeleteButtons = document.querySelectorAll('.delete-comment')      
commentDeleteButtons.forEach(btn => {
  btn.addEventListener('click', event => {
    const BASE_URI = event.target.baseURI
    const commentId = btn.dataset.id

    axios.post(`${BASE_URI}comments/${commentId}/delete/`, {}, {
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .then(res => {
        const articleId = res.data.article_id
        const comment = event.path[3]
        comment.parentNode.removeChild(comment)
        const count = res.data.count            
        const commentCount = document.querySelector(`#comment-count-${ articleId }`)
        if (count-1 > 0) {
          commentCount.innerText = `(${count-1})`
        } else {
          commentCount.innerText = '(0)'
        }
      })
      .catch(err => {
        console.log(err)
      })
  })
})
// 댓글 생성
const commentForms = document.querySelectorAll(".comment-form")
commentForms.forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault()
    
    const data = new FormData(event.target)

    axios.post(event.target.action, data)
      .then(res => {
        const comment = res.data
        const commentList = document.querySelector(
          `#comment-list-${ comment.article_id }`
        )
        const newComment = 
        `	<div>
            <div class="d-flex justify-content-between">
              <div>
                <strong class="base-title-font h4">${ comment.username }</strong>
                <i class="icon-to-button far fa-trash-alt delete-comment icon-to-button-delete mx-1" id="delete-${ comment.id }" data-id="${ comment.id }"></i>
                <i id="update-${ comment.id }" class="fas fa-edit icon-to-button-update update-comment ml-1" data-id="${ comment.id }"></i>
              </div>
              <div class="" style="font-size: 0.8rem;">
                <div>
                  댓글 생성 ${ comment.created_at }
                </div>
                <div>
                  최근 수정 ${ comment.updated_at }
                </div>
              </div>
            </div>
            <div>
              <span class="base-font" style="font-size: large">${ comment.content }</span>
            </div>
            </br>
          </div>
          `
        commentList.insertAdjacentHTML('beforeEnd', newComment)
        event.target.reset()
        const count = res.data.count
        const articleId = res.data.article_id            
        const commentCount = document.querySelector(`#comment-count-${ articleId }`)
        if (count > 0) {
          commentCount.innerText = `(${count})`
        } else {
          commentCount.innerText = '(0)'
        }

        // 댓글 생성 후 바로 지울 때
        const commentDeleteButton = document.querySelector(`#delete-${ comment.id }`)
        commentDeleteButton.addEventListener('click', event => {
          axios.post(`/community/${ comment.article_id }/comments/${ comment.id }/delete/`, {}, {
            headers: 
              { 'X-CSRFToken': csrftoken }
          })
            .then(res => {
              const comment = event.path[3]
              comment.parentNode.removeChild(comment)

              if (count-1 > 0) {
                commentCount.innerText = `(${count-1})`
              } else {
                commentCount.innerText = '(0)'                  }
            })
            .catch(err => {
              console.log(err)
              })
            })
        // 댓글 생성 후 바로 수정할 때
        const updateButton = document.querySelector(`#update-${ comment.id }`)
        updateButton.addEventListener('click', event => {
          const parentNode = event.target.parentElement.parentNode.nextSibling.nextSibling
          const text = parentNode.children[0]
          const input = document.createElement('input')
          input.value = text.innerText

          input.classList.add(`commentUpdateForm-${ comment.id }`)
          parentNode.replaceChild(input, text)
          const updateParrent = event.path[0].parentNode
          const updateButton = event.path[0]
          const updateCompleteButton = document.createElement('i')
          const deleteButton = event.path[1].children[1]
          deleteButton.setAttribute('style', 'display: None;')

          updateCompleteButton.setAttribute('class', `commentUpdateButton-${ comment.id }`)
          updateCompleteButton.classList.add('fas')
          updateCompleteButton.classList.add('fa-edit')
          updateCompleteButton.classList.add('icon-to-button-update')
          const timeZone = event.path[2].children[1]
          timeZone.setAttribute('style', 'display: None;')

          updateCompleteButton.addEventListener('click', event => {
            const baseURI = event.path[2].baseURI
            const content = input.value
            const data = { content }
            axios.post(`${ baseURI }comments/${ comment.id }/update/`, data, {
              headers:
                { 'X-CSRFToken': csrftoken}
            })
            .then(res => {
              console.log(res)
              const temp = document.querySelector(`.commentUpdateForm-${ comment.id }`)
              const newText = document.createElement('span')
              deleteButton.setAttribute('style', 'display: True;')
              newText.innerText = temp.value
              parentNode.replaceChild(newText, temp)
              event.path[2].children[1].children[0].firstChild.data = res.data.created_at
              event.path[2].children[1].children[1].firstChild.data = res.data.updated_at
              console.log(timeZone)
              timeZone.removeAttribute('style', 'display: None;')
              timeZone.setAttribute('style', 'font-size: 0.8rem;')
              updateParrent.replaceChild(updateButton, updateCompleteButton)
            })
            .catch(err => {
              console.log(err)
            })
          })
          updateParrent.replaceChild(updateCompleteButton, updateButton)
        })
        
        })
      .catch(err => {
        console.log(err)
      })
    })
  })
// 댓글 수정
const updateButtons = document.querySelectorAll(".update-comment")
updateButtons.forEach(button => {
  button.addEventListener('click', event => {
    console.log(event.target)
    const parentNode = event.target.parentElement.parentNode.nextSibling.nextSibling
    console.log('3###')
    console.log(parentNode)
    // const text = parentNode.children[0]
    const text = parentNode.querySelector('span')
    const input = document.createElement('input')
    input.value = text.innerText
    const commentId = button.dataset.id

    input.classList.add(`commentUpdateForm-${ commentId }`)
    parentNode.replaceChild(input, text)
    const updateParrent = event.path[0].parentNode
    const updateButton = event.path[0]
    const updateCompleteButton = document.createElement('i')
    const deleteButton = event.path[1].children[1]
    deleteButton.setAttribute('style', 'display: None;')
    updateCompleteButton.classList.add(`commentUpdateButton-${ commentId }`)
    updateCompleteButton.classList.add('fas')
    updateCompleteButton.classList.add('fa-edit')
    updateCompleteButton.classList.add('icon-to-button-update')
    const timeZone = event.path[2].children[1]
    timeZone.setAttribute('style', 'display: None;')

    updateCompleteButton.addEventListener('click', event => {
      const baseURI = event.target.baseURI
      const content = input.value
      data = { content }
      axios.post(`${ baseURI }comments/${ commentId }/update/`, data, {
          headers: 
            { 'X-CSRFToken': csrftoken }
        })
        .then(res => {
          console.log(res)
          const temp = document.querySelector(`.commentUpdateForm-${ commentId }`)
          const newText = document.createElement('span')
          deleteButton.setAttribute('style', 'display: True;')
          newText.innerText = temp.value
          parentNode.replaceChild(newText, temp)
          event.path[2].children[1].children[0].firstChild.data = res.data.created_at
          event.path[2].children[1].children[1].firstChild.data = res.data.updated_at
          timeZone.removeAttribute('style', 'display: None;')
          timeZone.setAttribute('style', 'font-size: 0.8rem;')

          updateParrent.replaceChild(updateButton, updateCompleteButton)
        })
        .catch(err => {
          console.log(err)
        })
    })
    console.log(parentNode)
    updateParrent.replaceChild(updateCompleteButton, updateButton)
  })
})
