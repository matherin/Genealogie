<template>
  <div class="vw-main-container">
    <div class="vw-main-container-left">
      <Menu class="vw-main-container-left-menu vw-menu-custom" :model="verwaltungsItems">
        <template #submenulabel="{ item }">
          <span class="text-primary-font-bold">{{ item.label }}</span>
        </template>
      </Menu>
    </div>
    <div class="vw-main-container-right">
      <Toast ref="toast" />
      <router-view />
    </div>
  </div>
</template>

<script>
import Menu from "primevue/menu";
import { useRoute } from "vue-router";
import Toast from "@/components/custom/toast/Toast.vue";
import { getSessionCookies } from "@/components/custom/cookies/CookieService";

export default {
  components: {
    Menu,
    Toast,
  },
  beforeRouteEnter(to, form, next) {
    const session = getSessionCookies();
    let permission = "user";
    if (session?.aud) permission = session.aud;
    else next("/");

    if (to.path.split("/")[1] === "nutzerverwaltung" && permission !== "admin")
      next("/");
    else if (
      to.path.split("/")[1] === "kundenverwaltung" &&
      !["admin", "user"].includes(permission)
    )
      next("/");
    else if (
      to.path.split("/")[1] === "warenverwaltung" &&
      !["admin", "user"].includes(permission)
    ) {
      next("/");
    } else if (
      to.path.split("/")[1] === "vertragsverwaltung" &&
      !["admin", "user"].includes(permission)
    )
      next("/");
    else next();
  },
  data() {
    return {
      route: useRoute(),
      verwaltungsItems: [
        {
          label: "Ansichten",
          items: [
            {
              label: "Nutzerübersicht",
              icon: "pi pi-users",
              command: () => this.$router.push("/nutzerverwaltung/nutzertabelle"),
            },
          ],
        },
      ],
    };
  },
};
</script>

<style>
.vw-main-container {
  display: flex;
  width: 100vw;
  min-width: 1000px;
  height: calc(100vh - 56px);
  min-height: 700px;
}

.vw-main-container-left {
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

.vw-main-container-left-menu {
  margin-bottom: 50px;
}

.vw-main-container-right {
  display: flex;
  flex: 1;
  overflow: auto;
}

.vw-menu-custom-button {
  size: small;
}

.vw-menu-custom {
  border: none !important;
  box-shadow: none !important;
  background: none !important;
  background-color: transparent !important;
}

.text-primary-font-bold {
  color: var(--color-font-primary) !important;
  font-weight: 700;
  letter-spacing: -0.5px;
}
</style>
