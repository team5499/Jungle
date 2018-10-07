class SocketInterface {
    constructor(port) {
        this.port = port;
        this.socket = null;
    }

    connect() {
        if(this.socket == null) {
            this.socket = io(window.location.protocol + "//" + window.location.host, {transports: ['websocket']});
            this._init();
        }
    }

    _init() {
        this.socket.on("connect", function (socket) {
            console.log("connection");
        });
    }

    static get_instance() {
        if(SocketInterface.INSTANCE == null) {
            SocketInterface.INSTANCE = new SocketInterface(SocketInterface.PORT);
        }
        return SocketInterface.INSTANCE;
    }
}
SocketInterface.PORT = 5800;
SocketInterface.INSTANCE = null;


class RawVarEditor {
    constructor(kwargs) {
        var id = kwargs["id"];
        this.input = $("#" + id + "_var_display");
        this.submit_button = $("#" + id + "_submit");
        this.submit_button.click(function(event) {
            SocketInterface.get_instance().connect();
        });
    }
}