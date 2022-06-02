// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    // Onclick event for each button 
    const buttons = document.getElementsByTagName("button");
    const length = buttons.length;
    for (var i = 0; i < length; i++) {
        buttons[i].onclick = function() {
            if (this.name === "edit") {
                prepareEdit(this.id);
            } else if (this.name === "like") {
                likePost(this.id);
            } else if (this.name === "follow") {
                followProfile();
            }
        }
    }
});

// Send request to views.py 
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
    })/*
    .then((response) => response.json()) 
    .then((responseData) => {
        console.log(responseData);
        return responseData;
    });*/
    .then((response) => {
/*TODO: improve code below */
        status_code = response.status;
        if((status_code == 202) & (route == '/edit')) {
            const content_container = document.getElementById(`content_${data.id}`);
            const edit_button = document.getElementById(`edit_${data.id}`);
            content_container.innerHTML = data.content;
            edit_button.style.display = "unset";
            save_button = document.getElementById('save');
            edit_button.parentNode.removeChild(save_button)    
        } else if (status_code == 400) {
            alert("Too long: Maximum length of 440 characters.")
        }
    })

};

// Replaces posts content 
function prepareEdit(id) {

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
        const post_content = document.querySelector('#edit_content').value;
        const route = '/edit';    
        const data = {content: post_content, id: post_id};
        fetchData(route, data)

        /*
        .then(result => {
            console.log(result)
            content_container.innerHTML = post_content;
            edit_button.style.display = "unset";
            edit_button.parentNode.removeChild(save_button)    
        })*/

    })
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
