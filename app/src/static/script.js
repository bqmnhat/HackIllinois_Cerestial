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

    //Not working
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
    const API_url = "/internal/weather"

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
        current_weather = data.current_weather;
        day = data.day
        console.log(current_weather)
        console.log(day)
        document.getElementById("temperature").innerHTML = current_weather + "°";

        const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];

        let graph = document.getElementById("chart");
        if (graph) {
            drawGraph(xValues, day, graph);
        }

        

    }).catch((error) => {
        console.log(error);

    })

    //window.setInterval(getWeatherStats(), 100)
}

const drawGraph = (xValues, yValues, graph) => {
    
    new Chart(graph, {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: "rgba(0, 0, 255, 1.0)",
                fill: false,
                borderColor: "rgba(0, 0, 255, 1.0)",
                data: yValues
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        color: "black"
                    }
                    
                },
                y: {
                    ticks: {
                        color: "black"
                    }
                }

            }
            //legend: {display: false},
            //scales: {
            //    yAxes: [{ticks: {min: -10, max: 10}}],
            //}
        }
    });

    //chart.render()
}

let weatherStats = setInterval(getWeatherStats(), 1000);

 
const handleChat = () => {
    sendChatBtn.removeEventListener("click", handleChat);
    chatInput.removeEventListener("keydown", handleChatKeydown);
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
    // sendChatBtn.addEventListener("click", handleChat);

    // chatInput.addEventListener("keydown", function(event) {
    //     if (event.key === "Enter") {
    //         event.preventDefault();
    //         handleChat();
    //     }
    // });
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