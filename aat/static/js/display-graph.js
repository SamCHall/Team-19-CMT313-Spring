function displayGraph(idName, title, data) {
    let layout = {title: title}
    let config = {
        displayModeBar: false,
        responsive: true
    }
    graph = document.getElementById(idName);
    Plotly.newPlot(graph, data, layout, config)
}
