$(window).on('load', function () {
  let protocol = 'wss://';
  let to;
  const elementMessage = $('#message');
  const msgArea = $('#msg_area');

  if (location.protocol === 'http:') {
    protocol = 'ws://';
  }
  const socket = new WebSocket(protocol + window.location.host + window.location.pathname);

  socket.onopen = function () {
    to = msgArea[0].scrollHeight;
    scrollMsg(to);
  };

  socket.onmessage = function (res) {
    let data = JSON.parse(res.data);
    let sender;
    if (data.sender) {
      sender = data.sender.toString();
      delete data.sender;
    }
    let html;
    let last_msg = msgArea.children().last();
    console.log(username, sender);
    if (username === sender) {
      // if last msg from self
      if (last_msg.hasClass('ongoing')) {
        // if prev msg from self to
        html = '' +
          '<div class="col-12 col-sm-10 mb-2 ongoing ' + sender + '">' +
          ' <div class="media from-user">' +
          '   <div class="media-body">' +
          '     <p>' + data.message + '</p>' +
          '     <p class="msg-date">' + data.created + '</p>' +
          '     <img src="/static/img/icon-check-mark.svg" alt="Delivered" class="msg-seen">' +
          '   </div>' +
          ' </div>' +
          '</div>';
      } else {
        // if prev msg from recipient
        html = '' +
          '<div class="col-12 col-sm-10 mb-2 ongoing ' + sender + '">' +
          ' <div class="media from-user">' +
          '   <span class="avatar mx-3">' + sender + '</span>' +
          '   <div class="media-body">' +
          '     <p>' + data.message + '</p>' +
          '     <p class="msg-date">' + data.created + '</p>' +
          '     <img src="/static/img/icon-check-mark.svg" alt="Delivered" class="msg-seen">' +
          '   </div>' +
          ' </div>' +
          '</div>';
      }
    } else {
      // if last msg from recipient
      if (!last_msg.hasClass(sender)) {
        // if prev msg from recipient
        html = '' +
          '<div class="col-12 col-sm-10 mb-2 incoming ml-auto ' + sender + '">' +
          ' <div class="media to-user">' +
          '   <div class="media-body">' +
          '     <p>' + data.message + '</p>' +
          '     <p class="msg-date">' + data.created + '</p>' +
          '   </div>' +
          '   <span class="avatar mx-3">' + sender + '</span>' +
          ' </div>' +
          '</div>';
      } else {
        // if prev msg from self
        html = '' +
          '<div class="col-12 col-sm-10 mb-2 incoming ml-auto ' + sender + '">' +
          ' <div class="media to-user">' +
          '   <div class="media-body">' +
          '     <p>' + data.message + '</p>' +
          '     <p class="msg-date">' + data.created + '</p>' +
          '   </div>' +
          ' </div>' +
          '</div>';
      }
    }
    msgArea.append(html);
    to = msgArea[0].scrollHeight;
    scrollMsg(to);
  };

  socket.onclose = function () {};

  $(window).onbeforeunload = function () {
    socket.close();
  };

  // -------------------------------------------------------------------------------------------

  $('#sendMsgBtn').click(function () {
    sendMessage();
  });

  function sendMessage() {
    let text = elementMessage.val().trim();
    if (text.length > 0) {
      socket.send(JSON.stringify({message: text}));
      elementMessage.val('');
    }
  }

  elementMessage.keypress(function (e) {
    const code = (e.keyCode ? e.keyCode : e.which);
    if (code === 13) {
      sendMessage();
      return false;
    }
  });

  function scrollMsg(to) {
    $('.chat-messages').animate({scrollTop: to}, 500);
  }
});