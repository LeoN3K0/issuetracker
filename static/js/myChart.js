$(document).ready(function(){
    var endpoint = '/api/chart/data'
    var chart1Labels = []
    var chart1Data = []
    var borderWidth1 = 1
    var borderWidth2 = 1
    var chart2Labels = []
    var chart2Data = []
    var chart3Labels = []
    var chart3Data = []
    var chart3Data1 = []
    var chart3Data2 = []
    var chart4Labels = []
    var chart4Data= []
    var d = new Date();
    var year = d.getFullYear();
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            chart1Data = data.cht1data
            chart1Labels = data.cht1labels
            chart2Data = data.cht2data
            chart2Labels = data.cht2labels
            chart3Labels = data.cht3labels
            chart3Data  = data.cht3data
            chart3Data1 = data.cht3data1
            chart3Data2 = data.cht3data2
            chart4Labels = data.cht4labels
            chart4Data = data.cht4data
             if (chart1Data.every(item => item === 0)){
                borderWidth1 = 0
             }
            setChart1()
            if (chart2Data.every(item => item === 0)){
                borderWidth2 = 0
             }
            setChart2()
            setChart3()
            setChart4()
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        }
    })

    function setChart1(){
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chart1Labels,
                datasets: [{
                    label: '# of Tickets',
                    data: chart1Data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                    ],
                    borderWidth: borderWidth1,
                    borderAlign: 'inner',

                }]
            },
            options: {
              title: {
                display: false,
                text: 'Overall Activity'
              },
              animation: {
                onComplete: function(animation) {
                    if (chart1Data.every(item => item === 0)) {
                        document.getElementById('no-data').style.display = 'block';
                    }
                    else{
                        document.getElementById('no-data').style.display = 'none';
                    }
                }
              },
              tooltips: {
                callbacks: {
                  label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue/total*100).toFixed(1));
                    return currentValue + ' (' + percentage + '%)';
                  },
                  title: function(tooltipItem, data) {
                    return data.labels[tooltipItem[0].index];
                  }
                }
              },
            }
        });
    }

    function setChart2(){
        const ctx = document.getElementById('myChart2').getContext('2d');
        const myChart2 = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: chart2Labels,
                datasets: [{
                    label: '# of Tickets',
                    data: chart2Data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(106, 27, 154, 0.2)',
                        'rgba(255, 87, 34, 0.2)',
                        'rgba(0, 200, 83, 0.2)',
                        'rgba(30, 136, 229, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(106, 27, 154, 1)',
                        'rgba(255, 87, 34, 1)',
                        'rgba(0, 200, 83, 1)',
                        'rgba(30, 136, 229, 1)',

                    ],
                    borderWidth: borderWidth2,
                    borderAlign: 'inner',

                }]
            },
            options: {
              title: {
                display: false,
                text: 'Overall Activity'
              },
              animation: {
                onComplete: function(animation) {
                    if (chart2Data.every(item => item === 0)) {
                        document.getElementById('display-no-data').style.display = 'block';
                    }
                    else{
                        document.getElementById('display-no-data').style.display = 'none';
                    }
                }
              },
              tooltips: {
                callbacks: {
                  label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue/total*100).toFixed(1));
                    return currentValue + ' (' + percentage + '%)';
                  },
                  title: function(tooltipItem, data) {
                    return data.labels[tooltipItem[0].index];
                  }
                }
              },
            }
        });
    }

     function setChart3(){
        const ctx = document.getElementById('myChart3').getContext('2d');
        const myChart3 = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chart3Labels,
                datasets: [{
                    type: 'bar',
                    label: 'Total',
                    data: chart3Data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 99, 132, 1)',
                        ]
                }, {
                    type: 'bar',
                    label: 'Fixed',
                    data: chart3Data1,
                    backgroundColor: [
                        'rgba(0, 200, 83, 0.2)',
                        'rgba(0, 200, 83, 0.2)',
                        'rgba(0, 200, 83, 0.2)',
                        'rgba(0, 200, 83, 0.2)',
                        ],
                    borderColor: [
                        'rgba(0, 200, 83, 1)',
                        'rgba(0, 200, 83, 1)',
                        'rgba(0, 200, 83, 1)',
                        'rgba(0, 200, 83, 1)',
                        ]
                },{
                    type: 'bar',
                    label: 'Closed',
                    data: chart3Data2,
                    backgroundColor: [
                        'rgba(30, 136, 229, 0.2)',
                        'rgba(30, 136, 229, 0.2)',
                        'rgba(30, 136, 229, 0.2)',
                        'rgba(30, 136, 229, 0.2)',
                        ],
                    borderColor: [
                        'rgba(30, 136, 229, 1)',
                        'rgba(30, 136, 229, 1)',
                        'rgba(30, 136, 229, 1)',
                        'rgba(30, 136, 229, 1)',
                        ]
                }],

            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                title: {
                    display: false,
                    text: 'Overall Activity'
                },
                animation: {
                onComplete: function(animation) {
                    if (chart3Data.every(item => item === 0) && chart3Data1.every(item => item === 0) && chart3Data2.every(item => item === 0) ) {
                        document.getElementById('no-data-message').style.display = 'block';
                    }
                    else{
                        document.getElementById('no-data-message').style.display = 'none';
                    }
                }
              },
            }
        });
    }

    function setChart4(){
        const ctx = document.getElementById('myChart4').getContext('2d');
        const myChart4 = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chart4Labels,
                datasets: [{
                    label: '# of Tickets ' + year,
                    data: chart4Data,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',

                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                title: {
                    display: false,
                    text: 'Overall Activity'
                },
                animation: {
                onComplete: function(animation) {
                    if (chart4Data.every(item => item === 0)) {
                        document.getElementById('no-data-clause').style.display = 'block';
                    }
                    else{
                        document.getElementById('no-data-clause').style.display = 'none';
                    }
                }
              },
            }
        });
    }
})