class SocketConnection {
    constructor(connection = "") {
        this.connection = "ws://" + window.location.host + "/ws/" + (connection ? connection + "/" : "");
        this.socket = new WebSocket(this.connection);
        
        this.socket.onopen = (event) => this.onOpen(event);
        this.socket.onmessage = (event) => this.onMessage(event);
        this.socket.onclose = (event) => this.onClose(event);
        this.socket.onerror = (event) => this.onError(event);
    }

    disconnect() {
        console.log(`${this.connection} disconnecting`);
        this.socket.close();
    }

    onOpen(event) {
        console.log(`${event.currentTarget.url} connected`);
    }

    onMessage(event) {
        console.log(`${event.currentTarget.url} message received`);
    }

    onClose(event) {
        console.log(`${event.currentTarget.url} disconnected`);
    }

    onError(event) {
        console.log(`${event.currentTarget.url} error`);
    }

    send(event, payload, status) {
        this.socket.send(JSON.stringify({
            event: event,
            payload: payload,
            status: status
        }));
        console.log(`${this.connection} message sent`);
    }
}