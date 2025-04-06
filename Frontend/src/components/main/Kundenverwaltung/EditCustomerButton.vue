<template>
  <div>
    <Toast ref="toast" />
    <Button icon="pi pi-pen-to-square" class="p-button-edit" @click="
      visible = true;
    this.editCustomer = JSON.parse(JSON.stringify(this.editableCustomer));
    console.log(this.editCustomer);
    " />
    <Dialog v-model:visible="visible" modal header="Kunden bearbeiten" >
      <div class="item-container">

        <div class="items-alone">
          <label class="text">Privatperson</label>
          <ToggleSwitch v-model="editCustomer.private" />
        </div>

        <div class="items-alone" v-if="!editCustomer.private">
          <label class="text">Firma</label>
          <InputText id="account_number" v-model="editCustomer.company" class="flex-auto" autocomplete="off"
            placeholder="Musterfirma GmbH" />
        </div>

        <div class="item-group">
          <label class="group-text">Kontaktpersonen</label>
          <div class="items">
            <label class="text">Kontakt 1</label>
            <InputText id="contact1" v-model="editCustomer.contacts[0]" class="flex-auto" autocomplete="off"
              placeholder="Max Mustermann" />
          </div>
          <div class="items">
            <label class="text">Kontakt 2*</label>
            <InputText id="contact2" v-model="editCustomer.contacts[1]" class="flex-auto" autocomplete="off"
              placeholder="Max Mustermann" />
          </div>
          <div class="items">
            <label class="text">Kontakt 3*</label>
            <InputText id="contact3" v-model="editCustomer.contacts[2]" class="flex-auto" autocomplete="off"
              placeholder="Max Mustermann" />
          </div>
        </div>

        <div class="item-group">
          <label class="group-text">E-Mail-Adressen</label>
          <div class="items">
            <label class="text">E-Mail 1</label>
            <InputText id="email1" v-model="editCustomer.emails[0]" class="flex-auto" autocomplete="off"
              placeholder="Max.Mustermann@gmail.com" />
          </div>
          <div class="items">
            <label class="text">E-Mail 2*</label>
            <InputText id="email2" v-model="editCustomer.emails[1]" class="flex-auto" autocomplete="off"
              placeholder="Max.Mustermann@gmail.com" />
          </div>
          <div class="items">
            <label class="text">E-Mail 3*</label>
            <InputText id="email3" v-model="editCustomer.emails[2]" class="flex-auto" autocomplete="off"
              placeholder="Max.Mustermann@gmail.com" />
          </div>
        </div>

        <div class="item-group">
          <label class="group-text">Telefonnummern</label>
          <div class="items">
            <label class="text">Telef-Nr. 1</label>
            <InputText id="phone1" v-model="editCustomer.phone_numbers[0]" class="flex-auto" autocomplete="off"
              placeholder="+4912345678910" />
          </div>
          <div class="items">
            <label class="text">Telef-Nr. 2*</label>
            <InputText id="phone2" v-model="editCustomer.phone_numbers[1]" class="flex-auto" autocomplete="off"
              placeholder="+4912345678910" />
          </div>
          <div class="items">
            <label class="text">Telef-Nr. 3*</label>
            <InputText id="phone3" v-model="editCustomer.phone_numbers[2]" class="flex-auto" autocomplete="off"
              placeholder="+4912345678910" />
          </div>
        </div>

        <div class="item-group">
          <label class="group-text">Lieferadresse</label>
          <div class="items">
            <label class="text">Land</label>
            <InputText id="country" v-model="editCustomer.delivery_address.country" class="flex-auto" autocomplete="off"
              placeholder="Musterland" />
          </div>
          <div class="items">
            <label class="text">Stadt</label>
            <InputText id="city" v-model="editCustomer.delivery_address.city" class="flex-auto" autocomplete="off"
              placeholder="Musterhausen" />
          </div>
          <div class="items">
            <label class="text">Postleitzahl</label>
            <InputText id="postal_code" v-model="editCustomer.delivery_address.postal_code" class="flex-auto"
              autocomplete="off" placeholder="12345" />
          </div>
          <div class="items">
            <label class="text">Straße</label>
            <InputText id="street" v-model="editCustomer.delivery_address.street" class="flex-auto" autocomplete="off"
              placeholder="Musterstraße" />
          </div>
          <div class="items">
            <label class="text">Hausnummer</label>
            <InputText id="house_number" v-model="editCustomer.delivery_address.house_number" class="flex-auto"
              autocomplete="off" placeholder="1a" />
          </div>
        </div>

        <div class="item-group">
          <label class="group-text">Rechnungsadresse</label>
          <div class="items">
            <label class="text">Land</label>
            <InputText id="country" v-model="editCustomer.billing_address.country" class="flex-auto" autocomplete="off"
              placeholder="Musterland" />
          </div>
          <div class="items">
            <label class="text">Stadt</label>
            <InputText id="city" v-model="editCustomer.billing_address.city" class="flex-auto" autocomplete="off"
              placeholder="Musterhausen" />
          </div>
          <div class="items">
            <label class="text">Postleitzahl</label>
            <InputText id="postal_code" v-model="editCustomer.billing_address.postal_code" class="flex-auto"
              autocomplete="off" placeholder="12345" />
          </div>
          <div class="items">
            <label class="text">Straße</label>
            <InputText id="street" v-model="editCustomer.billing_address.street" class="flex-auto" autocomplete="off"
              placeholder="Musterstraße" />
          </div>
          <div class="items">
            <label class="text">Hausnummer</label>
            <InputText id="house_number" v-model="editCustomer.billing_address.house_number" class="flex-auto"
              autocomplete="off" placeholder="1a" />
          </div>
        </div>

        <div class="items-alone">
          <label class="text">IBAN</label>
          <InputText id="account_number" v-model="editCustomer.account_number" class="flex-auto" autocomplete="off"
            placeholder="DE01 2345 6789 1011 1213 14" />
        </div>

        <div class="items-alone">
          <label class="text">Steuernummer</label>
          <InputText id="account_number" v-model="editCustomer.tax_number" class="flex-auto" autocomplete="off"
            placeholder="012345678910" />
        </div>

        <div class="items-notes">
          <label class="text">Notizen*</label>
          <Editor id="notes" v-model="editCustomer.notes" editorStyle="height: 320px"
            placeholder="Notizen schreiben..." />
        </div>

      </div>
      <template #footer>
        <div class="dialog-footer">
          <div class="dialog-footer-left">
            <span class="footer-note">*Optionale Felder</span>
          </div>
          <div class="buttons">
            <Button type="button" label="Abbrechen" severity="secondary" @click="closeEditCustomerMode"
              autofocus></Button>
            <Button type="button" label="Speichern" @click="sendDataToBackend" autofocus></Button>
          </div>
        </div>
      </template>
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
import Editor from "primevue/editor";

