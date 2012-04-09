//Register
var pusher = new Pusher('9bc222a1d5058587fb2c');
var channel = pusher.subscribe('condor_channel');
channel.bind('my_event', function(data) {
      alert(data);
});