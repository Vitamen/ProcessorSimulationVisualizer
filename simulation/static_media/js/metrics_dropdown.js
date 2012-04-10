var maxHeight = 600;

var metrics_list = $('#metrics_list');
for (var i=0; i < metrics.length; i++) {
	var metric = metrics[i];
	var metric_element = $('<option>').append(document.createTextNode(metric));
	metrics_list.append(metric_element);
}