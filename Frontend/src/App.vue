<template>
    <div class="app-container">
      <Toast position="bottom-right"></Toast>
      <AppHeader v-if="$route.path !== '/login'" />
      <mainBody />
      <AppFooter v-if="$route.path !== '/login'" />
    </div>
  </template>
  
  <script>
  import mainBody from "./components/main/mainBody.vue";
  import AppHeader from "./components/main/header/Header.vue";
  import AppFooter from "./components/main/footer/Footer.vue";
  import Toast from "primevue/toast";
  
  import "./variables.css";
  
  export default {
    name: "App",
    components: {
      mainBody,
      AppHeader,
      AppFooter,
      Toast,
    },
  };
  </script>
  
  <style>
  * {
    margin: 0;
    font-family: var(--font-family);
  }
  #app {
    color: #2c3e50;
  }
  
  .app-container {
    min-width: 1000px;
    min-height: 700px;
  }
  </style>
  