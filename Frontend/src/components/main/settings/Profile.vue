<template>
    <div class="user-info-container">
      <Toast ref="toast" />
      <div class="user-content">
  
        <!-- Nutzerinformationen -->
        <div class="user-info-card">
          <div class="user-info-card-title">
            <h3>Nutzerinformationen</h3>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">ID:</span>
            <span class="user-info-value">{{ userData.id }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Nutzername:</span>
            <span class="user-info-value">{{ userData.username }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Rolle:</span>
            <span class="user-info-value">{{ userData.role }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Toast from "@/components/custom/toast/Toast.vue";
  import { getSessionCookies } from "@/components/custom/cookies/CookieService";
  import Button from "primevue/button";
  
  export default {
    name: "UserInfoView",
    components: { Toast, Button },
    data() {
      return {
        userData: {
          id: "",
          username: "",
          role: ""
        },
      };
    },
    mounted() {
      this.fetchUserData();
    },
        methods: {
          async fetchUserData() {
        try {
          const session = getSessionCookies();
          if (!session) throw new Error("Session nicht gefunden");
  
          const response = await fetch(`/api/users/${session.id}`);
          if (!response.ok) throw new Error("Fehler beim Abrufen der Nutzerdaten");
          const accountData = await response.json();
  
          this.userData = {
            id: session.id || "N/A",
            username: accountData.username || "N/A",
            role: accountData.role || "N/A",
          };
        } catch (error) {
          console.error("Fehler beim Laden der Nutzerdaten:", error);
          if (this.$refs.toast) {
            this.$refs.toast.toastAddError("Fehler beim Laden der Nutzerdaten");
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  
  .user-info-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
    gap: 20px;
    padding: 20px;
    margin-top: 50px;
    margin-left: 7%;
  }
  
  .user-content {
    display: flex;
    flex-direction: row;
    gap: 50px;
    align-items: flex-start;
  }
  
  .user-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
    gap: 20px;
  }
  
  .user-group-card{
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .user-info-card, .user-group-card, .user-qr-card {
    background: #fff;
    padding: 20px;
    border-radius: 7px;
    width: 300px;
  }
  
  .user-info-card{
    width: 400px;
  }
  
  .user-info-card-title{
    text-align: center;
    font-size: 20px;
    margin-bottom: 40px;
  }
  
  .user-group-card-title{
    font-size: 20px;
    text-align: center;
    margin-bottom: 40px;
  }
  
  .user-qr-card-title {
    font-size: 20px;
    margin-bottom: 40px !important;
  }
  
  .user-info-label{
    font-size: var(--font-size-regular);
    min-width: 150px;
    text-align: left;
  }
  
  .user-info-value{
    font-size: var(--font-size-regular);
    flex-grow: 1;
    text-align: left;
  }
  
  .user-group-card-text{
    display: flex;
    flex-direction: column;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  
  .qr-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-left: 50px;
    justify-content: center;
    align-items: center;
  }
  
  .user-qr-card {
    background: #fff;
    padding: 20px;
    border-radius: 7px;
    text-align: center;
    width: 350px;
    height: 350px;
  }
  
  .user-qr-card-title {
    margin-bottom: 15px;
  }
  
  .download-button {
    margin-top: 80px;
    font-size: var(--font-size-regular) !important;
    text-align: center;
  }
  
  .custom-dow-button {
    font-size: var(--font-size-regular) !important;
  }
  
  .user-group-card-text-item {
    margin-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: var(--font-size-regular);
  }
  
  </style>
  
  