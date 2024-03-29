// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    // Onclick event for each button 
    const buttons = document.getElementsByTagName("button");
    const length = buttons.length;
    for (var i = 0; i < length; i++) {
        buttons[i].onclick = function() {
            if (this.name === "edit") {
                edit(this.id);
            } else if (this.name === "like") {
                likePost(this.id);
            } else if (this.name === "follow") {
                followProfile();
            }
        }
    }
});

// Send LIKE or FOLLOW request to views.py 
function fetchData(route, data) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        route,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data.message);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
};

// Like|Unlike post 
function likePost(id) {

    // Fetch data 
    const post_id = id.slice(5);
    const route = '/like';
    const data = {id: post_id};
    fetchData(route, data);

    // Update like-button & like-counter     
    const current_button = document.getElementById(`like_${post_id}`);
    const current_likes = document.getElementById(`count_${post_id}`);
    const like_count = parseInt(current_likes.innerHTML);
    if (current_button.innerHTML === "💙") {
        current_button.innerHTML = "❤️";
        current_likes.innerHTML = like_count + 1;     
    } else if (current_button.innerHTML === "❤️") {
        current_button.innerHTML = "💙";
        current_likes.innerHTML = like_count - 1;    
    }
};

// Follow|Unfollow profile 
function followProfile() {

    // Fetch data 
    const other_profile_name = document.getElementById("profile_name").innerHTML.trim();
    const route = '/follow';
    const data = {other_profile_name: other_profile_name};
    fetchData(route, data);

    // Update follow_button 
    const follow_button = document.getElementById('follow_button');
    const current_followers = document.getElementById('followers');
    const follower_count = parseInt(current_followers.innerHTML);
    if (follow_button.innerHTML === "Follow") {
        follow_button.innerHTML = "Unfollow";
        current_followers.innerHTML = follower_count + 1;   
    } else if (follow_button.innerHTML === "Unfollow") {
        follow_button.innerHTML = "Follow";
        current_followers.innerHTML = follower_count - 1;   
    }
};

// Edit post 
function edit(id) {

    // Clear content_container & hide 'edit'-button 
    const post_id = id.slice(5);      
    const edit_button = document.getElementById(id);
    const content_container = document.getElementById(`content_${post_id}`);
    const content = content_container.innerHTML.trim();
    content_container.innerHTML = '';
    edit_button.style.display = "none";

    // Create textarea to edit 
    var edit_textarea = document.createElement('textarea');
    edit_textarea.setAttribute('id', 'edit_content');

    // Create save button 
    var save_button = document.createElement('button');
    save_button.className = 'btn btn-primary';
    save_button.setAttribute('id', 'save');
    save_button.innerHTML = 'Save';

    // Add new elements to DOM and populate textarea 
    content_container.append(edit_textarea);
    edit_button.parentNode.append(save_button);
    edit_textarea.innerHTML = content;

    // Event: save edited content 
    document.querySelector('#save').addEventListener('click', function() {
 
        // Fetch data
        const error_field = document.querySelector(`#error_msg_${post_id}`); 
        const post_content = document.querySelector('#edit_content').value; 
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(
            '/edit',
            {headers: {'X-CSRFToken': csrftoken}}
        );
        fetch(request, {
            method: 'PUT',
            mode: 'same-origin',
            body: JSON.stringify({
                content: post_content, 
                id: post_id
            })
        })
        .then(response =>  response.json().then(
                data => ({status: response.status, data: data})
            )
        )
        .then(result => {
            if (result.status === 202) {
                error_field.innerHTML = '';
                console.log("Success:", result.data.message);
                content_container.innerHTML = post_content;
                edit_button.style.display = "unset";
                edit_button.parentNode.removeChild(save_button);
            } else if (result.status === 400) {           
                error_field.innerHTML = " &bull; " + result.data.error;                
                console.log("Error:", result.data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });    
    });
};
