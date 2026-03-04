<template>
  <div class="se-main-container">
    <div class="map-container">
      <l-map :useGlobalLeaflet="false" ref="map" v-model:zoom="zoom" :max-bounds="bounds" :max-bounds-viscosity="1.0"
        :center="center">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" />
          <l-marker v-if="coords.person" :lat-lng="(coords.person)">
            <l-popup>Birthplace</l-popup>
          </l-marker>
          <l-marker v-if="father" :lat-lng="coords.father" />
          <l-marker v-if="mother" :lat-lng="coords.mother" />
          <l-polyline v-if="coords.mother && coords.person" :lat-lngs="[coords.mother, coords.person]" :options="lineStyle()"/>
          <l-polyline v-if="coords.father && coords.person" :lat-lngs="[coords.father, coords.person]" :options="lineStyle()"/>
      </l-map>
    </div>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPolyline, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  name: "Settings",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolyline,
    LPopup
  },
  data() {
    return {
      zoom: 3,
      center: [40.4406, -79.9959],
      bounds: [
        [-90, -1000000],
        [90, 10000000]
      ],
      testData: {
        person: "Pittsburgh",
        father: "Germany",
        mother: "Ireland"
      },
      coords: {
        person: null,
        father: null,
        mother: null
      }
    }
  },
  async mounted(){
    this.coords.person = await this.geocode(this.testData.person);
    this.coords.mother = await this.geocode(this.testData.mother);
    this.coords.father = await this.geocode(this.testData.father);
  },
  methods: {
    async geocode(place) {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${place}`);
      const data = await res.json();
      if (!data.length) return null;
      return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
    },
    lineStyle(){
      return{
        color: "#e63946",
        weight: 2,
        opacity: 0.8
      };
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