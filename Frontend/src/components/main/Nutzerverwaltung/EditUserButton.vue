<template>
    <div>
      <Toast ref="toast" />
      <Button
        icon="pi pi-pen-to-square"
        class="p-button-edit"
        @click="
          visible = true;
          getGruppen();
          this.editUser = { ...editableUser };
        "
      />
      <Dialog
        v-model:visible="visible"
        modal
        header="Nutzer bearbeiten"
        :style="{ width: '30rem' }"
      >
        <div class="item-container">
          <div class="items">
            <label for="username" class="text">Username</label>
            <InputText
              id="username"
              v-model="editUser.username"
              class="flex-auto"
              autocomplete="off"
            />
          </div>
          <div class="items">
            <label for="role" class="text">Rolle</label>
            <Select
              v-model="editUser.role"
              optionValue="role"
              :options="rollen"
              optionLabel="role"
              placeholder="Rolle auswählen"
            />
          </div>
          <div v-if="!passwordVisible" class="items">
            <Button
              type="button"
              class="reset-button"
              label="Passwort zurücksetzen"
              @click="resetPassword"
            ></Button>
          </div>
          <div v-if="passwordVisible" class="items">
            <label class="password-text">Neues Passwort:</label>
            <label>{{ this.newPassword }}</label>
          </div>
        </div>
        <div class="buttons">
          <Button
            type="button"
            label="Abbrechen"
            severity="secondary"
            @click="closeEditUserMode"
          ></Button>
          <Button
            type="button"
            label="Speichern"
            @click="sendDataToBackend"
          ></Button>
        </div>
      </Dialog>
    </div>
  </template>
  
  <script>
  import Button from "primevue/button";
  import Dialog from "primevue/dialog";
  import InputText from "primevue/inputtext";
  import Select from "primevue/select";
  import Toast from "@/components/custom/toast/Toast.vue";
  import { toRaw } from "vue";
  
  var baseUrl = window.location.origin;
  
  export default {
    name: "AddUserButton",
    emits: ["editUserData"],
    components: {
      Button,
      Dialog,
      InputText,
      Select,
      Toast,
    },
    props: {
      editableUser: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        visible: false,
        passwordVisible: false,
        hashedPassword: "",
        editUser: null,
        newPassword: "",
        rollen: [{ role: "user" }, { role: "admin" }],
      };
    },
    methods: {
        async sendDataToBackend() {
            if (
            !this.editUser.username ||
            !this.editUser.role
            ) {
            this.$refs.toast.toastAddError(
                "Bitte weisen Sie dem Account alle Felder zu."
            );
            }
            let user = {
            ...this.editUser
            };
            if (this.passwordVisible) {
            user.password = this.hashedPassword;
            }
            const userID = user.id;
            delete user.id;
            user = toRaw(user);
            try {
            const response = await fetch(`${baseUrl}/api/users/${userID}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(user),
                credentials: "include",
            });
            if (!response.ok) {
                throw new Error(`HTTP error. Status: ${response.status}`);
            }
            this.$refs.toast.toastAddSuccess(
                "Nutzer wurde erfolgreich aktualisiert"
            );
            this.$emit("editUserData");
            this.closeEditUserMode();
            } catch (error) {
            this.$refs.toast.toastAddError(
                "Nutzer konnte nicht aktualisiert werden"
            );
            console.error("Upload error:", error);
            }
        },

      closeEditUserMode() {
        this.visible = false;
        this.editUser = null;
      },
  
      async resetPassword() {
        this.hashedPassword = await this.generateHashedPassword(
          this.generatePassword(12)
        );
        this.passwordVisible = true;
      },
  
      generatePassword(length) {
        const chars =
          "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*?";
        let password = "";
        for (let i = 0; i < length; i++) {
          const randomIndex = Math.floor(Math.random() * chars.length);
          password += chars[randomIndex];
        }
        this.newPassword = password;
        return password;
      },
  
      async generateHashedPassword(newPassword) {
        const encoder = new TextEncoder();
        const data = encoder.encode(newPassword);
        const hashBuffer = await crypto.subtle.digest("SHA-512", data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
      },
    },
  };
  </script>
  
  <style>
  .column {
    display: flex;
    flex-direction: column;
  }
  
  .item-container {
    margin-bottom: 1, 5rem;
  }
  
  .items {
    display: flex;
    align-items: center;
    gap: 4rem;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 4px;
  }
  
  .text {
    font-weight: 600;
    width: 24px;
  }
  
  .password-text {
    font-weight: 600;
  }
  
  .buttons {
    display: flex;
    justify-content: end;
    gap: 1rem;
    margin-top: 10px;
  }
  
  .flex-auto {
    display: flex;
    flex: auto;
  }
  
  .footer-button {
    justify-content: end;
  }
  
  .p-button-edit {
    background-color: white;
    color: var(--p-dialog-color);
    height: 28px !important;
    width: 28px !important;
  }
  
  .reset-button {
    background-color: white;
    color: var(--p-dialog-color);
  }
  </style>
  