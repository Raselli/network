// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

/* TODO: */
    /* ? other solution ? */
    /* more specific: name=edit */
    const buttons = document.getElementsByTagName("button");
    for (var i = 0; i < buttons.length; i += 1) {
        buttons[i].onclick = function() {
            edit(this.id);
        };
    };
});


/* replaces content of div with POST-Form */
function edit(event) {

    var element = document.getElementById(event);
    const parent = element.parentElement;
    const content = element.previousElementSibling.innerHTML.trim();
    parent.innerHTML = '';
    var form = document.createElement('form');
/* TODO */
    /* instead of inner html, could also fetch PUT */
    form.setAttribute("method", "POST");
    form.setAttribute("action", "/");
    parent.append(form);

/*
    var csrftoken = document.createElement('input');
    csrftoken.setAttribute('type','hidden');
    csrftoken.setAttribute('value', getCookie('csrftoken'));
*/


    /* Create Edit Content Textfield */
    var edit_textarea = document.createElement('textarea');
    edit_textarea.setAttribute('name', 'content');
    edit_textarea.setAttribute('id', 'edit_content');

    /* Create Submit Editing Button */
    var edit_button = document.createElement('button');
    edit_button.type = 'submit';
    edit_button.className = 'btn btn-sm btn-outline-primary';
    edit_button.setAttribute('id', 'edit');
    edit_button.innerHTML = 'Save';

    form.append(edit_textarea, edit_button);
    edit_textarea.innerHTML = content;

    console.log(parent);
    document.querySelector('#edit').addEventListener('submit', save_edit);
};


function save_edit() {
/* TODO: */
    /* first: GET post, then PUT */
    /* views -> csrf temp. deactivated */
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            content: document.querySelector('#edit_content').value
        })
    })
    .then(function(response) {
  
        // Print result & load mailbox
        console.log(response);
    })

};
