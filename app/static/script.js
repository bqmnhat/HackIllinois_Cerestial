const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");

let userMessage;
const API_KEY = "";

const createChatLi = (message, className) => {
    //Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span> <p></p>`;
    chatLi.innerHTML = chatContent;
    //Prevent HTML input
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

//**************************BIG PART
const generateResponse = (incomingChatLi) => {

    
    const API_url = "http://127.0.0.1:5000/internal/query";
    const messageElement = incomingChatLi.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'question': messageElement.textContent
         })
    }

    fetch(API_url, requestOptions).then(res => res.json()).then(data => {

        console.log("belo");
        messageElement.textContent = data.answer;
        //const JsonString = JSON.stringify({
        //    'question': messageElement.textContent
        //});


    }).catch((error) => {
        console.log(error);
        messageElement.textContent = "Uh oh, wrong data :(("
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight)); 
    //Wow. two anonymous classes in one line
}

 
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
        generateResponse(incomingChatLi);
    }, 600)
}
sendChatBtn.addEventListener("click", handleChat);