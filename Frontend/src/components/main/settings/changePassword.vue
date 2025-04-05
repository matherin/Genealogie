<template>
    <div class="container-pw">
      <NewToast ref="toast" />
      <div class="password-change-form-container">
        <p class="password-change-form-container-title">Passwort ändern</p>
  
        <!-- Neues Passwort -->
        <div
          class="password-change-form-container-new change-password-button-layout change-password-input-color"
        >
          <p
            class="password-change-form-container-new-text change-password-info-text-layout"
            :class="{ moved: newPasswordIsFocused }"
          >
            NEUES PASSWORT
          </p>
          <input
            class="password-change-form-container-new-input change-password-input-layout"
            type="password"
            v-model="newPassword"
            @focus="onNewPasswordFocus"
            @blur="onNewPasswordBlur"
            @keydown.enter="submitPasswordChange"
          />
        </div>
  
        <!-- Neues Passwort bestätigen -->
        <div
          class="password-change-form-container-confirm change-password-button-layout change-password-input-color"
        >
          <p
            class="password-change-form-container-confirm-text change-password-info-text-layout"
            :class="{ moved: confirmNewPasswordIsFocused }"
          >
            PASSWORT BESTÄTIGEN
          </p>
          <input
            class="password-change-form-container-confirm-input change-password-input-layout"
            type="password"
            v-model="confirmNewPassword"
            @focus="onConfirmNewPasswordFocus"
            @blur="onConfirmNewPasswordBlur"
            @keydown.enter="submitPasswordChange"
          />
        </div>
  
        <Button
          class="change-password-button-layout-custom password-change-form-container-submit"
          @click="submitPasswordChange"
          >Bestätigen</Button
        >
      </div>
    </div>
  </template>
  
  <script>
  import Button from "primevue/button";
  import { getSessionCookies } from "@/components/custom/cookies/CookieService.js";
  import NewToast from "@/components/custom/toast/Toast.vue";
  
  var baseUrl = window.location.origin;
  
  export default {
    components: {
      Button,
      NewToast,
    },
  
    data() {
      return {
        newPassword: "",
        confirmNewPassword: "",
        newPasswordIsFocused: false,
        confirmNewPasswordIsFocused: false,
      };
    },
  
    methods: {
      async submitPasswordChange() {
        const data = getSessionCookies();
        const userID = data.id;
  
        if (!this.newPassword || !this.confirmNewPassword) {
          this.$refs.toast.toastAddError("Bitte alle Felder ausfüllen!");
          return;
        }
  
        if (this.newPassword !== this.confirmNewPassword) {
          this.$refs.toast.toastAddError(
            "Die neuen Passwörter stimmen nicht überein!"
          );
          return;
        }
  
        try {
          const hashedPassword = await this.encodePassword(this.newPassword);
  
          const payload = {
            password: hashedPassword,
          };
  
          const response = await fetch(`${baseUrl}/api/users/${userID}/password`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(
              `Fehler: ${
                errorData.message || "Passwort konnte nicht geändert werden."
              }`
            );
          }
  
          this.$refs.toast.toastAddSuccess("Passwort erfolgreich geändert!");
  
          this.resetForm();
        } catch (error) {
          console.error("Fehler beim Ändern des Passworts:", error);
          this.$refs.toast.toastAddError(
            error.message || "Es gab ein Problem beim Verbinden mit dem Server."
          );
        }
      },
  
      async encodePassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest("SHA-512", data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
      },
  
      resetForm() {
        this.newPassword = "";
        this.confirmNewPassword = "";
        this.newPasswordIsFocused = false;
        this.confirmNewPasswordIsFocused = false;
      },
  
      onNewPasswordFocus() {
        this.newPasswordIsFocused = true;
      },
      onNewPasswordBlur() {
        if (this.newPassword.length === 0) {
          this.newPasswordIsFocused = false;
        }
      },
      onConfirmNewPasswordFocus() {
        this.confirmNewPasswordIsFocused = true;
      },
      onConfirmNewPasswordBlur() {
        if (this.confirmNewPassword.length === 0) {
          this.confirmNewPasswordIsFocused = false;
        }
      },
    },
  };
  </script>
  
  <style>
  .password-change-form-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .password-change-form-container-title {
    margin-top: 5%;
    margin-bottom: 40px;
    font-size: var(--font-size-big);
    letter-spacing: -0.5px;
    font-weight: 600;
  }
  
  .password-change-form-container-new-text,
  .password-change-form-container-confirm-text {
    transition: transform 0.15s ease;
  }
  
  .password-change-form-container-new-text.moved,
  .password-change-form-container-confirm-text.moved {
    transform: translate(-10px, -25px);
  }
  
  .password-change-form-container-submit {
    background: var(--color-secondary);
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    padding-bottom: 0%;
  }
  
  .password-change-form-container-submit:hover {
    background-color: #f5984c;
  }
  
  .change-password-button-layout {
    width: 390px;
    height: 55px;
    margin-bottom: 20px;
  
    display: flex;
    position: relative;
    border-radius: 4px !important;
    font-weight: 600 !important;
  }
  
  .change-password-input-color {
    background-color: #ebf0f3;
  }
  
  .change-password-info-text-layout {
    position: absolute;
    color: var(--color-font-primary-a8);
    top: 50%;
    left: 17px;
    transform: translate(0, -50%);
    font-weight: 800;
    font-size: 0.8rem;
    pointer-events: none;
  }
  
  .change-password-input-layout {
    display: flex;
    background: none;
    border: none;
    flex: 1;
    color: var(--color-font-primary);
    vertical-align: bottom;
    text-align: left;
    padding-top: 15px;
    padding-left: 5px;
    font-weight: 500;
  
    outline: none;
    border-radius: 5px;
    transition: border-color 0.2s ease;
  }
  
  .change-password-input-layout {
    border: solid 2px #00000000;
  }
  
  .change-password-button-layout-custom {
    width: 390px;
    height: 55px;
    margin-bottom: 20px;
  
    display: flex;
    position: relative;
    border-radius: 4px !important;
    font-weight: 600 !important;
    background: #fc8f00 !important;
    border: none !important;
  }
  
  .change-password-button-layout-custom:hover {
    background-color: #ffa43c !important;
  }
  
  .change-password-button-layout-custom:active {
    background-color: #fcae6f !important;
  }
  
  .container-pw {
    display: flex;
    flex: 1;
  }
  
  .password-change-form-container-new-input:focus {
    border-color: var(--color-font-primary-a8);
  }
  
  .password-change-form-container-confirm-input:focus {
    border-color: var(--color-font-primary-a8);
  }
  </style>
  