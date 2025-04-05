<template>
  <div>
      <Toast ref="toast" />
      <Button icon="pi pi-pen-to-square" class="p-button-edit" @click="
          visible = true;
      this.editCustomer = { ...editableCustomer };
      " />
      <Dialog v-model:visible="visible" modal header="Kunden bearbeiten" :style="{ width: '30rem' }">
          <div class="item-container">
              <div class="items">
                <label>Privatperson</label>
                <ToggleSwitch v-model="editCustomer.private" />
              </div>
              <div class="items">
                  <label for="account_number" class="text">IBAN</label>
                  <InputText id="account_number" v-model="editCustomer.account_number" class="flex-auto" autocomplete="off" />
              </div>
          </div>
          <div class="buttons">
              <Button type="button" label="Abbrechen" severity="secondary" @click="closeEditUserMode"></Button>
              <Button type="button" label="Speichern" @click="sendDataToBackend"></Button>
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
import { ToggleSwitch } from "primevue";

var baseUrl = window.location.origin;

export default {
  name: "EditCustomerButton",
  emits: ["editCustomerData"],
  components: {
    Button,
    Dialog,
    InputText,
    ToggleSwitch,
    Select,
    Toast,
  },
  props: {
    editableCustomer: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      visible: false,
      editCustomer: null,
    };
  },
  methods: {
    async sendDataToBackend() {
      if (
        !this.editCustomer.account_number ||
        !this.editCustomer.billing_address ||
        !this.editCustomer.contact1 ||
        !this.editCustomer.delivery_address ||
        !this.editCustomer.email1 ||
        !this.editCustomer.phone1 ||
        !this.editCustomer.tax_number
      ) {
        this.$refs.toast.toastAddError(
          "Bitte weisen Sie dem Kunden alle Pflichtfelder zu."
        );
      }
      let customer = {
        ...this.editCustomer
      };
      const customerID = customer.kid;
      delete customer.kid;
      customer = toRaw(customer);
      try {
        const response = await fetch(`${baseUrl}/api/customers/${customerID}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(customer),
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error(`HTTP error. Status: ${response.status}`);
        }
        this.$refs.toast.toastAddSuccess(
          "Kunde wurde erfolgreich aktualisiert"
        );
        this.$emit("editCustomerData");
        this.closeEditCustomerMode();
      } catch (error) {
        this.$refs.toast.toastAddError(
          "Kunde konnte nicht aktualisiert werden"
        );
        console.error("Upload error:", error);
      }
    },

    closeEditCustomerMode() {
      this.visible = false;
      this.editCustomer = null;
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

.items-password {
  display: flex;
  align-items: center;
  gap: 2rem;
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

.copy-User {
  border-color: transparent !important;
  background-color: transparent !important;
  color: gray !important;
  width: 20px;
  height: 20px;
}

.copy-User:hover {
  color: black !important;
}
</style>