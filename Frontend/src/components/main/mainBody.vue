<template>
    <div class="main-container">
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: "mainBody",
    components: {},
  };
  </script>
  
  <style scoped>
  .main-container {
    min-height: 100%;
    min-width: 100%;
  }
  </style>
  