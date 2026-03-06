<template>
  <div class="se-main-container">
    <Toast ref="toast" />
    <div class="map-container">
      <l-map :useGlobalLeaflet="false" ref="map" v-model:zoom="zoom" :max-bounds="bounds" :max-bounds-viscosity="1.0"
        :center="center">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" />
        <l-marker v-for="m in markers" :key="m.name" :lat-lng="m.coords">
          <l-popup>
            <b>{{ m.name }}</b><br>
            Person birthplace: {{ m.person }}<br>
            Mother birthplace: {{ m.mother }}<br>
            Father birthplace: {{ m.father }}
          </l-popup>
        </l-marker>
      </l-map>
    </div>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import Toast from "@/components/custom/toast/Toast.vue";

var baseUrl = window.location.origin;

export default {
  name: "Settings",
  components: {
    LMap,
    LTileLayer,
    LMarker,
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
      places: {}
    }
  },
  computed: {
    markers() {
      if (!this.places) return [];
      return Object.entries(this.places)
        .filter(([_, p]) => p.coords)
        .map(([name, p]) => ({
          name,
          coords: p.coords,
          person: p.person,
          mother: p.mother,
          father: p.father
        }));
    }
  },
  async mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch(`${baseUrl}/api/1880/pob-count`, {
          method: "GET",
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log(data);
        const mergedPlaces = this.mergedPlaces(data);
        this.places = await this.geocodePlaces(mergedPlaces);
      } catch (error) {
        console.error("Error fetching data:", error);
        this.$refs.toast.toastAddError("Data could not load");
      }
    },
    mergePlaces(data) {

      const places = {};

      const allPlaces = new Set([
        ...Object.keys(data.person || {}),
        ...Object.keys(data.mother || {}),
        ...Object.keys(data.father || {})
      ]);

      allPlaces.forEach(place => {
        places[place] = {
          person: data.person?.[place] || 0,
          mother: data.mother?.[place] || 0,
          father: data.father?.[place] || 0,
          coords: null
        };
      });

      return places;
    },
    async geocodePlaces(places) {

      for (const place in places) {

        const res = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${place}`
        );

        const data = await res.json();

        if (data.length) {
          places[place].coords = [
            parseFloat(data[0].lat),
            parseFloat(data[0].lon)
          ];
        }
      }

      return places;
    },
    lineStyle() {
      return {
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