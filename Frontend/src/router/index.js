import { createRouter, createWebHistory } from "vue-router";

import CensusData from "@/components/main/Nutzerverwaltung/CensusData.vue";
import CensusDataMain from "@/components/main/Nutzerverwaltung/CensusDataMain.vue";
import SettingsMain from "./../components/main/settings/SettingsMain.vue";

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
    path: "/settings",
    name: "Settings",
    component: SettingsMain
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
