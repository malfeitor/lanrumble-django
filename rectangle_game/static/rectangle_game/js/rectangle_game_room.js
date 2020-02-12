var roomName = window.location.pathname.slice(16,-1);

var chatSocket = new WebSocket(
    'wss://' + window.location.host +
    '/ws/rectangle_game/' + roomName + '/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#chat-log').value += (message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));

    messageInputDom.value = '';
};

// debut du code du jeu avec PHASER !
let gameScene = new Phaser.Scene('Game');

let config = {
    type: Phaser.AUTO,
    width: 640,
    height: 640,
    parent: 'phaser-content',
    scene: gameScene
};

let game = new Phaser.Game(config);