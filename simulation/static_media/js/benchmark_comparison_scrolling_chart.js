var chart;

var metric_id = document.getElementById('metric_id').getAttribute('value');

var upperStack = data.slice(0);
var visible_names = new Array();
var visible_data = new Array();
var lowerStack = new Array();

for (var i = 0; i < 10; i++) {
	var data_item = upperStack.shift();
	for (var parsed_key in data_item) {
		visible_names.push(parsed_key.replace("Z","."));
		visible_data.push(data_item[parsed_key][0]);
	}
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            type: 'column',
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
        },
        title: {
            text: '100M_np_base benchmark chart for core_insn_fetched and core_insn_fetched_onpath'
        },
        xAxis: {
            categories:visible_names
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Rainfall (mm)'
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