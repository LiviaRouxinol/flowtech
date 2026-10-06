const grafico = new CanvasJS.Chart("grafico", {
    title: {
        text: "Temperatura"
    },

    axisY: {
        title: "Temperatura °C"
    },

    data: [
        {
            type: "line",

            dataPoints: [
                { x: 1, y: 25 },
                { x: 2, y: 27 },
                { x: 3, y: 26 },
                { x: 4, y: 29 },
                { x: 5, y: 30 }
            ]
        }
    ]
});

grafico.render();