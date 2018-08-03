class SocketInterface {
    constructor(port) {
        this.port = port;
        this.socket = null;
    }

    connect() {
        if(this.socket == null) {
            this.socket = io('http://localhost:' + this.port)
            this.init()
        }
    }

    init() {
        if(this.socket == null) {
            this.connect()
        }
        this.socket.on('connection', function (socket) {

        });
    }
}

class RawVarEditor {
    constructor(kwargs) {
        var id = kwargs["id"];
        this.input = $("#" + id + "_var_display");
        this.submit_button = $("#" + id + "_submit");
        this.submit_button.click(function(event) {
            console.log("Click");
        });
    }
}