var baseUrl = window.location.origin;

export default {
  name: "EditCustomerButton",
  emits: ["editCustomerData"],
  components: {
    Button,
    Dialog,
    InputText,
    Editor,
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
        !this.editCustomer.billing_address.city ||
        !this.editCustomer.billing_address.country ||
        !this.editCustomer.billing_address.house_number ||
        !this.editCustomer.billing_address.postal_code ||
        !this.editCustomer.billing_address.street ||
        this.editCustomer.contacts[0] === '' ||
        !this.editCustomer.contacts.length ||
        !this.editCustomer.delivery_address ||
        !this.editCustomer.delivery_address.city ||
        !this.editCustomer.delivery_address.country ||
        !this.editCustomer.delivery_address.house_number ||
        !this.editCustomer.delivery_address.postal_code ||
        !this.editCustomer.delivery_address.street ||
        this.editCustomer.emails[0] === '' ||
        !this.editCustomer.emails.length ||
        this.editCustomer.phone_numbers[0] === '' ||
        !this.editCustomer.phone_numbers.length ||
        !this.editCustomer.tax_number ||
        !this.editCustomer.private && !this.editCustomer.company
      ) {
        this.$refs.toast.toastAddError(
          "Bitte weisen Sie dem Kunden alle Pflichtfelder zu."
        );
        return;
      }
      let customer = {
        ...this.editCustomer
      };
      const customerID = customer.id;
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

<style scoped>
.column {
  display: flex;
  flex-direction: column;
}

.item-container {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.items-alone {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
  margin-left: 20px;
  margin-bottom: 4px;
  width: 80%;
}

.items {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 4px;
  width: 100%;
}

.items-notes {
  display: flex;
  align-items: start;
  flex-direction: column;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 8px;
  margin-top: 15px;
  gap: 8px;
}

.item-group {
  margin-top: 2rem;
  margin-bottom: 2rem;
  width: 80%;
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

.group-text {
  font-weight: 600;
  width: 24px;
  text-decoration: solid;
  margin-bottom: 8px;
}

.password-text {
  font-weight: 600;
}

.buttons {
  display: flex;
  justify-content: end;
  gap: 1rem;
  padding-top: 10px;
  position: sticky;
  bottom: 0;
  background: white;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.dialog-footer-left {
  display: flex;
  align-items: flex-end;
}

.footer-note {
  color: gray;
  font-weight: 400;
}

.flex-auto {
  display: flex;
  flex: auto;
  margin-left: 50px;
  max-width: 500px;
}

.footer-button {
  justify-content: end;
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

.p-dialog {
  min-width: 400px !important;
  min-height: 400px !important;
  max-width: 60rem !important;
  width: 60rem !important;
  max-height: 70rem !important;
  overflow: auto !important;
}
</style>