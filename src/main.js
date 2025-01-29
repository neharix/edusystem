import "./assets/css/tailwind.css";
import "./assets/css/flowbite.css";
import "./assets/css/base.css";

import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-dt';
import 'datatables.net-select-dt';
import 'datatables.net-responsive-dt';

import {createApp} from "vue";
import {createPinia} from "pinia";
import VueApexCharts from "vue3-apexcharts"

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

DataTable.use(DataTablesCore);

app.use(createPinia());
app.use(router);
app.use(VueApexCharts)

app.mount("#app");
