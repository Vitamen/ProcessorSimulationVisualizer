var chart;

var benchmarks = new Array();
$('.benchmark').each(function() {
	benchmarks.push(this.getAttribute('value'))
})
console.log(benchmarks)
var metric_id = document.getElementById('metric_id').getAttribute('value');
console.log(metric_id)
var upperStack = data.slice(0);
var visible_names = new Array();
var visible_data = new Array();
var lowerStack = new Array();

for (var i = 0; i < data.length; i++) {
	var data_item = data.shift();
	for (var parsed_key in data_item) {
		parsed_name = parsed_key.replace("Z",".").replace("Z",".");
		
		if (benchmarks.indexOf(parsed_name) > -1) {
			visible_names.push(parsed_name);
			visible_data.push(data_item[parsed_key][0]);
		}
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
        	backgroundColor: '#F8F8F8',
            renderTo: 'container',
            type: 'column',
            /*
            events: {
                click: function() {
                	var series = this.series[0];
                    var data_object = upperStack.shift();
                    var scrolling_parsed_data_point;
                    var scrolling_parsed_name;
                    var categories = this.xAxis[0].categories;
                    
                    for (var key in data_object) {
                    	scrolling_parsed_data_point = data_object[key];
                    	scrolling_parsed_name = key.replace("Z",".");
                    };
	                
                    categories.push(scrolling_parsed_name);
                    series.addPoint(scrolling_parsed_data_point);
     
                    console.log(visible_names.length);
                    chart.redraw();
                }
            },
            */
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
        series: [{
            name: 'Experiment 1',
            data: visible_data
        },
        ]
    });
});