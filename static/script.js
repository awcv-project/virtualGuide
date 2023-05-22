document.addEventListener('DOMContentLoaded', function() {
    // Start recording button event listener
    document.getElementById('start-recording').addEventListener('click', function(event) {
        event.preventDefault();
        startRecording();
    });

    // // Stop recording button event listener
    // document.getElementById('stop-recording').addEventListener('click', function(event) {
    //     event.preventDefault();
    //     stopRecording();
    // });

    // Play voice button event listener
    document.getElementById('play-voice').addEventListener('click', function(event) {
        event.preventDefault();
        var inputLanguage = document.getElementById('input-language').value;
        var button= document.getElementById('play-voice');
        button.disabled=true;
        var start_button=document.getElementById('start-recording');
        start_button.disabled=false;
        playVoice(inputLanguage);
    });
});

function startRecording() {
    fetch('/start_recording', {
        method: 'POST'
    })
    .then(function(response) {
        if (response.ok) {
            console.log('Recording started');
        } else {
            console.error('Error starting recording');
        }
    })
    .catch(function(error) {
        console.error('Error starting recording:', error);
    });
}

function stopRecording() {
    fetch('/stop_recording', {
        method: 'POST'
    })
    .then(function(response) {
        if (response.ok) {
            console.log('Recording stopped');
        } else {
            console.error('Error stopping recording');
        }
    })
    .catch(function(error) {
        console.error('Error stopping recording:', error);
    });
}

function playVoice(inputLanguage) {
    fetch('/play_voice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ inputLanguage: inputLanguage })
    })
    .then(function(response) {
        if (response.ok) {
            console.log('Playing voice');
            response.text().then(function(data) {
                $('#status').append('<p>' + data + '</p>');
            });
        } else {
            console.error('Error playing voice');
        }
    })
    .catch(function(error) {
        console.error('Error playing voice:', error);
    });
}

