const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const UIToggler = document.querySelector(".UI-toggler");
const chatbot = document.querySelector(".chatbot");

let userMessage;
let page = 0;
let last_id;



const getLastId = async () => {
    const API_URL = "/internal/get_count";

    try {
        const response = await fetch(API_URL, { method: 'GET' });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        last_id = data.count

        const chatDiv = document.createElement("div");
        chatDiv.className += " start_session";
        chatDiv.textContent = "Session started."
        chatbox.appendChild(chatDiv);

        if (last_id == 0) {
            chatbox.appendChild(createChatLi(
                "Hello! What can I help you with?", "incoming", new Date()));
        }
      } catch (error) {
        console.error("Error getting last message's id:", error);
      }
}

getLastId();

const createChatLi = (message, className, time) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    
    let chatContent = className === "outgoing" 
        ? `<p></p>` 
        : `<span class="material-symbols-outlined">potted_plant</span><p></p>`;

    chatLi.innerHTML = chatContent;
    const chatDiv = document.createElement("div");
    const chatSmall = document.createElement("small");
    // Prevent HTML input and set message text
    chatDiv.textContent = message;
    
    // Set the time correctly
    chatSmall.textContent = formatDateToCustomFormat(time);
    chatLi.querySelector("p").appendChild(chatDiv)
    chatLi.querySelector("p").appendChild(chatSmall)

    return chatLi;
};


//**************************BIG PART
const generateResponse = (incomingChatLi, message) => {

    
    const API_url = "/internal/query";
    const messageElement = incomingChatLi.querySelector("p div");

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
        setTimeout( () => {
            sendChatBtn.disabled = false;
            chatInput.disabled = false;
            sendChatBtn.addEventListener("click", handleChat);
            chatInput.addEventListener("keydown", check_handle);
            chatInput.focus(); 
        }, 600)
        
    }).catch((error) => {
        console.log(error);
        messageElement.textContent = "Uh oh,something is wrong :(("
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

    getWeatherCode();

    fetch(API_url, requestOptions).then(res => res.json()).then(data => {
        console.log("bello!");
        current_weather = data.current_weather;
        day = data.day
        for (let i = 0; i < day.length; i++) {
            day[i] = day[i] * 9/5 + 32;
        }
        console.log(current_weather)
        document.getElementById("temperature").innerHTML = (current_weather * 9/5 + 32) + "°F";

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

// let weather_dictionary = {'0': "{{url_for('static',filename='sunny.gif')}}", 
//     '1': "{{url_for('static',filename='sunny.gif')}}", 
//     '2': "{{url_for('static',filename='sunny.gif')}}", 
//     '3': "{{url_for('static',filename='sunny.gif')}}",
//     '45': "..\\static\\cloudy.gif", 
//     '48': "..\\static\\cloudy.gif",
//     '51': "..\\static\\cloudy.gif", 
//     '53': "..\\static\\cloudy.gif", 
//     '55': "..\\static\\cloudy.gif",
//     '56': "..\\static\\snowy.gif",
//     '57': "..\\static\\snowy.gif",
//     '61': "..\\static\\rainy.gif", 
//     '63': "..\\static\\rainy.gif", 
//     '65': "..\\static\\rainy.gif",	
//     '66': "..\\static\\rainy.gif", 
//     '67': "..\\static\\rainy.gif",
//     '71': "..\\static\\snowy.gif",
//     '73': "..\\static\\snowy.gif", 
//     '75': "..\\static\\snowy.gif",
//     '77': "..\\static\\snowy.gif",
//     '80': "..\\static\\rainy.gif", 
//     '81': "..\\static\\rainy.gif", 
//     '82': "..\\static\\rainy.gif",
//     '85': "..\\static\\snowy.gif",
//     '86': "..\\static\\snowy.gif",
//     '95': "..\\static\\rainy.gif",
//     '96': "..\\static\\rainy.gif", 
//     '99': "..\\static\\rainy.gif"}

let weather_dictionary = {'0': "..\\static\\sunny.gif", 
    '1': "..\\static\\sunny.gif", 
    '2': "..\\static\\sunny.gif", 
    '3': "..\\static\\sunny.gif",
    '45': "..\\static\\cloudy.gif", 
    '48': "..\\static\\cloudy.gif",
    '51': "..\\static\\cloudy.gif", 
    '53': "..\\static\\cloudy.gif", 
    '55': "..\\static\\cloudy.gif",
    '56': "..\\static\\snowy.gif",
    '57': "..\\static\\snowy.gif",
    '61': "..\\static\\rainy.gif", 
    '63': "..\\static\\rainy.gif", 
    '65': "..\\static\\rainy.gif",	
    '66': "..\\static\\rainy.gif", 
    '67': "..\\static\\rainy.gif",
    '71': "..\\static\\snowy.gif",
    '73': "..\\static\\snowy.gif", 
    '75': "..\\static\\snowy.gif",
    '77': "..\\static\\snowy.gif",
    '80': "..\\static\\rainy.gif", 
    '81': "..\\static\\rainy.gif", 
    '82': "..\\static\\rainy.gif",
    '85': "..\\static\\snowy.gif",
    '86': "..\\static\\snowy.gif",
    '95': "..\\static\\rainy.gif",
    '96': "..\\static\\rainy.gif", 
    '99': "..\\static\\rainy.gif"}

const getWeatherCode = () => {
    const API_url = "/internal/weather"

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'category': 'weather_code'
        })
    }

    fetch(API_url, requestOptions).then(res => res.json()).then(data => {
        console.log("bello!");
        current_weather = data.current_weather;
        day = data.day;
        console.log(current_weather);
        document.getElementsByClassName("weatherimg")[0].src=weather_dictionary[current_weather]
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
                label: "Temperature Today",
                backgroundColor: "rgba(0, 0, 255, 1.0)",
                fill: false,
                borderColor: "rgba(255, 255, 255, 1.0)",
                pointBackgroundColor: "white",  
                pointBorderColor: "white",
                data: yValues
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        color: "black"
                    },
                    grid: {
                      color: "black"       
                    },
                    border: {
                      color: "black"
                    }
                    
                },
                y: {
                    ticks: {
                        color: "black"
                    },
                    grid: {
                        color: "black"       
                      },
                      border: {
                        color: "black"
                      }
                }

            }
             
        },
        plugins: {
            legend: {
              labels: {
                usePointStyle: true,  
                color: "black"        
              }
            }
          }
    });

    //chart.render()
}

