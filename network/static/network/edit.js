// Wait for page to loaded:
document.addEventListener('DOMContentLoaded', function() {

/* TODO: */
    /* more specific: name=edit, forEach? */
    const buttons = document.getElementsByTagName("button");
    for (var i = 0; i < buttons.length; i += 1) {
        buttons[i].onclick = function() {
            edit(this.id);
        };
    };
});

/* replaces content of div with POST-Form */
function edit(id) {
    var element = document.getElementById(id);
    const parent = element.parentElement;
    const content = element.previousElementSibling.innerHTML.trim();
    parent.innerHTML = '';

    /* Create Content Textfield */
    var edit_textarea = document.createElement('textarea');
    edit_textarea.setAttribute('id', 'edit_content');

    /* Create Editing Button */
    var edit_button = document.createElement('button');
    edit_button.className = 'btn btn-sm btn-outline-primary';
    edit_button.setAttribute('id', 'edit');
    edit_button.innerHTML = 'Save';

    parent.append(edit_textarea, edit_button);
    edit_textarea.innerHTML = content;

    document.querySelector('#edit').addEventListener('click', save_edit)

};


function save_edit(event) {
/* TODO: */
    /* views -> csrf temp. deactivated */
    console.log(`id = ${document.querySelector('#edit_content').parentNode.id.slice(8)}`);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/edit',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
            id: document.querySelector('#edit_content').parentNode.id.slice(8),
            content: document.querySelector('#edit_content').value
        })
    })
    .then(function(response) {
        console.log(response);
    })
    .catch(error => {
        console.log('Error:', error);
    });

    event.preventDefault();
};
