<template>
    <div class="se-main-container">
      <div class="map-container">
        <l-map :useGlobalLeaflet="false" ref="map" v-model:zoom="zoom" :max-bounds="bounds" :max-bounds-viscosity="1.0" :center="center">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap"></l-tile-layer>
      </l-map>
      </div>
    </div>
  </template>
  
  <script>
  import "leaflet/dist/leaflet.css";
  import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

  export default {
    name: "Settings",
    components: {
      LMap,
      LTileLayer
    },
    data() {
      return {
        zoom: 3,
        center: [40.4406, -79.9959],
        bounds: [
          [-90, -1000000],
          [90, 10000000]
        ],
      }
  }
}
  </script>
  
  <style>
  .se-main-container {
    display: flex;
    width: 100vw;
    min-width: 1000px;
    height: calc(100vh - 56px);
    min-height: 700px;
    align-items: center;
    justify-content: center;
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

  .map-container {
    width: 90%;
    height: 80%;
  }
  </style>
  