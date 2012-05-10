var chart;

var benchmarks = new Array();
$('.benchmark').each(function() {
	console.log("benchmark");
	benchmarks.push(this.getAttribute('value'))
})

var experiments = new Array();
$('.experiment').each(function() {
	experiments.push(this.getAttribute('value'))
})

var metric_id = document.getElementById('metric_id').getAttribute('value');
var visible_names = new Array();
var visible_data = new Array();
var lowerStack = new Array();

var all_data = [];

for (var exp_i = 0; exp_i < experiments.length; exp_i++) {
	var data = datatest[experiments[exp_i]];
	var visible_data = [];
	for (var i = 0; i < data.length; i++) {
		var data_item = data[i];
		for (var parsed_key in data_item) {
			parsed_name = parsed_key.replace("Z",".").replace("Z",".");
			if (benchmarks.indexOf(parsed_name) > -1) {
				visible_names.push(parsed_name);
				visible_data.push(data_item[parsed_key][0]);
			}
		}
	}
	all_data.push({
		name: experiments[exp_i],
        data: visible_data
	})
}
console.log(all_data);

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
        	backgroundColor: '#F8F8F8',
            renderTo: 'container',
            type: 'column',
        },
        title: {
            text: ''
        },
        xAxis: {
            categories:visible_names,
            labels: {
                rotation: -90,
                align: 'right'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: metric_id
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
        series: all_data
    });
});