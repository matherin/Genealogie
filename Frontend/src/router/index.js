import { createRouter, createWebHistory } from "vue-router";

import Login from "./../components/login/Login.vue";

import ChangePassword from "./../components/main/settings/changePassword.vue";
import Profile from "./../components/main/settings/Profile.vue";
import NutzerverwaltungMain from "@/components/main/Nutzerverwaltung/NutzerverwaltungMain.vue";
import Nutzerverwaltung from "@/components/main/Nutzerverwaltung/Nutzerverwaltung.vue";
import SettingsMain from "./../components/main/settings/SettingsMain.vue";
import Kundenverwaltung from "@/components/main/Kundenverwaltung/Kundenverwaltung.vue";
import KundenverwaltungMain from "@/components/main/Kundenverwaltung/KundenverwaltungMain.vue";

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
      { path: "nutzertabelle", component: Nutzerverwaltung },
    ],
  },
  
  {
    path: "/kundenverwaltung",
    name: "Kunden",
    component: KundenverwaltungMain,
    children: [
      { path: "kundentabelle", component: Kundenverwaltung },
    ],
  },
  {
    path: "/einstellungen",
    name: "Einstellungen",
    component: SettingsMain,
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
