<template>
  <div ref="chartContainer" class="chart-container">
  </div>
</template>

<script setup>
import * as d3 from "d3";
import {onBeforeUnmount, onMounted, ref, watch} from "vue";


const chartContainer = ref(null);
const svg = ref(null);
const data = {
  nodes: [
    {id: "Институт", group: 1},
    {id: "Факультет 1", group: 2},
    {id: "Факультет 2", group: 2},
    {id: "Кафедра 1", group: 3},
    {id: "Кафедра 2", group: 3},
    {id: "Кафедра 3", group: 3},
    {id: "Специализация 1", group: 4},
    {id: "Специализация 2", group: 4},
    {id: "Специализация 3", group: 4},
    {id: "Специализация 4", group: 4},
  ],
  links: [
    {source: "Институт", target: "Факультет 1"},
    {source: "Институт", target: "Факультет 2"},
    {source: "Факультет 1", target: "Кафедра 1"},
    {source: "Факультет 1", target: "Кафедра 2"},
    {source: "Факультет 2", target: "Кафедра 3"},
    {source: "Кафедра 1", target: "Специализация 1"},
    {source: "Кафедра 1", target: "Специализация 2"},
    {source: "Кафедра 2", target: "Специализация 3"},
    {source: "Кафедра 3", target: "Специализация 4"},
  ],
};

const colorScale = d3.scaleOrdinal(["#ff4d4f", "#ffa940", "#36cfc9", "#597ef7"]);

// Объявляем функцию handleZoom перед её использованием
const handleZoom = (event) => {
  svg.value.selectAll("g").attr("transform", event.transform);
};

const zoom = d3.zoom().scaleExtent([0.5, 3]).on("zoom", handleZoom);

const resizeGraph = () => {
  const width = chartContainer.value.clientWidth;
  const height = chartContainer.value.clientHeight;

  // Обновляем размеры viewBox для SVG, чтобы графика адаптировалась
  svg.value
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet");
};

onMounted(() => {
  svg.value = d3
    .select(chartContainer.value)
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("viewBox", "0 0 800 600")
    .attr("preserveAspectRatio", "xMidYMid meet")
    .call(zoom); // Применяем масштабирование

  // Добавляем маркер стрелки
  svg.value
    .append("defs")
    .append("marker")
    .attr("id", "arrowhead")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr("fill", "#333");

  const simulation = d3
    .forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id((d) => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(800 / 2, 600 / 5))
    .force("y", d3.forceY().strength(0.1))
    .on("tick", ticked);

  const link = svg.value
    .append("g")
    .attr("stroke-width", 2)
    .selectAll("line")
    .data(data.links)
    .join("line")
    .attr("stroke", "#333")
    .attr("marker-end", "url(#arrowhead)");

  const node = svg.value
    .append("g")
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
    .attr("r", 10)
    .attr("fill", (d) => colorScale(d.group))
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .call(
      d3
        .drag()
        .on("start", dragStarted)
        .on("drag", dragged)
        .on("end", dragEnded)
    );

  const label = svg.value
    .append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
    .attr("dy", 4)
    .attr("x", 12)
    .text((d) => d.id)
    .style("font-size", "12px")
    .style("fill", "#000");

  function ticked() {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

    label.attr("x", (d) => d.x).attr("y", (d) => d.y);
  }

  function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  // Перерасчет при изменении размера
  resizeGraph();
  window.addEventListener("resize", resizeGraph);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeGraph);
});
</script>

<style>
.chart-container {
  width: 100%;
  height: 35vh;
  overflow: hidden;
  position: relative;
}
</style>
