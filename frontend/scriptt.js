const userInput = document.getElementById("userInput");

const sessionid = crypto.randomUUID();
// console.log(sessionid);

function addMessage(text, sender) {



   
    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");
    messageDiv.classList.add(sender === "user" ? "user-message" : "ai-message");


  
    const avatarDiv = document.createElement("div");

    avatarDiv.classList.add("message-avatar");

    avatarDiv.textContent = sender === "user" ? "YOU" : "AI";


   
    const contentDiv = document.createElement("div");

    contentDiv.classList.add("message-content");


    const paragraph = document.createElement("p");

    paragraph.textContent = text;

    contentDiv.appendChild(paragraph);


    
    if (sender === "ai") {
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
    } else {
        messageDiv.appendChild(contentDiv);
    }



    chatMessages.appendChild(messageDiv);


    
    chatMessages.scrollTop = chatMessages.scrollHeight;


    return messageDiv;
}

chatForm.addEventListener("submit", async function (event) {

  
    event.preventDefault();


    
    const message = userInput.value.trim();


   
    if (message === "") {
        return;
    }


    
    addMessage(message, "user");


    userInput.value = "";

    const typingEl = addMessage("typing...", "ai");

    
    try {
        const response = await fetch("http://127.0.0.1:8000/hello", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: message ,session_key: sessionid})
        });

        const data = await response.json();
        typingEl.remove();
        addMessage(data.answer, "ai");
    } catch (error) {
        typingEl.remove();
        addMessage("Something went wrong, try again later.", "ai");
    }


    addMessage(aiResponse, "ai");



});