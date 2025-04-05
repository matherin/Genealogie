<template>
    <div>
      <Toast ref="toast" />
      <Button
        @click="visible = true"
        icon="pi pi-trash"
        severity="danger"
        outlined
        class="p-button-delete"
      />
      <Dialog
        v-model:visible="visible"
        modal
        header="Nutzer löschen"
        :style="{ width: '25rem' }"
      >
        <span class="text information"
          >Möchten Sie den Nutzer wirklich löschen?</span
        >
        <div class="buttons">
          <Button
            type="button"
            label="Abbrechen"
            severity="secondary"
            @click="closeDeleteUserMode"
          />
          <Button type="button" label="Löschen" @click="onDeleteUser" />
        </div>
      </Dialog>
    </div>
  </template>
  
  <script>
  import Dialog from "primevue/dialog";
  import Button from "primevue/button";
  import Toast from "@/components/custom/toast/Toast.vue";
  
  var baseUrl = window.location.origin;
  
  export default {
    name: "DeleteUserButton",
    emits: ["deleteUserData"],
    components: {
      Button,
      Dialog,
      Toast,
    },
    data() {
      return {
        visible: false,
      };
    },
    props: {
      deleteUser: {
        type: Number,
        required: true,
      },
    },
    methods: {
      async onDeleteUser() {
        try {
          const response = await fetch(
            `${baseUrl}/api/users/${this.deleteUser}`,
            { method: "DELETE", credentials: "include" }
          );
          if (!response.ok) {
            throw new Error(`Fehler beim Löschen. Status: ${response.status}`);
          }
          this.$refs.toast.toastAddSuccess("Nutzer wurde erfolgreich entfernt");
          this.$emit("deleteUserData");
          this.closeDeleteUserMode();
        } catch (error) {
          console.error("Fehler beim Löschen des Benutzers:", error);
          this.$refs.toast.toastAddError("Nutzer konnte nicht entfernt werden");
        }
      },
  
      closeDeleteUserMode() {
        this.visible = false;
      },
    },
  };
  </script>
  
  <style>
  .p-button-delete {
    height: 28px !important;
    width: 28px !important;
  }
  
  .text {
    font-weight: 600;
    width: 24px;
  }
  
  .information {
    margin-bottom: 1rem;
  }
  .buttons {
    display: flex;
    justify-content: end;
    gap: 1rem;
    margin-top: 10px;
  }
  </style>
  