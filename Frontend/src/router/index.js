import { createRouter, createWebHistory } from "vue-router";

import Login from "./../components/login/Login.vue";

import ChangePassword from "./../components/main/settings/changePassword.vue";
import Profile from "./../components/main/settings/Profile.vue";
import Einstellungen from "./../components/main/settings/SettingsMain.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },/*
  {
    path: "/verwaltung",
    name: "Verwaltung",
    component: VerwaltungMain,
    children: [
     // { path: "standorte", component: Standortverwaltung, props: true },
      { path: "nutzer", component: Nutzerverwaltung },
      //{ path: "abrechnungen", component: AbrechnungMain },
    ],
  }*/,
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
  mode: "history",
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
