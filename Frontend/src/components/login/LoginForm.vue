<template>
    <div class="login-form-container">
      <NewToast ref="toast" />
      <p class="login-form-container-title">Login</p>
      <div
        class="login-form-container-username login-button-layout login-input-color"
      >
        <p
          class="login-form-container-username-text login-info-text-layout"
          :class="{ moved: usernameIsFocused }"
        >
          BENUTZERNAME
        </p>
        <input
          class="login-form-container-username-input login-input-layout"
          type="text"
          v-model="username"
          @focus="onUsernameFocus"
          @blur="onUsernameBlur"
          @keydown.enter="checkForLogin()"
        />
      </div>
      <div
        class="login-form-container-password login-button-layout login-input-color"
      >
        <p
          class="login-form-container-password-text login-info-text-layout"
          :class="{ moved: passwordIsFocused }"
        >
          PASSWORT
        </p>
        <input
          class="login-form-container-password-input login-input-layout"
          type="password"
          v-model="password"
          @focus="onPasswordFocus"
          @blur="onPasswordBlur"
          @keydown.enter="checkForLogin()"
        />
      </div>
      <p  class="login-form-container-pw-vergessen-text"
          @mouseover="forgotPasswordText = 'Bitte die Verwaltung kontaktieren!'"
          @mouseout="forgotPasswordText = 'Passwort vergessen?'">
          {{ forgotPasswordText }} </p>
      <Button
        class="login-button-layout-custom login-form-container-login"
        @keydown.enter="checkForLogin()"
        @click="checkForLogin()"
        >Login</Button
      >
    </div>
  </template>
  
  <script>
  import Button from "primevue/button";
  import NewToast from "../custom/toast/Toast.vue";
  import { getSessionCookies } from "../custom/cookies/CookieService";
  
  var baseUrl = window.location.origin;
  
  export default {
    components: {
      Button,
      NewToast,
    },
    data() {
      return {
        username: "",
        password: "",
        usernameIsFocused: false,
        passwordIsFocused: false,
        forgotPasswordText: "Passwort vergessen?",
      };
    },
    methods: {
      async checkForLogin() {
        const hashedPassword = await this.encodePassword(this.password);
        const loginUser = { name: this.username, password: hashedPassword };
        /*try {
          const response = await fetch(`${baseUrl}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(loginUser),
            credentials: "include",
          });
          if (!response.ok) {
            throw new Error(`HTTP error. Status: ${response.status}`);
          }
          this.$refs.toast.toastAddSuccess("Erfolgreich eingeloggt");
  
          this.checkForRoute();
        } catch (error) {
          console.error("Upload error:", error);
          this.$refs.toast.toastAddError("Einloggen nicht erfolgreich");
        }*/
        if(loginUser.name === "dev" && this.password === "1234"){
          this.$router.push("einstellungen/profil");
        }
      },
  
      checkForRoute() {
        let session = getSessionCookies()
  
        if (!session || !session?.aud || session.aud === 'user') this.$router.push("/einstellungen/profil");
        else if (session.aud === 'group') this.$router.push("/gruppenleitung/gruppen");
        else if (session.aud === 'location') this.$router.push("/standortleitung/gruppen");
        else if (session.aud === 'admin') this.$router.push("/verwaltung/nutzer");
        else this.$router.push("einstellungen/profil");
  
      },
  
      async encodePassword(newPassword) {
        const encoder = new TextEncoder();
        const data = encoder.encode(newPassword);
        const hashBuffer = await crypto.subtle.digest("SHA-512", data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
      },
  
      onUsernameFocus() {
        this.usernameIsFocused = true;
      },
      onUsernameBlur() {
        if (this.username.length == 0) {
          this.usernameIsFocused = false;
        }
      },
      onPasswordFocus() {
        this.passwordIsFocused = true;
      },
      onPasswordBlur() {
        if (this.password.length == 0) {
          this.passwordIsFocused = false;
        }
      },
    },
  };
  </script>
  
  <style>
  .login-form-container {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20vh;
  }
  
  .login-form-container-username-text {
    transition: transform 0.15s ease;
  }
  
  .login-form-container-username-text.moved {
    transform: translate(-10px, -25px);
  }
  
  .login-form-container-username-input {
    font-size: var(--font-size-regular);
  }
  
  .login-form-container-username-input:focus {
    border-color: #ffffffd0;
  }
  
  .login-form-container-password-input {
    font-size: var(--font-size-regular);
  }
  
  .login-form-container-password-input:focus {
    border-color: #ffffffd0;
  }
  
  .login-form-container-password-text {
    transition: transform 0.15s ease;
  }
  
  .login-form-container-password-text.moved {
    transform: translate(-10px, -25px);
  }
  
  .login-form-container-title {
    color: #fff;
    margin-bottom: 40px;
  
    font-size: var(--font-size-large);
    font-weight: 600;
  }
  
  .login-form-container-login {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    background-color: var(--color-secondary);
    font-weight: 600;
  
    margin-top: 50px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .login-form-container-login:hover {
    background-color: #f5984c;
  }
  
  .login-form-container-pw-vergessen-text {
    position: absolute;
    left: 0;
    margin-top: 250px;
    color: var(--color-font-basic-a8);
    font-weight: 600;
  }
  
  .login-button-layout {
    width: 390px;
    height: 55px;
    margin-bottom: 20px;
  
    display: flex;
    position: relative;
    border-radius: 4px !important;
    font-weight: 600 !important;
  }
  
  .login-button-layout-custom {
    width: 390px;
    height: 55px;
    margin-bottom: 20px;
  
    display: flex;
    position: relative;
    border-radius: 4px !important;
    font-weight: 600 !important;
    background: var(--color-secondary) !important;
    border: none !important;
  }
  
  .login-button-layout-custom:hover {
    background-color: #f5984c !important;
  }
  
  .login-button-layout-custom:active {
    background-color: #fcae6f !important;
  }
  
  .login-input-color {
    background-color: #3b5a71b0;
  }
  
  .login-input-layout {
    display: flex;
    background: none;
    border: none;
    flex: 1;
    color: #e2e7e9;
    vertical-align: bottom;
    text-align: left;
    padding-top: 15px;
    padding-left: 5px;
    font-weight: 500;
  
    outline: none;
    border: solid 2px #ffffff00;
    border-radius: 5px;
    transition: border-color 0.2s ease;
  }
  
  .login-info-text-layout {
    position: absolute;
    color: #cce0e975;
    top: 50%;
    left: 17px;
    transform: translate(0, -50%);
    font-weight: 800;
    font-size: 0.8rem;
    pointer-events: none;
  }
  </style>
  