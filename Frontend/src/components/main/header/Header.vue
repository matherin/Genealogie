<template>
  <div class="header-container">
    <div class="header-container-view">
      <div class="header-container-right">
        <div class="header-container-profile">
          <router-link :class="{ routeractive: isActive('/map') }" class="header-container-profile-button"
            to="/map">
            <i class="pi pi-map"/></router-link>
        </div>
        <div class="header-container-bar">
          <router-link :class="{ routeractive: isActive('/censusData') }" class="header-container-bar-item"
            to="/censusData">
            Census Data</router-link>
        </div>
      </div>
      <div class="header-container-logo">
        <div class="header-container-logo-art"></div>
        <p class="header-container-logo-text" @click="onTitleClick">Pittsburgh/Allegheny Census Data</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import Menu from "primevue/menu";
import Button from "primevue/button";

export default {
  name: "AppHeader",
  components: {
    Menu,
    Button,
  },
  data() {
    return {
      route: useRoute(),
    };
  },
  methods: {
    profileToggle(event) {
      this.$refs.menu.toggle(event);
    },
    onTitleClick() {
      this.$router.push("/");
    },
    isActive(prefix) {
      return this.route.path.startsWith(prefix);
    },
  },
};
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
  width: 40%;
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
  color: #ffffffb0;
}

.header-container-profile-button:hover {
  background-color: #ffffff2c !important;
  border: none !important;
  color: #fff;
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