
var loginform = document.querySelector('#loginform')

loginform.addEventListener('submit', function(e){
    e.preventDefault()

    let form = new FormData(loginform)

    fetch('/api/user/login', {
        method: 'POST',
        body: form
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
            window.location.href ='/dashboard'
        }
    })
})

