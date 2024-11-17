class SocketConnection {
    constructor(connection = "")
    {
        this.socketUrl =  CONFIG.socketUrl + "/" + (connection ? connection + "/" : "");
        this.connection = this.socketUrl + "?token=" + localStorage.getItem("token");
        this.socket = new WebSocket(this.connection);
        
        this.socket.onopen = (event) => this.onOpen(event);
        this.socket.onmessage = (event) => this.onMessage(event);
        this.socket.onclose = (event) => this.onClose(event);
        this.socket.onerror = (event) => this.onError(event);
        this.events = [];
    }

    disconnect() {
        console.log(`${this.socketUrl} disconnecting`);
        this.socket.close();
    }

    onOpen(event) 
    {
        let url = event.currentTarget.url.split("?")[0];
        console.log(`${url} connected`);
    }

    onMessage(event) {
        let url = event.currentTarget.url.split("?")[0];
        let data = JSON.parse(event.data);
        if (this.events[data.event])
            this.events[data.event](data.payload);
        console.log(`${url} message received`);
    }

    onClose(event) {
        let url = event.currentTarget.url.split("?")[0];
        console.log(`${url} disconnected`);
    }

    onError(event) {
        let url = event.currentTarget.url.split("?")[0];
        console.log(`${url} error`);
    }

    send(event, payload=null) {
        this.socket.send(JSON.stringify({
            event: event,
            payload: payload
        }));
        console.log(`${this.socketUrl} message sent`);
    }

    event(event, func)
    {
        this.events[event] = func;
    }
}