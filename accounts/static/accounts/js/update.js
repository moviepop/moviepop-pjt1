const preferenceLists = document.querySelectorAll('#preference li')
preferenceLists.forEach((list, idx) => {
  const spanTag = document.createElement('span')
  spanTag.setAttribute('id', `id-${idx}`)
  spanTag.innerHTML = list.innerHTML
  list.parentNode.replaceChild(spanTag, list)
  const labelTag = spanTag.firstChild
  console.log(labelTag)
  const inputTag = labelTag.firstChild
  console.log(inputTag)
  inputTag.setAttribute('class', 'input-check')
})