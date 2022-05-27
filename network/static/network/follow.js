// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    /* Onclick event: follow|unfollow */
    const follow_button = document.getElementById("follow_button");
    follow_button.addEventListener("click", follow_profile());

});

/* Follow|Unfollow profile */
function follow_profile() {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;    
    const other_profile_name = document.getElementById("profile_name");

/*starting here: change everything from edit to follow */
    /* Send request to 'follow' in views.py */
    const request = new Request(
        '/follow',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            other_profile_name: other_profile_name
        })
    })
    .then(function(response) {
        console.log(response);
    });

    /* update follow_button */
    const follow_button = document.getElementById('follow_button');
    const current_followers = document.getElementById('followers');
    const follower_count = parseInt(current_likes.innerHTML);

    if (follow_button.innerHTML === "follow") {
        follow_button.innerHTML = "unfollow";
        current_followers.innerHTML = follower_count + 1;   
    } else if (follow_button.innerHTML === "unfollow") {
        follow_button.innerHTML = "follow";
        current_followers.innerHTML = follower_count - 1;   
    };
    
};