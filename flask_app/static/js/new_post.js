$(document).ready(function() {
    $('#summernote').summernote();
});

// function uploadImage(image) {
//     var data = new FormData();
//     data.append("image", image);
//     $.ajax({
//         url: 'Your url to deal with your image',
//         cache: false,
//         contentType: false,
//         processData: false,
//         data: data,
//         type: "post",
//         success: function(url) {
//             var image = $('<img>').attr('src', 'http://' + url);
//             $('#summernote').summernote("insertNode", image[0]);
//         },
//         error: function(data) {
//             console.log(data);
//         }
//     });
// }



// var postform = document.querySelector('#postform')

// postform.addEventListener('submit', function(e){
//     e.preventDefault()

//     let form = new FormData(postform)

//     fetch('/api/post', {
//         method: 'POST',
//         body: form
//     })
//     .then(resp => resp.json())
//     .then(data => {
//         console.log(data);
//         if (data['status'] == 400){
//             let allErrors = document.querySelectorAll(".errors")
//             for (const error of allErrors) {
//                 let errorId = error.getAttribute('id');
//                 if (errorId in data['errors']) {
//                     error.innerText = data['errors'][errorId]
//                 }
//             }
//         } else if (data['status'] === 200){
//             window.location.href ='/dashboard'
//         }
//     })
// })