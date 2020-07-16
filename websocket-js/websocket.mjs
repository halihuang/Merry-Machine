export { new_web_socket }

function new_web_socket(uri_path) {
  var protocol = 'ws:';
  if (window.location.protocol === 'https:') {
      protocol = 'wss:';
  }
  var host = window.location.host;
  var url = protocol + '//' + 'localhost:5000' + uri_path;
  console.log(url);
  var ws = new WebSocket(url);
  return ws;
}