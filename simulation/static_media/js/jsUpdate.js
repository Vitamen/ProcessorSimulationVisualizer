//Register
var pusher = new Pusher('e217c8fb76bbbb16a8cd');
var channel = pusher.subscribe('test_channel');
channel.bind('my_event', function(data) {
      alert(data);
});