(function (document, $, storage) { // let's pull all of this into context of nice function

  $(document).ready(function() {

    var ws;
    var host = 'localhost';
    var port = '8888';
    var uri = '/ws';

    ws = new WebSocket("ws://" + host + ":" + port + uri);
    ws.onopen = function(event) {
      $("#container").css("background", "#00ff00");
    };
    ws.onmessage = function(event) {
      var msg = JSON.parse(event.data);
      $("<li/>").text(msg.text).appendTo("#container");
      return false;
    };
    ws.onclose = function() {
      $("#container").css("background", "#ff0000");
    };

    });


})(document, jQuery, localStorage);
