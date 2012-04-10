var chart;
var parsed_names = new Array();
var parsed_data = new Array();

var metric_id = document.getElementById('metric_id').getAttribute('value');

var i = 0;

console.log("fjweiifow");

for (var key in data) {
	var data_item = data[key];
	for (var parsed_key in data_item) {
		parsed_names[i] = parsed_key.replace("Z",".");
		parsed_data[i++] = data_item[parsed_key][0];
		console.log("fjweiifow");
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            type: 'column'
        },
        title: {
            text: '100M_np_base benchmark chart for '+metric_id
        },
        xAxis: {
            categories:parsed_names,
            labels: {
                rotation: -90,
                align: 'right'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Metric'
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function() {
                return ''+
                    this.x +': '+ this.y +' mm';
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
            series: [{
            name: 'Experiment 1',
            data: parsed_data

        },]
    });
});
