(async function ()
{
    let me = await get("auth/me");
    let friend = await get(`friends/${Router.params["username"]}`);
    let chatBox = document.getElementsByClassName("chat-box")[0];

    console.log(me);
    console.log(friend);
    let roomName = me.payload.user.id > friend.payload.friend.id ? `${me.payload.user.id}_${friend.payload.friend.id}` : `${friend.payload.friend.id}_${me.payload.user.id}`;
    let chat = new SocketConnection("chat/" + roomName);

    document.getElementById("message").addEventListener("keypress", function (e)
    {
        if (e.key === "Enter")
        {
            chat.send("message", this.value);
            this.value = "";
        }
    });
    chat.event("message", function (data)
    {
        let turn = me.payload.user.username === data.user.username ? "message-right" : "";
        let marginEnd = me.payload.user.username === data.user.username ? "me-2" : "";
        let html = `<div class="chat-message ${turn}">
            <div class="chat-message-sender">
                <img src="${data.user.image}" alt="Player 1" height="50" width="50" class="object-fit-cover">
                <p class="mb-0">${data.user.username}</p>
            </div>
            <div class="chat-message-content neon">
                <p class="mb-0 ${marginEnd}">${data.message}</p>
            </div>
        </div>`;
        chatBox.innerHTML += html;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
})();