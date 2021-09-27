
var regform = document.querySelector('#editform')

editform.addEventListener('submit', function(e){
    e.preventDefault()

    let form = new FormData(editform)
    let file = new FileSystem(editform)

    fetch('/api/save', {
        method: 'POST',
        body: form,
        body: file
    })
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
        if (data['status'] == 400){
            let allErrors = document.querySelectorAll(".errors")
            for (const error of allErrors) {
                let errorId = error.getAttribute('id');
                if (errorId in data['errors']) {
                    error.innerText = data['errors'][errorId]
                }
            }
        } else if (data['status'] === 200){
            window.location.href = '/<int:id>/edit'
        }
    })
})