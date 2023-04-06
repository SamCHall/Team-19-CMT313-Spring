function displayGraph(idName, title, data) {
    let layout = {title: title};
    let config = {
        displayModeBar: false,
        responsive: true
    };
    graph = document.getElementById(idName);
    Plotly.newPlot(graph, data, layout, config);
}

function barGraphData(data) {
    return [
        {
            x : Object.keys(data),
            y : Object.values(data),
            type : 'bar'
        }
    ];
}

function cohortBarGraphData(data) {
    let displayData = [];

    let i = 0;
    for ([cohort, mark_dist] of Object.entries(data)) {
        displayData[i] = {
            x : Object.keys(mark_dist),
            y : Object.values(mark_dist),
            name : cohort,
            type : 'bar'
        };
        i++;
    }

    return displayData;
}

function resize(graph) {
    Plotly.relayout(graph, {autosize: true});
}
