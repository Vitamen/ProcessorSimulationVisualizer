var chart;

var benchmark = "";
$('.benchmark').each(function() {
	benchmark = this.getAttribute('value');
})

var experiment = "";
$('.experiment').each(function() {
	experiment = this.getAttribute('value');
})

var metric_id = document.getElementById('metric_id').getAttribute('value');

var visible_data = new Array();

var all_data = [];
var dataname = experiment+benchmark;
var data = datatest[dataname];

for (var i = 0; i < data.length; i++) {
	visible_data.push([i,data[i]]);
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
        	backgroundColor: '#F8F8F8',
            renderTo: 'container',
            type: 'scatter',
        },
        title: {
            text: ''
        },
        xAxis: {
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
        	scatter: {
				marker: {
					radius: 3,
					states: {
						hover: {
							enabled: true,
							lineColor: 'rgb(100,100,100)'
						}
					}
				},
				states: {
					hover: {
						marker: {
							enabled: false
						}
					}
				}
			}
        },
        series: [{
            name: 'Female',
            color: 'rgba(223, 83, 83, .5)',
            data: visible_data
        }]
    });
});