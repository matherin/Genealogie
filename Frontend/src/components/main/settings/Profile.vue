<template>
    <div class="user-info-container">
      <NewToast ref="toast" />
      <div class="user-content">
  
        <!-- Nutzerinformationen -->
        <div class="user-info-card">
          <div class="user-info-card-title">
            <h3>Nutzerinformationen</h3>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">ID:</span>
            <span class="user-info-value">{{ userData.account_id }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Vorname:</span>
            <span class="user-info-value">{{ userData.vorname }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Nachname:</span>
            <span class="user-info-value">{{ userData.nachname }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Rolle:</span>
            <span class="user-info-value">{{ userData.role }}</span>
          </div>
          <div class="user-info-row">
            <span class="user-info-label">Standort:</span>
            <span class="user-info-value">{{ userData.location }}</span>
          </div>
        </div>
  
        <!-- Gruppentabelle -->
        <div class="user-group-card">
          <div class="user-group-card-title">
            <h3>Gruppen</h3>
          </div>
          <div class="user-group-card-text">
            <span class="user-group-card-text-item" v-for="(group, index) in userData.groups" :key="index">
              {{ group }}
            </span>
          </div>
        </div>
      </div>
  
      <!-- QR-Code Bereich -->
      <div class="qr-container">
        <div class="download-button">
          <Button class="custom-dow-button" type="button" label="Herunterladen" icon="pi pi-download" @click="exportQR" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NewToast from "@/components/custom/toast/Toast.vue";
  import { getSessionCookies } from "@/components/custom/cookies/CookieService";
  import Button from "primevue/button";
  
  export default {
    name: "UserInfoView",
    components: { NewToast, Button },
    data() {
      return {
        userData: {
          account_id: "",
          vorname: "",
          nachname: "",
          role: "",
          location: "",
          groups: []
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
  
          const response = await fetch(`/api/accounts/${session.id}`);
          if (!response.ok) throw new Error("Fehler beim Abrufen der Nutzerdaten");
          const accountData = await response.json();
  
          let currentGroups = [];
          for(let group of accountData.groups){
            currentGroups.push(group.group_name);
          }
          let currentLocation = "N/A";
          if (accountData?.groups[0] && accountData.groups[0]?.location_name) {
            currentLocation = accountData.groups[0].location_name
          }
  
          this.userData = {
            account_id: session.id || "N/A",
            vorname: accountData.vorname || "N/A",
            nachname: accountData.nachname || "N/A",
            role: accountData.role || "N/A",
            location: currentLocation || "N/A",
            groups: currentGroups || "N/A"
          };
          this.qrCodeValue = `${this.userData.account_id}`;
        } catch (error) {
          console.error("Fehler beim Laden der Nutzerdaten:", error);
          if (this.$refs.toast) {
            this.$refs.toast.toastAddError("Fehler beim Laden der Nutzerdaten");
          }
        }
      },
      exportQR() {
        const canvas = document.querySelector("canvas");
        if (!canvas) return;
        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/png");
        link.download = `${this.userData.vorname}_${this.userData.nachname}_QR.png`;
        link.click();
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
  
  