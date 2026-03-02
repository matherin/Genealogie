import { createRouter, createWebHistory } from "vue-router";

import CensusData from "@/components/main/CensusData/CensusData.vue";
import CensusDataMain from "@/components/main/CensusData/CensusDataMain.vue";
import Map from "@/components/main/map/Map.vue";

const routes = [
  {
    path: "/",
    redirect: "/censusData/table",
  },
  {
    path: "/censusData",
    name: "Census",
    component: CensusDataMain,
    children: [
      { path: "table", component: CensusData },
    ],
  },
  {
    path: "/map",
    name: "Map",
    component: Map
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
