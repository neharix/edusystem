<script setup>
import 'leaflet/dist/leaflet.css';
import {watch, onMounted, ref} from "vue";
import L from "leaflet";
import {useHighSchoolsStore} from "@/stores/api.store.js";
import {storeToRefs} from "pinia";

const mapContainer = ref(null);
const map = ref(null);
const markers = ref([]); // Храним маркеры

const highSchoolsStore = useHighSchoolsStore();

const { highSchoolsResponse } = storeToRefs(highSchoolsStore);

highSchoolsStore.getAll();

const addMarker = (lat, lng, name) => {
  if (!map.value) return;

  const marker = L.marker([lat, lng]).addTo(map.value).bindPopup(name);
  markers.value.push(marker);
};

watch(highSchoolsResponse, (newValue, oldValue) => {
  newValue.forEach(({ lat, lng, name }) => {
    addMarker(lat, lng, name);
  });
})

onMounted(() => {
  map.value = L.map(mapContainer.value).setView([39.13, 59.37], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map.value);
});
</script>

<template>
  <div class="rounded-lg mb-6 shadow-md" ref="mapContainer" style="width: 100%; height: 70vh;"></div>
</template>


<style>
.leaflet-control-attribution {
  display: none !important;
}

.leaflet-pane, .leaflet-top, .leaflet-bottom{
  z-index: 10;
}

</style>
