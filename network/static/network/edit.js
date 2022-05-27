// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    /* Onclick event for each edit-buttons */
    /* For-loop loops faster than forEach */
    const edit_buttons = document.getElementsByName("edit");
    const length = edit_buttons.length;
    for (var i = 0; i < length; i += 1) {
        edit_buttons[i].onclick = function() {
            prepare_edit(this.id);
        };
    };
    
});

/* Replaces posts content */
function prepare_edit(id) {

    const element = document.getElementById(id);
    const content_container = element.previousElementSibling;
    const content = element.previousElementSibling.innerHTML.trim();

    /* Clear content_container & hide 'edit'-button */
    content_container.innerHTML = '';
    element.style.display="none";

    /* Create Content Textfield */
    var edit_textarea = document.createElement('textarea');
    edit_textarea.setAttribute('id', 'edit_content');

    /* Create Save Button */
    var save_button = document.createElement('button');
    save_button.className = 'btn btn-sm btn-outline-primary';
    save_button.setAttribute('id', 'save');
    save_button.innerHTML = 'Save';

    /* Add new elements to content-container(DIV) and populate textarea */
    content_container.append(edit_textarea, save_button);
    edit_textarea.innerHTML = content;

    /* Event: save edited content */
    document.querySelector('#save').addEventListener('click', save_edit);

};

/* 'Save' edited content */
function save_edit(event) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;    
    const post_id = document.querySelector('#edit_content').parentNode.id.slice(8);
    const post_content = document.querySelector('#edit_content').value;

    /* Send request to 'edit' in views.py */
    const request = new Request(
        '/edit',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            id: post_id,
            content: post_content
        })
    })
    .then(function(response) {
        console.log(response);
    });

    /* Replace content */
    document.querySelector(`#content_${post_id}`).innerHTML = post_content;

    /* Display 'Edit'-button */
    document.getElementById(`edit_${post_id}`).style.display="unset";

    /* Prevent submission */
    event.preventDefault();

};
