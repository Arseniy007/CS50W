document.addEventListener('DOMContentLoaded', function() {

    // Get all like buttons
    const like_buttons = document.getElementsByClassName('like_button');
    const num_of_like_buttons = like_buttons.length;

    // Add functionality
    for (let i = 0; i < num_of_like_buttons; i++) {
        like_buttons[i].addEventListener('click', () => like_post(like_buttons[i].dataset.post_id));
    }

    // Get follow button and add functionality to it
    const follow_button = document.querySelector('#follow_button');

    if (follow_button) {
        follow_button.addEventListener('click', () => follow(follow_button.dataset.user_id));
    }
    
    // Get all edit post buttons
    const edit_post_buttons = document.getElementsByClassName('edit_button');
    const num_of_edit_buttons = edit_post_buttons.length;

    // Add functionality
    for (let i = 0; i < num_of_edit_buttons; i++) {
        edit_post_buttons[i].addEventListener('click', () => edit_post(edit_post_buttons[i].dataset.post_id));
    }

    // Get all delete buttons
    const delete_post_buttons = document.getElementsByClassName('delete_button');
    const num_of_delete_buttons = delete_post_buttons.length;

    // Add functionality
    for (let i = 0; i <num_of_delete_buttons; i++) {
        delete_post_buttons[i].addEventListener('click', () => delete_post(delete_post_buttons[i].dataset.post_id));
    }
});

function like_post(post_id) {

    // Send request to like-view
    fetch(`like/${post_id}`)
    .then(response => response.json())
    .then(result => {

        // Update number of likes
        document.querySelector(`#likes_for_${post_id}`).innerHTML = `Likes: ${result.number_of_likes}`;
    });
}

function follow(user_id) {

    // Send request to follow-view
    fetch(`/follow/${user_id}`)
    .then(response => response.json())
    .then(result => {

        // Get right text for follow button
        let button_text;
        if (result.status === 'not followed') {
            button_text = 'Follow';
        }
        else {
            button_text = 'Unfollow';
        }

        // Update number of followers
        document.querySelector('#follow_button').innerHTML = button_text;
        document.querySelector('#number_of_followers').innerHTML = `Number of followers: ${result.number_of_followers}`;
    });
}

function edit_post(post_id) {

    // Get post insides
    const post_view = document.querySelector(`#post_view_${post_id}`);
    const edit_form_div = document.querySelector(`#edit_form_${post_id}`);

    if (post_view.style.display == 'block') {

        // Hide post
        post_view.style.display = 'none';
        edit_form_div.style.display = 'block';

        // Add functionality to save button (call save function)
        const save_button = document.querySelector(`#save_${post_id}`);
        save_button.addEventListener('click', () => save_edited_post(post_id));
    }
    else {
        // Show it back if hidden
        post_view.style.display = 'block';
        edit_form_div.style.display = 'none';
    }
}

function save_edited_post(post_id) {
    
    // Get post insides
    const post_view = document.querySelector(`#post_view_${post_id}`);
    const edit_form = document.querySelector(`#edit_form_${post_id}`);
    const old_text = document.querySelector(`#text_${post_id}`);

    // Get new text for the post
    const new_text = document.querySelector(`#new_text_${post_id}`).value;

    // Send POST request to edit view
    fetch(`/edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            new_text: new_text
        })
    })

    // Show new text if successful
    .then(response => response.json())
    .then(result => {

        if (result.status === 'ok') {
            // Replace old text with new one
            old_text.innerHTML = new_text;
        }        

        // Hide edit form and show post
        edit_form.style.display = 'none';
        post_view.style.display = 'block';
    });
}

function delete_post(post_id) {

    // Send request to delte_post-view
    fetch(`/delete/${post_id}`)
    .then(response => response.json())
    .then(result => {

        if (result.status === 'ok') {
            // Get post
            const post = document.querySelector(`#post_${post_id}`);

            // Play removing animation and hide it
            post.style.animationPlayState = 'running';
            post.addEventListener('animationend', () => {
                post.remove();
            });
        }
    });
}
