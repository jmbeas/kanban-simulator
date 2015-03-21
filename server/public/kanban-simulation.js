(function (document, $, storage) { // let's pull all of this into context of nice function

  $(document).ready(function() {

    var ws;
    var host = 'localhost';
    var port = '8888';
    var uri = '/ws';

    ws = new WebSocket("ws://" + host + ":" + port + uri);
    ws.onopen = function(event) {
      $("#connection").css("color", "#00ff00");
      $("#connection").removeClass("glyphicon-ban-circle").addClass("glyphicon-ok-circle");
    };
    ws.onclose = function() {
      $("#connection").css("color", "#ff0000");
      $("#connection").removeClass("glyphicon-ok-circle").addClass("glyphicon-ban-circle");
    };
    ws.onmessage = function(event) {
      var msg = JSON.parse(event.data);
      // El texto del mensaje está en msg.text
      var li = $("<li class='timeline-inverted'/>");
      li.append("<div class='timeline-badge'><i class='fa fa-car'></i></div>");
      var title = $("<h4>").addClass("timeline-title").text(msg.text);
      var message = $("<div class='timeline-panel'><div class='timeline-heading'>");
      message.append(title).appendTo(li);
      li.appendTo("#container");
      return false;
    };

    });


})(document, jQuery, localStorage);
