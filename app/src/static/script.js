const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const widget = document.getElementById('scrollable-widget');
const slides = widget.querySelectorAll('.widget-temp');
let currentSlide = 0;
const threshold = 50;


let userMessage;
const API_KEY = "";

const createChatLi = (message, className) => {
    //Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">potted_plant</span> <p></p>`;
    chatLi.innerHTML = chatContent;
    //Prevent HTML input
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

//**************************BIG PART
const generateResponse = (incomingChatLi, message) => {

    
    const API_url = "/internal/query";
    const messageElement = incomingChatLi.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'question': message
         })
    }

    fetch(API_url, requestOptions).then(res => res.json()).then(data => {
        response = data.answer;
        messageElement.textContent = response;
        if (window.MathJax) {
            MathJax.typesetPromise([messageElement]).then(() => {
                console.log("MathJax rendering complete");
            });
        }
        
    }).catch((error) => {
        console.log(error);
        messageElement.textContent = "Uh oh, wrong data :(("
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight)); 
    //Wow. two anonymous classes in one line
}

const getWeatherStats = () => {
    const API_url = "http://127.0.0.1:5000/internal/weather"

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'category': 'temperature_2m'
        })
    }

    fetch(API_url, requestOptions).then(res => res.json()).then(data => {
        console.log("bello!");
        document.querySelector("h2").innerHTML = data;
    }).catch((error) => {
        console.log(error);

    })

    //window.setInterval(getWeatherStats(), 100)
}

let weatherStats = setInterval(getWeatherStats(), 1000);

 
const handleChat = () => {
    userMessage = chatInput.value.trim();
    console.log(userMessage); //Important.
    if (!userMessage) return;
    chatInput.value = ""; //Delete chat once sent
    
    //Append user's message to chatbox 
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));

    //Auto-scroll to bottom
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        //Chatbot think.
        const incomingChatLi = createChatLi("Hmmmm...", "incoming")
        
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi, userMessage);
    }, 600)
}

widget.addEventListener('wheel', (event) => {
    // Prevent default scroll behavior if you want to control the interaction completely
    event.preventDefault();
  
    if (event.deltaY > threshold) {
      // Scroll down detected: show next slide if it exists
      if (currentSlide < slides.length - 1) {
        slides[currentSlide].classList.remove('active');
        currentSlide++;
        slides[currentSlide].classList.add('active');
      }
    } else if (event.deltaY < -threshold) {
      // Scroll up detected: show previous slide if it exists
      if (currentSlide > 0) {
        slides[currentSlide].classList.remove('active');
        currentSlide--;
        slides[currentSlide].classList.add('active');
      }
    }
  });




sendChatBtn.addEventListener("click", handleChat);

chatInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        handleChat();
    }
});