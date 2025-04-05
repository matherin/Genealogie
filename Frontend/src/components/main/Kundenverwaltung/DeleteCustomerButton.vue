<template>
  <div>
    <Toast ref="toast" />
    <Button @click="visible = true" icon="pi pi-trash" severity="danger" outlined class="p-button-delete" />
    <Dialog v-model:visible="visible" modal header="Kunden löschen" :style="{ width: '25rem' }">
      <span class="text information">Möchten Sie den Kunden wirklich löschen?</span>
      <div class="buttons">
        <Button type="button" label="Abbrechen" severity="secondary" @click="closeDeleteCustomerMode" />
        <Button type="button" label="Löschen" @click="onDeleteCustomer" />
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
  name: "DeleteCustomerButton",
  emits: ["deleteCustomerData"],
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
    deleteCustomer: {
      type: Number,
      required: true,
    },
  },
  methods: {
    async onDeleteCustomer() {
      try {
        const response = await fetch(
          `${baseUrl}/api/customers/${this.deleteCustomer}`,
          { method: "DELETE", credentials: "include" }
        );
        if (!response.ok) {
          throw new Error(`Fehler beim Löschen. Status: ${response.status}`);
        }
        this.$refs.toast.toastAddSuccess("Kunde wurde erfolgreich entfernt");
        this.$emit("deleteCustomerData");
        this.closeDeleteCustomerMode();
      } catch (error) {
        console.error("Fehler beim Löschen des Kundens:", error);
        this.$refs.toast.toastAddError("Kunde konnte nicht gelöscht werden");
      }
    },

    closeDeleteCustomerMode() {
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
  margin-top: 10px; }
  
</style>
  
