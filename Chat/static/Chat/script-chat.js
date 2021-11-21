$(document).ready(function () {
    const name = JSON.parse(document.getElementById('name').textContent);
    const nameSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + name
        + '/'
        );

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
    );

    let delay = setTimeout(function () {
        if (nameSocket.readyState === WebSocket.OPEN){
            nameSocket.send(JSON.stringify({
                message_type: "name",
                message: name,
                status: "online"
            }));
            delay = setTimeout(function () {
            },500);
        }
    },500);


    nameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data["message_type"] === "status" && data["message"] === "online") {
            $(".online_names").empty();
            for (let i=0;i<data["online_list"].length;i++){
                var name_para = document.createElement("p");
                var name_para_text = document.createTextNode(data["online_list"][i] + "    " + "online");
                name_para.appendChild(name_para_text);
                var online_names = document.getElementsByClassName("online_names")[0];
                online_names.appendChild(name_para);
            }
        }
    };

    chatSocket.onmessage = function(e){
        const data = JSON.parse(e.data);
        if (data["message_type"] === "message"){
            document.getElementById("chat_log").value += data["message"] + "\n";
        }
    };


    $("#send").click(function () {
        var message = $("#text_input").val();
        chatSocket.send(JSON.stringify({
            message_type: "message",
            message: message,
            name: name,
        }));
        document.getElementById("text_input").value = "";
    });
});