let weatherStats = setInterval(getWeatherStats(), 1000);

function formatDateToCustomFormat(jsDate) {
    // Use getUTCHours() to avoid timezone issues and keep consistent with UTC time
    const hours = jsDate.getHours().toString().padStart(2, '0'); // 24-hour format
    const minutes = jsDate.getMinutes().toString().padStart(2, '0'); // Ensure two digits for minutes
    const month = (jsDate.getMonth() + 1).toString().padStart(2, '0'); // Month is 0-based
    const day = jsDate.getDate().toString().padStart(2, '0'); // Ensure two digits for day
    const year = jsDate.getFullYear().toString().slice(-2); // Get last two digits of the year
    
    return `${hours}:${minutes} ${month}/${day}/${year}`;
}

const loadChat = async () => {
    const API_url = "/internal/load_chat";
    const query = `n=5&page=${page}&max_id=${last_id}`;
    const url = `${API_url}?${query}`;

  try {
    const response = await fetch(url, { method: 'GET' });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    const messages = data.messages;
    if (messages.length == 0) {
        return;
    }
    for (const message of messages) {  
        let date = new Date(message.time)
        date.setHours(date.getHours() - 6);
        if (message.isBot == "True") {  
            chatbox.insertBefore(createChatLi(message.message, "incoming", date), chatbox.firstChild); 
        } else {
            chatbox.insertBefore(createChatLi(message.message, "outgoing", date), chatbox.firstChild);
        }
    }
    page += 1;

  } catch (error) {
    console.error('Error loading chat:', error);
  }
}
 
const handleChat = () => {
    userMessage = chatInput.value.trim();
    console.log(userMessage); //Important.
    if (!userMessage) return;
    sendChatBtn.disabled = true;
    chatInput.blur(); 
    sendChatBtn.removeEventListener("click", handleChat);
    chatInput.removeEventListener("keydown", check_handle);
    chatInput.value = ""; //Delete chat once sent
    
    //Append user's message to chatbox 
    chatbox.appendChild(createChatLi(userMessage, "outgoing", new Date()));

    //Auto-scroll to bottom
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        //Chatbot think.
        const incomingChatLi = createChatLi("Hmmmm...", "incoming", new Date())
        
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi, userMessage);
    }, 600)
}

const widgetContainer = document.querySelector(".widget-container"); // Select the div to toggle

if (UIToggler && widgetContainer) {
    UIToggler.addEventListener("click", () => {
      widgetContainer.classList.toggle("show-widget");
      chatbot.classList.toggle("blurred"); // Add blur effect
    });
  } else {
    console.error("UI-toggler or widget-container not found");
  }



sendChatBtn.addEventListener("click", handleChat);

chatInput.addEventListener("keydown", check_handle);

function check_handle(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        handleChat();
    }
};

chatbox.addEventListener("scroll", (event) => {
    if (chatbox.scrollTop === 0) {
        loadChat();
    }
});

function enable_load_chat() {
    chatbox.addEventListener("scroll", check_top_load);
}

function disable_load_chat() {
    chatbox.removeEventListener("scroll", check_top_load);
}

function check_top_load() {
    if (chatbox.scrollTop === 0) {
        loadChat();
    }
    disable_load_chat();
}

function check_not_top() {
    if (chatbox.scrollTop > 10) {
        enable_load_chat();
    }
}

loadChat()
chatbox.scrollTo(0, chatbox.scrollHeight);
