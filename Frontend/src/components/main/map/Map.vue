<template>
  <div class="se-main-container">
    <Toast ref="toast" />
    <div class="radio-button-container">
      <div class="radio-button-container-individual" v-for="y in years" :key="y">
        <RadioButton v-model="year" :value="y" />
        <label>{{ y }}</label>
      </div>
    </div>
    <div class="map-container">
      <l-map :useGlobalLeaflet="false" ref="map" v-model:zoom="zoom" :center="center" :max-bounds="bounds"
        :max-bounds-viscosity="1.0">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" />
        <l-marker v-for="m in activeMarkers" :key="year + '-' + m.name" :lat-lng="m.coords">
          <l-popup>
            <b>{{ m.name }}</b><br>
            Person birthplace: {{ m.person }}<br>
            <span v-if="m.mother">Mother birthplace: {{ m.mother }}<br></span>
            <span v-if="m.father">Father birthplace: {{ m.father }}</span>
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
import RadioButton from "primevue/radiobutton";

var baseUrl = window.location.origin;

export default {
  name: "Settings",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    RadioButton,
    Toast
  },
  data() {
    return {
      zoom: 3,
      center: [40.4406, -79.9959],
      bounds: [
        [-90, -1000000],
        [90, 10000000]
      ],
      year: 1880,
      years: [1850, 1860, 1870, 1880],

      places1850: {
        "Africa": { coords: [0, 20], person: 3 },
        "Alabama": { coords: [32.8067, -86.7911], person: 6 },
        "Austria": { coords: [47.5162, 14.5501], person: 11 },
        "Bavaria": { coords: [48.7904, 11.4979], person: 3 },
        "Belgium": { coords: [50.5039, 4.4699], person: 2 },
        "CANADA W.": { coords: [53.7267, -127.6476], person: 1 },
        "Canada": { coords: [56.1304, -106.3468], person: 87 },
        "Connecticut": { coords: [41.6032, -73.0877], person: 93 },
        "Cuba": { coords: [21.5218, -77.7812], person: 10 },
        "Delaware": { coords: [38.9108, -75.5277], person: 65 },
        "Denmark": { coords: [56.2639, 9.5018], person: 5 },
        "East Indies": { coords: [0, 110], person: 2 },
        "England": { coords: [52.3555, -1.1743], person: 1759 },
        "France": { coords: [46.2276, 2.2137], person: 142 },
        "Georgia": { coords: [32.1656, -82.9001], person: 13 },
        "Germany": { coords: [51.1657, 10.4515], person: 6044 },
        "Great Britain": { coords: [54.0, -2.0], person: 4 },
        "High Seas": { coords: [0, 0], person: 12 },
        "Hungary": { coords: [47.1625, 19.5033], person: 1 },
        "Illegible": { coords: [0, 0], person: 18 },
        "Illinios": { coords: [40.6331, -89.3985], person: 17 },
        "Indiana": { coords: [40.2672, -86.1349], person: 38 },
        "Iowa": { coords: [41.878, -93.0977], person: 5 },
        "Ireland": { coords: [53.1424, -7.6921], person: 10016 },
        "Italy": { coords: [41.8719, 12.5674], person: 18 },
        "Kentuky": { coords: [37.8393, -84.270], person: 70 },
        "Latin America": { coords: [-8.7832, -55.4915], person: 2 },
        "Louisiana": { coords: [30.9843, -91.9623], person: 18 },
        "Maine": { coords: [45.2538, -69.4455], person: 25 },
        "Maryland": { coords: [39.0458, -76.6413], person: 568 },
        "Massachusetts": { coords: [42.4072, -71.3824], person: 181 },
        "Michigan": { coords: [44.3148, -85.6024], person: 8 },
        "Minnesota": { coords: [46.7296, -94.6859], person: 4 },
        "Mississippi": { coords: [32.3547, -89.3985], person: 6 },
        "Missouri": { coords: [37.9643, -91.8318], person: 54 },
        "N. BRUNSWICK": { coords: [46.5, -66.0], person: 5 },
        "N.FOUNDLAND": { coords: [53.1355, -57.6604], person: 1 },
        "NOVA SCOTIA": { coords: [44.6820, -63.7443], person: 11 },
        "Nasua": { coords: [0, 0], person: 1 },
        "Netherlands": { coords: [52.1326, 5.2913], person: 17 },
        "New Hampshire": { coords: [43.1939, -71.5724], person: 37 },
        "New Jorsey": { coords: [40.0583, -74.4057], person: 203 },
        "New Yyork": { coords: [43.2994, -74.2179], person: 526 },
        "Nort Carolina": { coords: [35.7596, -79.0193], person: 10 },
        "Not Given": { coords: [0, 0], person: 5 },
        "Ohio": { coords: [40.4173, -82.9071], person: 613 },
        "Pennsylvania": { coords: [41.2033, -77.1945], person: 23860 },
        "Poland": { coords: [51.9194, 19.1451], person: 25 },
        "Portugal": { coords: [39.3999, -8.2245], person: 1 },
        "Prussia": { coords: [52.0, 18.0], person: 50 },
        "Rhode Island": { coords: [41.5801, -71.4774], person: 13 },
        "Saxony": { coords: [51.1045, 13.2017], person: 2 },
        "Scotland": { coords: [56.4907, -4.2026], person: 350 },
        "South Carolina": { coords: [33.8361, -81.1637], person: 8 },
        "Spain": { coords: [40.4637, -3.7492], person: 1 },
        "Sweden": { coords: [60.1282, 18.6435], person: 5 },
        "Switzerland": { coords: [46.8182, 8.2275], person: 50 },
        "Tennessee": { coords: [35.5175, -86.5804], person: 30 },
        "Texas": { coords: [31.9686, -99.9018], person: 2 },
        "Vermont": { coords: [44.5588, -72.5778], person: 34 },
        "Virgina": { coords: [37.4316, -78.6569], person: 641 },
        "Wales": { coords: [52.1307, -3.7837], person: 739 },
        "Washington, D.C.": { coords: [38.9072, -77.0369], person: 88 },
        "Wisconsin": { coords: [43.7844, -88.7879], person: 1 }
      },
      places1860: {
        "Africa": { coords: [0, 20], person: 2 },
        "Alabama": { coords: [32.8067, -86.7911], person: 5 },
        "America": { coords: [39.8283, -98.5795], person: 3 },
        "Arkansas": { coords: [34.9697, -92.3731], person: 3 },
        "Asia": { coords: [34.0479, 100.6197], person: 2 },
        "Austria": { coords: [47.5162, 14.5501], person: 16 },
        "Baden": { coords: [48.5, 8.5], person: 346 },
        "Bavaria": { coords: [48.7904, 11.4979], person: 624 },
        "Belgium": { coords: [50.5039, 4.4699], person: 1 },
        "Bohemia": { coords: [49.8, 15.5], person: 6 },
        "CANADA E.": { coords: [45.4215, -75.6972], person: 5 },
        "CANADA W.": { coords: [53.7267, -127.6476], person: 9 },
        "Canada": { coords: [56.1304, -106.3468], person: 69 },
        "Connecticut": { coords: [41.6032, -73.0877], person: 50 },
        "Cuba": { coords: [21.5218, -77.7812], person: 13 },
        "Delaware": { coords: [38.9108, -75.5277], person: 36 },
        "Denmark": { coords: [56.2639, 9.5018], person: 1 },
        "England": { coords: [52.3555, -1.1743], person: 1281 },
        "Florida": { coords: [27.6648, -81.5158], person: 2 },
        "France": { coords: [46.2276, 2.2137], person: 234 },
        "Georgia": { coords: [32.1656, -82.9001], person: 2 },
        "Germany": { coords: [51.1657, 10.4515], person: 3538 },
        "Hanover": { coords: [52.3759, 9.7320], person: 269 },
        "Hesse": { coords: [50.6521, 9.1624], person: 396 },
        "High Seas": { coords: [0, 0], person: 12 },
        "Hungary": { coords: [47.1625, 19.5033], person: 1 },
        "Illegible": { coords: [0, 0], person: 18 },
        "Illinios": { coords: [40.6331, -89.3985], person: 35 },
        "Indiana": { coords: [40.2672, -86.1349], person: 37 },
        "Iowa": { coords: [41.8780, -93.0977], person: 26 },
        "Ireland": { coords: [53.1424, -7.6921], person: 9000 },
        "Isle Of Jersey": { coords: [49.2144, -2.1313], person: 1 },
        "Italy": { coords: [41.8719, 12.5674], person: 25 },
        "Kentuky": { coords: [37.8393, -84.2700], person: 77 },
        "Latin America": { coords: [-8.7832, -55.4915], person: 5 },
        "Louisiana": { coords: [30.9843, -91.9623], person: 20 },
        "Maine": { coords: [45.2538, -69.4455], person: 24 },
        "Maryland": { coords: [39.0458, -76.6413], person: 457 },
        "Massachusetts": { coords: [42.4072, -71.3824], person: 151 },
        "Mecklenburg": { coords: [53.6127, 12.4296], person: 6 },
        "Michigan": { coords: [44.3148, -85.6024], person: 14 },
        "Minnesota": { coords: [46.7296, -94.6859], person: 3 },
        "Mississippi": { coords: [32.3547, -89.3985], person: 13 },
        "Missouri": { coords: [37.9643, -91.8318], person: 30 },
        "N. BRUNSWICK": { coords: [46.5, -66.0], person: 12 },
        "N.FOUNDLAND": { coords: [53.1355, -57.6604], person: 5 },
        "NOVA SCOTIA": { coords: [44.6820, -63.7443], person: 10 },
        "Nasua": { coords: [0, 0], person: 1 },
        "Netherlands": { coords: [52.1326, 5.2913], person: 56 },
        "New England": { coords: [43.5, -70.5], person: 1 },
        "New Hampshire": { coords: [43.1939, -71.5724], person: 35 },
        "New Jorsey": { coords: [40.0583, -74.4057], person: 197 },
        "New Yyork": { coords: [43.2994, -74.2179], person: 494 },
        "Nort Carolina": { coords: [35.7596, -79.0193], person: 3 },
        "Not Given": { coords: [0, 0], person: 45 },
        "Ohio": { coords: [40.4173, -82.9071], person: 765 },
        "Oregon": { coords: [43.8041, -120.5542], person: 6 },
        "Pennsylvania": { coords: [41.2033, -77.1945], person: 26598 },
        "Poland": { coords: [51.9194, 19.1451], person: 16 },
        "Prussia": { coords: [52.0, 18.0], person: 256 },
        "Rhode Island": { coords: [41.5801, -71.4774], person: 29 },
        "Russia": { coords: [61.5240, 105.3188], person: 4 },
        "Saxony": { coords: [51.1045, 13.2017], person: 228 },
        "Schleswig-Holstein": { coords: [54.2194, 9.6961], person: 9 },
        "Scotland": { coords: [56.4907, -4.2026], person: 259 },
        "South Carolina": { coords: [33.8361, -81.1637], person: 7 },
        "Spain": { coords: [40.4637, -3.7492], person: 3 },
        "Sweden": { coords: [60.1282, 18.6435], person: 6 },
        "Switzerland": { coords: [46.8182, 8.2275], person: 172 },
        "Tennessee": { coords: [35.5175, -86.5804], person: 16 },
        "Texas": { coords: [31.9686, -99.9018], person: 4 },
        "Vermont": { coords: [44.5588, -72.5778], person: 27 },
        "Virgina": { coords: [37.4316, -78.6569], person: 475 },
        "Wales": { coords: [52.1307, -3.7837], person: 413 },
        "Washington, D.C.": { coords: [38.9072, -77.0369], person: 47 },
        "Wertenburg": { coords: [48.5373, 9.0410], person: 185 },
        "Wisconsin": { coords: [43.7844, -88.7879], person: 11 }
      },
      places1870: {
        "Alabama": { coords: [32.8067, -86.7911], person: 9 },
        "Alsace-Lorraine": { coords: [48.5, 7.5], person: 6 },
        "Arizona": { coords: [34.0489, -111.0937], person: 2 },
        "Arkansas": { coords: [34.9697, -92.3731], person: 4 },
        "Asia": { coords: [34.0479, 100.6197], person: 1 },
        "Austria": { coords: [47.5162, 14.5501], person: 101 },
        "Baden": { coords: [48.5, 8.5], person: 1194 },
        "Bavaria": { coords: [48.7904, 11.4979], person: 1508 },
        "Belgium": { coords: [50.5039, 4.4699], person: 7 },
        "Bohemia": { coords: [49.8, 15.5], person: 52 },
        "California": { coords: [36.7783, -119.4179], person: 7 },
        "Canada": { coords: [56.1304, -106.3468], person: 258 },
        "CANADA W.": { coords: [53.7267, -127.6476], person: 1 },
        "Central America": { coords: [15.7835, -90.2308], person: 1 },
        "Colorado": { coords: [39.5501, -105.7821], person: 1 },
        "Connecticut": { coords: [41.6032, -73.0877], person: 94 },
        "Cuba": { coords: [21.5218, -77.7812], person: 15 },
        "Delaware": { coords: [38.9108, -75.5277], person: 86 },
        "Denmark": { coords: [56.2639, 9.5018], person: 9 },
        "England": { coords: [52.3555, -1.1743], person: 2831 },
        "Florida": { coords: [27.6648, -81.5158], person: 4 },
        "France": { coords: [46.2276, 2.2137], person: 337 },
        "Georgia": { coords: [32.1656, -82.9001], person: 21 },
        "Germany": { coords: [51.1657, 10.4515], person: 1128 },
        "Greece": { coords: [39.0742, 21.8243], person: 1 },
        "Hanover": { coords: [52.3759, 9.732], person: 545 },
        "Hesse": { coords: [50.6521, 9.1624], person: 1052 },
        "Hungary": { coords: [47.1625, 19.5033], person: 12 },
        "Illinois": { coords: [40.6331, -89.3985], person: 107 },
        "Indiana": { coords: [40.2672, -86.1349], person: 101 },
        "Iowa": { coords: [41.878, -93.0977], person: 73 },
        "Ireland": { coords: [53.1424, -7.6921], person: 12884 },
        "Isle Of Jersey": { coords: [49.2144, -2.1313], person: 2 },
        "Italy": { coords: [41.8719, 12.5674], person: 83 },
        "Kansas": { coords: [39.0119, -98.4842], person: 6 },
        "Kentuky": { coords: [37.8393, -84.270], person: 192 },
        "Latin America": { coords: [-8.7832, -55.4915], person: 9 },
        "Louisiana": { coords: [30.9843, -91.9623], person: 39 },
        "Maine": { coords: [45.2538, -69.4455], person: 82 },
        "Maryland": { coords: [39.0458, -76.6413], person: 934 },
        "Massachusetts": { coords: [42.4072, -71.3824], person: 248 },
        "Mecklenburg": { coords: [53.6127, 12.4296], person: 11 },
        "Michigan": { coords: [44.3148, -85.6024], person: 40 },
        "Minnesota": { coords: [46.7296, -94.6859], person: 13 },
        "Mississippi": { coords: [32.3547, -89.3985], person: 13 },
        "Missouri": { coords: [37.9643, -91.8318], person: 84 },
        "Nebraska": { coords: [41.4925, -99.9018], person: 1 },
        "Netherlands": { coords: [52.1326, 5.2913], person: 122 },
        "Nevada": { coords: [38.8026, -116.4194], person: 1 },
        "New Hampshire": { coords: [43.1939, -71.5724], person: 48 },
        "New Jorsey": { coords: [40.0583, -74.4057], person: 284 },
        "New Yyork": { coords: [43.2994, -74.2179], person: 1035 },
        "New Zealand": { coords: [-40.9006, 174.886], person: 2 },
        "Nort Carolina": { coords: [35.7596, -79.0193], person: 20 },
        "Norway": { coords: [60.472, 8.4689], person: 3 },
        "Ohio": { coords: [40.4173, -82.9071], person: 1623 },
        "Pennsylvania": { coords: [41.2033, -77.1945], person: 50808 },
        "Poland": { coords: [51.9194, 19.1451], person: 49 },
        "Portugal": { coords: [39.3999, -8.2245], person: 1 },
        "Prussia": { coords: [52.5, 13.4], person: 2206 },
        "Rhode Island": { coords: [41.5801, -71.4774], person: 21 },
        "Russia": { coords: [61.524, 105.3188], person: 40 },
        "Saxony": { coords: [51.1045, 13.2017], person: 335 },
        "Schleswig-Holstein": { coords: [54.2194, 9.6961], person: 26 },
        "Scotland": { coords: [56.4907, -4.2026], person: 574 },
        "South Carolina": { coords: [33.8361, -81.1637], person: 32 },
        "Spain": { coords: [40.4637, -3.7492], person: 3 },
        "Sweden": { coords: [60.1282, 18.6435], person: 27 },
        "Switzerland": { coords: [46.8182, 8.2275], person: 329 },
        "Tennessee": { coords: [35.5175, -86.5804], person: 72 },
        "Texas": { coords: [31.9686, -99.9018], person: 3 },
        "Vermont": { coords: [44.5588, -72.5778], person: 65 },
        "Virgina": { coords: [37.4316, -78.6569], person: 999 },
        "Wales": { coords: [52.1307, -3.7837], person: 1000 },
        "Washington, D.C.": { coords: [38.9072, -77.0369], person: 86 },
        "Wertenburg": { coords: [48.6616, 9.3501], person: 746 },
        "West Virginia": { coords: [38.5976, -80.4549], person: 214 },
        "Wisconsin": { coords: [43.7844, -88.7879], person: 25 }
      },
      places1880: {
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
    };
  },
  computed: {
    activeMarkers() {
      let dataset;

      switch (this.year) {
        case 1850:
          dataset = this.places1850;
          break;
        case 1860:
          dataset = this.places1860;
          break;
        case 1870:
          dataset = this.places1870;
          break;
        case 1880:
          dataset = this.places1880;
          break;
        default:
          dataset = {};
      }

      return Object.entries(dataset || {}).map(([name, p]) => ({
        name,
        coords: p.coords,
        person: p.person,
        mother: p.mother,
        father: p.father
      }));
    }
  }
};
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
  flex-direction: column;
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
.radio-button-container{
  display: flex;  
  flex-direction: row;  
  align-items: center;  
  gap: 1rem;
  margin: 1rem;
}

.radio-button-container-individual {
  display: flex;       
  flex-direction: row; 
  align-items: center;   
  gap: 0.5rem;  
}
</style>