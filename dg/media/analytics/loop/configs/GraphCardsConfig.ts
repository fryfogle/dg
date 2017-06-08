export const cardGraphConfig = {
    'solid_gauge' : {
        chart: {
            type: 'solidgauge',
            width: 180,
            height: 100,
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            margin: [-10, 0, 0, 0]
        },

        title: '',

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
    
        tooltip: {
            enabled: false
        },

        exporting: { 
            enabled: false 
        },
        // the value axis
        yAxis: {
            stops: [
                [0.1, '#DF5353'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#55BF3B'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            labels: {
                y: 16
            },
            min: 0,
            max: 100
        },
    
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        },
    
        credits: {
            enabled: false
        },
    
        series: [{
            name:'present',
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color: black' +
                        '">{y}</span><br/>'
            },
            tooltip: {
                valueSuffix: null
            },
        }]
    },
    
}