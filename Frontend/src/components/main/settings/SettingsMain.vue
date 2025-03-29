<template>
    <div class="se-main-container">
      <div class="se-main-container-left">
        <Menu
          class="se-main-container-left-menu st-menu-custom"
          :model="verwaltungsItems"
        >
          <template #submenulabel="{ item }">
            <span class="text-primary-font-bold">{{ item.label }}</span>
          </template>
        </Menu>
      </div>
      <div class="se-main-container-right">
        <router-view />
      </div>
    </div>
  </template>
  
  <script>
  import Menu from "primevue/menu";
  import { useRoute } from "vue-router";
  
  export default {
    name: "SettingS",
    components: {
      Menu,
    },
    data() {
      return {
        route: useRoute(),
        verwaltungsItems: [
          {
            label: "Einstellungen",
            items: [
              {
                label: "Profil",
                icon: "pi pi-user",
                command: () => this.$router.push("/einstellungen/profil"),
              },
              {
                label: "Passwort ändern",
                icon: "pi pi-key",
                command: () => this.$router.push("/einstellungen/passwort"),
              },
            ],
          },
        ],
      };
    },
  
    methods: {},
  };
  </script>
  
  <style>
  .se-main-container {
    display: flex;
    width: 100vw;
    min-width: 1000px;
    height: calc(100vh - 56px);
    min-height: 700px;
  }
  
  .se-main-container-left {
    display: flex;
    flex-direction: column;
    max-height: 100vh;
    min-height: 700px;
    width: 14.6vw;
    min-width: 225px;
    max-width: 300px;
    padding: 40px;
    padding-left: 10px;
    padding-right: 10px;
    background-color: #fcfbfb;
    box-shadow: 0px 0px 60px rgba(0, 0, 0, 0);
    border-right: 1px solid #0000000f;
  }
  
  .se-main-container-left-menu {
    margin-bottom: 50px;
  }
  
  .se-main-container-right {
    display: flex;
    flex: 1;
  }
  
  .st-menu-custom {
    border: none !important;
    box-shadow: none !important;
    background: none !important;
    background-color: transparent !important;
  }
  </style>
  