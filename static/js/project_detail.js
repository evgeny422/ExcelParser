var chart = c3.generate({
    bindto: '#chart',

    data: {

        columns: [

            projectData['y1'],
            projectData['y2'],
            projectData['y3'],
        ],

        types: {
            "Статус": "bar",
            "Дедлайн": "bar",
            "План": "bar",
        }
    },

});


// let projectData = {
//     'x': ['x', '2022-11-30', '2022-12-09', '2022-12-26', '2023-01-30'],
//     'y1': ['Статус', '3', '16', '26', '35'],
//     'y2': ['Дедлайн', '0', '0', '14', '0'],
//     'y3': ['План', '24', '27', '34', '39']
// }

const getOrCreateLegendList = (chart, id) => {
    const legendContainer = document.getElementById(id);
    let listContainer = legendContainer.querySelector('#project-chart-legend');

    console.log(legendContainer);

    if (!listContainer) {
        listContainer = document.createElement('ul');
        listContainer.classList = 'project-chart-legend';
        legendContainer.appendChild(listContainer);
    }

    return listContainer;
};

let labels = projectData['x'].splice(1, projectData['x'].length);

const ctx = document.getElementById('project-chart');

let chartJs = new Chart(ctx, {
    type: 'bar',
    columns: projectData['x'].splice(1, projectData['x'].length),
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Статус',
                data: projectData['y1'].splice(1, projectData['y1'].length),
                backgroundColor: '#98B2E5'
                // borderWidth: 1
            },
            {
                label: 'Дедлайн',
                data: projectData['y2'].splice(1, projectData['y2'].length),
                backgroundColor: '#ED9C87'
                // borderWidth: 1
            },
            {
                label: 'План',
                data: projectData['y3'].splice(1, projectData['y3'].length),
                backgroundColor: '#FECA7E'
                // borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                gridLines: {
                    display: false
                }
            }
        },
        plugins: {
            htmlLegend: {
                // ID of the container to put the legend in
                containerID: 'legend-colors',
            },
            legend: {
                display: false,
            }
        }
    },
    plugins: [{
        id: 'htmlLegend',
        afterUpdate(chart, args, options) {
            const ul = getOrCreateLegendList(chart, options.containerID);

            // Remove old legend items
            while (ul.firstChild) {
                ul.firstChild.remove();
            }

            // Reuse the built-in legendItems generator
            const items = chart.options.plugins.legend.labels.generateLabels(chart);

            items.forEach(item => {
                const li = document.createElement('li');
                li.classList = 'color text-center';

                li.onclick = () => {
                    const {type} = chart.config;
                    if (type === 'pie' || type === 'doughnut') {
                        // Pie and doughnut charts only have a single dataset and visibility is per item
                        chart.toggleDataVisibility(item.index);
                    } else {
                        chart.setDatasetVisibility(item.datasetIndex, !chart.isDatasetVisible(item.datasetIndex));
                    }
                    chart.update();
                };

                // Color box
                const boxSpan = document.createElement('div');
                boxSpan.classList = 'project-graph-color';
                boxSpan.style.background = item.fillStyle;
                boxSpan.style.borderColor = item.strokeStyle;
                boxSpan.style.borderWidth = item.lineWidth + 'px';

                // Text
                const textContainer = document.createElement('div');
                textContainer.classList = 'color-title';
                textContainer.style.color = item.fontColor;
                textContainer.style.textDecoration = item.hidden ? 'line-through' : '';

                const text = document.createTextNode(item.text);
                textContainer.appendChild(text);

                li.appendChild(boxSpan);
                li.appendChild(textContainer);
                ul.appendChild(li);
            });
        }
    }]
});

