<template>
    <div class="header-container">
      <div class="header-container-view">
        <div class="header-container-right">
          <div class="header-container-profile">
            <Button
              class="header-container-profile-button"
              type="button"
              icon="pi pi-user"
              @click="profileToggle"
              aria-haspopup="true"
              aria-controls="overlay_menu"
            />
            <Menu
              class="options-p-menu"
              ref="menu"
              id="profileMenu"
              :model="profileItems"
              :popup="true"
              append-to="body"
            >
              <template #submenulabel="{ item }">
                <span class="text-primary-font-bold">{{ item.label }}</span>
              </template>
            </Menu>
          </div>
          <div class="header-container-bar">
            <router-link
              :class="{ routeractive: isActive('/nutzerverwaltung') }"
              v-if="permissionLevel === 'admin'"
              class="header-container-bar-item"
              to="/nutzerverwaltung/übersicht"
            >
              Verwaltung</router-link
            >
          </div>
        </div>
        <div class="header-container-logo">
          <div class="header-container-logo-art"></div>
          <p class="header-container-logo-text" @click="onTitleClick">Metcera-Recycling</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import { useRoute } from "vue-router";
  import Menu from "primevue/menu";
  import Button from "primevue/button";
  import { getSessionCookies } from "@/components/custom/cookies/CookieService";
  
  export default {
    name: "AppHeader",
    components: {
      Menu,
      Button,
    },
    data() {
      return {
        permissionLevel: "admin", //temp hardcode permission
        profileItems: [
          {
            label: "Einstellungen",
            items: [
              {
                label: "Profil",
                icon: "pi pi-user",
                command: () => {
                  this.$router.push("/einstellungen/Profil");
                },
              },
              {
                label: "Passwort ändern",
                icon: "pi pi-key",
                command: () => {
                  this.$router.push("/einstellungen/passwort");
                },
              },
            ],
          },
          {
            separator: true,
          },
          {
            items: [
              {
                label: "Logout",
                icon: "pi pi-sign-out",
                command: () => {
                  this.delete_cookie("Session");
                  this.$router.push("/login");
                },
              },
            ],
          },
        ],
        route: useRoute(),
        state,
      };
    },
    mounted() {
      const session = getSessionCookies();
      if (session?.aud) this.permissionLevel = session.aud;
    },
    methods: {
      delete_cookie(name) {
        document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      },
      profileToggle(event) {
        this.$refs.menu.toggle(event);
      },
      onTitleClick() {
        this.$router.push("/login");
      },
      isActive(prefix) {
        return this.route.path.startsWith(prefix);
      },
    },
  };
  
  const state = ref("Gruppenleitung");
  </script>
  
  <style>
  .test-in-dev {
    color: #ffffffb0;
  }
  
  .header-container {
    background-color: #304858;
    color: #fff;
    margin: 0px;
    border: 0px;
    width: 100%;
    min-width: 1250px;
    display: flex;
    z-index: 2;
  }
  
  .header-container-view {
    display: flex;
    width: 100vw;
    min-width: 700px;
    padding-left: 17px;
    padding-right: 20px;
    padding-top: 17px;
    padding-bottom: 20px;
    flex-direction: row-reverse;
    justify-content: space-between;
    z-index: 2;
  }
  
  .header-container-right {
    display: flex;
    position: relative;
    flex-direction: row-reverse;
  }
  
  .header-container-logo {
    margin-left: 0px;
    display: flex;
    position: relative;
    width: 20%;
    height: 100%;
  }
  
  .header-container-logo-text {
    position: absolute;
    font-family: var(--font-family2);
    margin-left: 6px;
    font-size: var(--font-size-regular);
    user-select: none;
    cursor: pointer;
    color: #fff;
    letter-spacing: -0.5px;
  }
  
  .header-container-logo-art {
    position: absolute;
    height: 20px;
    width: 2px;
    background-color: var(--color-secondary);
    margin-top: 3px;
    margin-left: 3px;
  }
  
  .header-container-profile {
    position: relative;
    width: 25px;
    padding-bottom: 19px;
  }
  
  .header-container-profile-button {
    display: flex;
    align-items: center;
    position: absolute !important;
    border-radius: 100px !important;
    padding: 10px;
    padding-left: 15px;
    padding-right: 15px;
    top: 50%;
    transform: translate(-50%, -50%);
    right: -34px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    background: none !important;
    border-color: #ffffff00 !important;
  }
  
  .header-container-profile-button:hover {
    background-color: #ffffff2c !important;
    border: none !important;
  }
  
  .header-container-profile-button:active {
    background-color: #ffffff5b !important;
  }
  
  .header-container-profile-button-item {
    font-size: var(--font-size-normal);
    font-weight: 400;
    top: 50%;
    bottom: 50%;
    color: #ffffff;
    user-select: none;
    margin-right: 10px;
  }
  
  .header-container-bar {
    display: flex;
    margin-right: 6vw;
  }
  
  .header-container-bar-item {
    position: relative;
    margin-left: 20px;
    margin-right: 20px;
    cursor: pointer;
    font-size: var(--font-size-normal);
    font-weight: 500;
    letter-spacing: 0px;
    color: #ffffffb0;
  
    text-decoration: none;
    font-family: var(--font-family);
  
    transition: color 0.3s ease;
  }
  
  .header-container-bar-item:hover {
    color: #fff;
  }
  
  .header-container-bar-item::after {
    position: absolute;
    content: "";
    height: 2px;
    background-color: #ff9100;
    left: 1px;
    bottom: -1px;
    width: 0px;
    border-radius: 0px;
    transition: width 0.3s ease;
  }
  
  .routeractive {
    color: #ffffff;
  }
  
  .routeractive::after {
    width: 1rem;
  }
  
  .options-p-menu {
    box-shadow: none !important;
    top: 74px !important;
    transition-duration: 0.08s !important;
  }
  </style>
  