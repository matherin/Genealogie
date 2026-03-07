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
      places: {
        "Germany": { "coords": [51.1657, 10.4515], "person": 3094, "mother": 8580, "father": 9618 },
        "Baden": { "coords": [48.5, 8.5], "person": 1395, "mother": 3263, "father": 3847 },
        "Bavaria": { "coords": [48.7904, 11.4979], "person": 2654, "mother": 6545, "father": 6695 },
        "Hanover": { "coords": [52.3759, 9.7320], "person": 638, "mother": 1651, "father": 1695 },
        "Hesse": { "coords": [50.6521, 9.1624], "person": 1722, "mother": 4355, "father": 4716 },
        "Mecklenburg": { "coords": [53.6127, 12.4296], "person": 15, "mother": 20, "father": 22 },
        "Prussia": { "coords": [52.0, 18.0], "person": 4459, "mother": 9947, "father": 10876 },
        "Saxony": { "coords": [51.1045, 13.2017], "person": 432, "mother": 909, "father": 1070 },
        "Wertenburg": { "coords": [48.5373, 9.0410], "person": 1149, "mother": 2848, "father": 3085 },
        "Schleswig-Holstein": { "coords": [54.2194, 9.6961], "person": 28, "mother": 63, "father": 73 },

        "Alsace-Lorraine": { "coords": [48.5, 7.5], "person": 144, "mother": 364, "father": 394 },
        "Austria": { "coords": [47.5162, 14.5501], "person": 208, "mother": 320, "father": 363 },
        "Bohemia": { "coords": [49.8, 15.5], "person": 96, "mother": 156, "father": 161 },
        "Poland": { "coords": [51.9194, 19.1451], "person": 364, "mother": 589, "father": 629 },
        "Hungary": { "coords": [47.1625, 19.5033], "person": 53, "mother": 57, "father": 78 },
        "Russia": { "coords": [61.5240, 105.3188], "person": 259, "mother": 433, "father": 470 },
        "Italy": { "coords": [41.8719, 12.5674], "person": 242, "mother": 367, "father": 416 },
        "France": { "coords": [46.2276, 2.2137], "person": 279, "mother": 639, "father": 793 },
        "Spain": { "coords": [40.4637, -3.7492], "person": 11, "mother": 20, "father": 25 },
        "Portugal": { "coords": [39.3999, -8.2245], "person": 1, "mother": 1, "father": 3 },
        "Greece": { "coords": [39.0742, 21.8243], "person": 7, "mother": 14, "father": 14 },

        "England": { "coords": [52.3555, -1.1743], "person": 5053, "mother": 7987, "father": 8441 },
        "Ireland": { "coords": [53.1424, -7.6921], "person": 16442, "mother": 39922, "father": 42265 },
        "Scotland": { "coords": [56.4907, -4.2026], "person": 8, "mother": 26, "father": 13 },
        "Wales": { "coords": [52.1307, -3.7837], "person": 2030, "mother": 3941, "father": 3988 },

        "Norway": { "coords": [60.4720, 8.4689], "person": 14, "mother": 14, "father": 16 },
        "Sweden": { "coords": [60.1282, 18.6435], "person": 101, "mother": 145, "father": 161 },
        "Denmark": { "coords": [56.2639, 9.5018], "person": 6, "mother": 10, "father": 9 },
        "Switzerland": { "coords": [46.8182, 8.2275], "person": 584, "mother": 1333, "father": 1283 },
        "Luxembourg": { "coords": [49.8153, 6.1296], "person": 5, "mother": 7, "father": 5 },
        "Netherlands": { "coords": [52.1326, 5.2913], "person": 89, "mother": 217, "father": 260 },

        "Canada": { "coords": [56.1304, -106.3468], "person": 258, "mother": 249, "father": 223 },
        "Cuba": { "coords": [21.5218, -77.7812], "person": 15, "mother": 9, "father": 22 },

        "New York": { "coords": [43.0, -75.0], "person": 1644, "mother": 1563, "father": 1583 },
        "New Jersey": { "coords": [40.0583, -74.4057], "person": 640, "mother": 856, "father": 893 },
        "Pennsylvania": { "coords": [41.2033, -77.1945], "person": 97103, "mother": 40820, "father": 34170 },
        "Delaware": { "coords": [38.9108, -75.5277], "person": 81, "mother": 117, "father": 104 },
        "Maryland": { "coords": [39.0458, -76.6413], "person": 1276, "mother": 1811, "father": 1836 },
        "Virginia": { "coords": [37.4316, -78.6569], "person": 1816, "mother": 2590, "father": 2624 },
        "North Carolina": { "coords": [35.7596, -79.0193], "person": 26, "mother": 38, "father": 59 },
        "South Carolina": { "coords": [33.8361, -81.1637], "person": 51, "mother": 59, "father": 57 },
        "Georgia": { "coords": [32.1656, -82.9001], "person": 21, "mother": 25, "father": 37 },
        "Florida": { "coords": [27.6648, -81.5158], "person": 6, "mother": 4, "father": 8 },

        "Ohio": { "coords": [40.4173, -82.9071], "person": 2408, "mother": 1863, "father": 1618 },
        "Indiana": { "coords": [40.2672, -86.1349], "person": 252, "mother": 216, "father": 121 },
        "Illinois": { "coords": [40.6331, -89.3985], "person": 272, "mother": 100, "father": 70 },
        "Michigan": { "coords": [44.3148, -85.6024], "person": 102, "mother": 43, "father": 34 },
        "Wisconsin": { "coords": [43.7844, -88.7879], "person": 3, "mother": 11, "father": 15 },
        "Minnesota": { "coords": [46.7296, -94.6859], "person": 23, "mother": 3, "father": 10 },
        "Iowa": { "coords": [41.8780, -93.0977], "person": 102, "mother": 16, "father": 22 },
        "Missouri": { "coords": [37.9643, -91.8318], "person": 174, "mother": 111, "father": 60 },
        "Texas": { "coords": [31.9686, -99.9018], "person": 7, "mother": 1, "father": 1 },
        "California": { "coords": [36.7783, -119.4179], "person": 9, "mother": 2, "father": 2 }
      }
    }
  },
  computed: {
    markers() {
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
  },
  methods: {
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