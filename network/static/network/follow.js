// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    /* Onclick event: follow|unfollow */
    document.getElementById("follow_button").addEventListener("click", follow_profile);
    
});

/* Follow|Unfollow profile */
function follow_profile() {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;    
    const other_profile_name = document.getElementById("profile_name").innerHTML.trim();

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
    const follower_count = parseInt(current_followers.innerHTML);

    console.log(follow_button)

    if (follow_button.innerHTML === "Follow") {
        follow_button.innerHTML = "Unfollow";
        current_followers.innerHTML = follower_count + 1;   
    } else if (follow_button.innerHTML === "Unfollow") {
        follow_button.innerHTML = "Follow";
        current_followers.innerHTML = follower_count - 1;   
    };
    
};