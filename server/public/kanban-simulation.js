var format_message_for_the_timeline = function($,msg) {
  var li = $("<li class='timeline-inverted'/>");
  li.append("<div class='timeline-badge'><i class='fa'></i></div>");
  switch (msg.type) {
    case 'open':
      li.removeClass("timeline-inverted");
      li.find(".fa").addClass("fa-check");
      break;
    case 'close':
      li.removeClass("timeline-inverted");
      li.find(".fa").addClass("fa-close");
      break;
      case 'charging':
        li.find(".fa").addClass("fa-bolt");
        break;
    case 'interruption':
      li.removeClass("timeline-inverted");
      li.find(".fa").addClass("fa-wrench");
      break;
    default:
      li.find(".fa").addClass("fa-car");
  }

  var title = $("<h4>").addClass("timeline-title").text(msg.text);
  var message = $("<div class='timeline-panel'><div class='timeline-heading'>");
  message.append(title);

  if (msg.timestamp) {
    var timestamp = $("<p>").append(
      $("<small class='text-muted'>").text(' '+msg.timestamp).prepend("<i class='fa fa-clock-o'></i>") );
    message.append(timestamp);
  }

  message.appendTo(li);
  return li;
};

var init_websocket = function() {

  var ws;
  var host = 'localhost';
  var port = '8888';
  var uri = '/ws';

  ws = new WebSocket("ws://" + host + ":" + port + uri);
  ws.onopen = function(event) {
    $("#connection").css("color", "#00ff00");
    $("#connection").removeClass("glyphicon-ban-circle").addClass("glyphicon-ok-circle");
    var msg = {'text':'Connection open','type':'open'};
    var li = format_message_for_the_timeline($,msg);
    li.appendTo("#container");
  };
  ws.onclose = function() {
    $("#connection").css("color", "#ff0000");
    $("#connection").removeClass("glyphicon-ok-circle").addClass("glyphicon-ban-circle");
    var msg = {'text':'Connection closed','type':'close'};
    var li = format_message_for_the_timeline($,msg);
    li.appendTo("#container");
  };
  ws.onmessage = function(event) {
    var msg = JSON.parse(event.data);
    var li = format_message_for_the_timeline($,msg);
    li.appendTo("#container");
    return false;
  };
  return ws;
};

var start_simulation = function(ws) {
  ws.send('start');
};

var stop_simulation = function(ws) {
  ws.send('stop');
};

(function (document, $, storage) { // let's pull all of this into context of nice function

  $(document).ready(function() {
    var ws = init_websocket();
    $("#play_button.start").click(function() {
      start_simulation(ws);
      $(this).removeClass("start").addClass("stop");
      $(this).find(".glyphicon").removeClass("glyphicon-play").addClass("glyphicon-stop");
    });
    $("#play_button.stop").click(function() {
      stop_simulation(ws);
      $(this).removeClass("stop").addClass("start");
      $(this).find(".glyphicon").removeClass("glyphicon-stop").addClass("glyphicon-start");
    });
  });


})(document, jQuery, localStorage);
