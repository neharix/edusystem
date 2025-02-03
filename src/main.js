import 'virtual:uno.css'
import "./assets/css/tailwind.css";
import "./assets/css/base.css";

import {createApp} from "vue";
import {createPinia} from "pinia";
import {createYmaps} from "vue-yandex-maps";
import VueApexCharts from "vue3-apexcharts"

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createYmaps({
  apikey: '355f7362-a162-456b-a40d-a024f66986fd',
  version: "3.0"
}));

app.use(createPinia());
app.use(router);
app.use(VueApexCharts)

app.mount("#app");
