document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', event => {
    event.preventDefault();
    send_email();
  })
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single_email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single_email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><br>`;

  // Send GET request to /emails/<mailbox>
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    // Create div for every email
    emails.forEach(email => {

      const one_email = document.createElement('div');
      one_email.className = 'list-group-item email';
      one_email.innerHTML = `
      <h6>From: ${email.sender}
      <h5>${email.subject}</h5>
      <small>${email.timestamp}<small>`;

      if (email.read) {
        one_email.style.backgroundColor = 'gray';
      }
      else
      {
        one_email.style.backgroundColor = 'white';
      }

      // Allow to click and view email page
      one_email.addEventListener('click', () => load_email(email.id));

      document.querySelector('#emails-view').append(one_email);
    })
  });
}

function load_email(email_id) {

  // Show single email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single_email-view').style.display = 'block';

  // Mark email as read
  read_email(email_id);

  // Send GET request to /emails/email_id
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Fill div with single email
    const email_page = document.querySelector('#single_email-view');
    email_page.className = '';

    // Set text for archive button
    const is_archived = email.archived;
    let button_text;
    if (is_archived) {
      button_text = 'Unarchive';
    }
    else {
      button_text = 'Archive';
    }
    
    email_page.innerHTML = `
    <h6>From: ${email.sender}</h6>
    <h6>To: ${email.recipients}</h6>
    <h6>Subject: ${email.subject}</h6>
    <h6>Timestamp: ${email.timestamp}</h6>
    <button id="reply_button">Reply</button>
    <hr>
    <h5>${email.body}</h5>
    <button id="archive_button">${button_text}</button>`;

    // Allow to archive / unarchive email then button is clicked
    if (email.sender != email.user) {
      document.querySelector('#archive_button').addEventListener('click', () => archive_email(email));
    }
    else {
      document.querySelector('#archive_button').style.display = 'none';
    }

    // Allow to reply to email
    document.querySelector('#reply_button').addEventListener('click', () => reply(email));
  });
}

function read_email(email_id) {

  // Send PUT request to /emails/<email_id>
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function archive_email(email) {

  // Archive it or unarchive it based on its status
  if (email.archived) {
    
    // Send PUT request to /emails/<email_id>
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })
  }
  else {

    // Send PUT request to /emails/<email_id>
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
  }

  // Redirect to inbox page
  load_mailbox('inbox');
}

function reply(email) {

  // Redirect to composition form
  compose_email();

  // Pre-fill the composition form
  document.querySelector('#compose-recipients').value = email.sender;

  if (email.body.startsWith('Re:')) {
    document.querySelector('#compose-subject').value = email.subject;
  }
  else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }

  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
}

function send_email() {

  // Get input
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a POST request to the /emails
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipient,
        subject: subject,
        body: body
    })
  })

  // Redirect to sent page if successful
  .then(response => response.json())
  .then(result => {
    if (result.message == 'Email sent successfully.') {
      load_mailbox('sent');
    }
  });
}
