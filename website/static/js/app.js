document.addEventListener('DOMContentLoaded', () => {

    // Function to hide flash messages after 5 seconds
    function hideFlashMessages() {
        document.querySelector('.alert').style.display = "none";
    }

    // Set a timeout to call the hideFlashMessages function after 5 seconds
    setTimeout(hideFlashMessages, 5000);
});

function handleSignUpForm(event) {
    console.log(event.target);

    event.preventDefault(); // Prevent the default form submission
    
    // Get form data
    var formData = $(this).serialize();
    
    // Send AJAX request to Flask backend
    $.ajax({
        type: 'POST',
        url: '/sign-up',
        data: formData,
        success: (response) => {
            // Update the page with the flash message
            if (response.category === 'error') {
                document.querySelector('#messageDiv').html(
                    '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                    response.message +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button></div>'
                );
            } else if (response.category === 'success') {
                document.querySelector('#messageDiv').html(
                    '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                    response.message +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button></div>'
                );
            }
        }
    });
}

function deleteNote(noteId)
{
    fetch('/delete-note', 
    {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => 
    {
        window.location.href = '/';
    });
}
