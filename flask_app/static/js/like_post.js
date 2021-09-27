var like = document.querySelector('#like')

like.addEventListener('click', function(){

fetch('/api/<int:id>/like')
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
        if (data['status'] == 200){
        window.location.href = '/dashboard'
        }
    })
})
