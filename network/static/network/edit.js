// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#posts_frame').addEventListener('click', edit);

});

function edit(event) {
    const element = event.target;
    const parent = element.parentElement;
    const content = element.previousElementSibling.innerHTML.trim();
    parent.innerHTML = '';

    /* Create Edit Content Textfield */
    var edit_textarea = document.createElement('textarea');
    edit_textarea.setAttribute('id', 'edit_content');

    /* Create Submit Editing Button */
    var edit_button = document.createElement('button');
    edit_button.type = 'submit';
    edit_button.className = 'btn btn-sm btn-outline-primary';
    edit_button.setAttribute('id', 'edit');
    edit_button.innerHTML = 'Save';

    parent.append(edit_textarea, edit_button);
    edit_textarea.innerHTML = content;

    console.log(parent);


/* change request.POST methods at index to initial_post and edit */
/* then only save content, not timestamp and likes */

    fetch('/', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#edit_content').value,
            csrfmiddlewaretoken: '{{ csrf_token }}' 
        })
    })
    .then(response => response.json())
    .then(result => {
  
        // Print result & load mailbox
        console.log(result);
    })

};