function send() {
    var input = document.getElementById("userinput").value;  
    var lang = document.getElementById("userlang").value; 

    document.getElementById("chatbox").innerHTML += "<p class='mensaje'> Tú: " + input + "</p>";  
    document.getElementById("userinput").value = ""; 

    fetchResponse(input, lang)
        .then(data => {
            displayTranslatedText(data.text);  
            playAudio(data.audio);  
            scrollChatbox();  
        });

    scrollChatbox();  
}
function handleKeyPress(event) {
    if (event.keyCode === 13) { // 13 corresponde a la tecla "Enter"
      send();
    }
  }
function fetchResponse(input, lang) {
    return fetch(`/get_response?msg=${input}&lang=${lang}`)  
        .then(response => response.json()); 
}

function displayTranslatedText(text) {
    var chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p class='mensajeia'> Guía: ${text}</p>`;  
}

function playAudio(audio) {
    var audioUrl = `data:audio/mp3;base64,${audio}`;  
    var player = document.getElementById("player");
    player.src = audioUrl;  
    player.play();  
}

function scrollChatbox() {
    var chatbox = document.getElementById("chatbox");
    chatbox.scrollTop = chatbox.scrollHeight;  
}


// funcion de microfono --------------------------------------------------
function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "es-ES"; 
        recognition.start();

        recognition.onresult = function(e) {
            document.getElementById('userinput').value = e.results[0][0].transcript;
            recognition.stop();
            send();
        };
        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}

