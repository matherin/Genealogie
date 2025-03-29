import { createRouter, createWebHistory } from "vue-router";

import Login from "./../components/login/Login.vue";

import ChangePassword from "./../components/main/settings/changePassword.vue";
import Profile from "./../components/main/settings/Profile.vue";
import Einstellungen from "./../components/main/settings/SettingsMain.vue";
import NutzerverwaltungMain from "@/components/main/Nutzerverwaltung/NutzerverwaltungMain.vue";
import Nutzerverwaltung from "@/components/main/Nutzerverwaltung/Nutzerverwaltung.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/nutzerverwaltung",
    name: "Nutzer",
    component: NutzerverwaltungMain,
    children: [
     // { path: "standorte", component: Standortverwaltung, props: true },
      { path: "übersicht", component: Nutzerverwaltung },
      //{ path: "abrechnungen", component: AbrechnungMain },
    ],
  },
  {
    path: "/einstellungen",
    name: "Einstellungen",
    component: Einstellungen,
    children: [
      { path: "passwort", component: ChangePassword },
      { path: "profil", component: Profile },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
