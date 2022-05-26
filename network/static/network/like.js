// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {
    
    const like_buttons = document.getElementsByName("like");
    like_buttons.forEach(item => {
        item.addEventListener("click", () => {
                like_post(item.id);
            })
        }
    );
    
});

/* Like|Unlike post */
function like_post(id) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;    
    const post_id = id.slice(5);

    /* Send request to 'like' in views.py */
    const request = new Request(
        '/like',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            id: post_id
        })
    })
    .then(function(response) {
        console.log(response);
    });

    const current_button = document.getElementById(`like_${post_id}`);
    const current_likes = document.getElementById(`count_${post_id}`);
    const likecount = parseInt(current_likes.innerHTML);    

    /* update like-button & like-counter */
    if (current_button.innerHTML === "like") {
        current_button.innerHTML = "unlike";
        current_likes.innerHTML = likecount + 1;     
    } else if (current_button.innerHTML === "unlike") {
        current_button.innerHTML = "like";
        current_likes.innerHTML = likecount - 1;    
    };

};