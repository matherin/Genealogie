<template>
  <div>
    <Toast ref="toast" />
    <Button icon="pi pi-eye" outlined class="p-button-edit" @click="onViewClick" />
    <Dialog v-model:visible="visible" modal>
      <template #header>
        <div class="dialog-header">
          <span v-if="readOnlyMode" class="header-text">Kundenübersicht</span>
          <span v-else class="header-text">Kunden bearbeiten</span>
          <Button :icon="!readOnlyMode ? 'pi pi-eye' : 'pi pi-pen-to-square'" class="button" severity="primary" outlined
            @click="readOnlyMode = !readOnlyMode; checkForDifferentAddress(); closeEditCustomerMode()" />
        </div>
      </template>
      <div class="item-container">

        <div class="column-left">
          <div class="item-group">
            <div class="items-alone">
              <label class="text">Privatperson</label>
              <ToggleSwitch v-model="editCustomer.private" :disabled="readOnlyMode" />
            </div>

            <div class="items-alone" v-if="!editCustomer.private">
              <label class="text">Firma<span v-if="!readOnlyMode">*</span></label>
              <InputText id="account_number" v-model="editCustomer.company"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterfirma GmbH' : ''" :readonly="readOnlyMode" />
            </div>


            <div class="items-alone">
              <label class="text">IBAN<span v-if="!readOnlyMode">*</span></label>
              <InputText id="account_number" v-model="editCustomer.account_number"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'DE01 2345 6789 1011 1213 14' : ''" :readonly="readOnlyMode" />
            </div>

            <div class="items-alone">
              <label class="text">Steuernummer<span v-if="!readOnlyMode">*</span></label>
              <InputText id="account_number" v-model="editCustomer.tax_number"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '012345678910' : ''" :readonly="readOnlyMode" />
            </div>
          </div>

          <div class="item-group">
            <label class="group-text">Kontaktpersonen</label>
            <div class="items">
              <label class="text">Kontakt 1<span v-if="!readOnlyMode">*</span></label>
              <InputText id="contact1" v-model="editCustomer.contacts[0]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max Mustermann' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Kontakt 2</label>
              <InputText id="contact2" v-model="editCustomer.contacts[1]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max Mustermann' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Kontakt 3</label>
              <InputText id="contact3" v-model="editCustomer.contacts[2]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max Mustermann' : ''" :readonly="readOnlyMode" />
            </div>
          </div>

          <div class="item-group">
            <label class="group-text">E-Mail-Adressen</label>
            <div class="items">
              <label class="text">E-Mail 1<span v-if="!readOnlyMode">*</span></label>
              <InputText id="email1" v-model="editCustomer.emails[0]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max.Mustermann@gmail.com' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">E-Mail 2</label>
              <InputText id="email2" v-model="editCustomer.emails[1]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max.Mustermann@gmail.com' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">E-Mail 3</label>
              <InputText id="email3" v-model="editCustomer.emails[2]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Max.Mustermann@gmail.com' : ''" :readonly="readOnlyMode" />
            </div>
          </div>

          <div class="item-group">
            <label class="group-text">Telefonnummern</label>
            <div class="items">
              <label class="text">Telef-Nr. 1<span v-if="!readOnlyMode">*</span></label>
              <InputText id="phone1" v-model="editCustomer.phone_numbers[0]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '+4912345678910' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Telef-Nr. 2</label>
              <InputText id="phone2" v-model="editCustomer.phone_numbers[1]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '+4912345678910' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Telef-Nr. 3</label>
              <InputText id="phone3" v-model="editCustomer.phone_numbers[2]"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '+4912345678910' : ''" :readonly="readOnlyMode" />
            </div>
          </div>
        </div>

        <div class="column-right">
          <div class="item-group">
            <label class="group-text">Lieferadresse</label>
            <div class="items">
              <label class="text">Land<span v-if="!readOnlyMode">*</span></label>
              <InputText id="country" v-model="editCustomer.delivery_address.country"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterland' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Stadt<span v-if="!readOnlyMode">*</span></label>
              <InputText id="city" v-model="editCustomer.delivery_address.city"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterhausen' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Postleitzahl<span v-if="!readOnlyMode">*</span></label>
              <InputText id="postal_code" v-model="editCustomer.delivery_address.postal_code"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '12345' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Straße<span v-if="!readOnlyMode">*</span></label>
              <InputText id="street" v-model="editCustomer.delivery_address.street"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterstraße' : ''" :readonly="readOnlyMode" />
            </div>
            <div class="items">
              <label class="text">Hausnummer<span v-if="!readOnlyMode">*</span></label>
              <InputText id="house_number" v-model="editCustomer.delivery_address.house_number"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '1a' : ''" :readonly="readOnlyMode" />
            </div>
          </div>
          <div class="item-group">
            <div v-if="!readOnlyMode" class="items-alone">
              <label class="text">Abweichende Rechnungsadresse</label>
              <ToggleSwitch v-model="showRechnungsadresse" />
            </div>
            <label v-if="showRechnungsadresse" class="group-text">Rechnungsadresse</label>
            <div v-if="showRechnungsadresse" class="items">
              <label class="text">Land<span v-if="!readOnlyMode">*</span></label>
              <InputText id="country" v-model="editCustomer.billing_address.country"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterland' : ''" :readonly="readOnlyMode" />
            </div>
            <div v-if="showRechnungsadresse" class="items">
              <label class="text">Stadt<span v-if="!readOnlyMode">*</span></label>
              <InputText id="city" v-model="editCustomer.billing_address.city"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterhausen' : ''" :readonly="readOnlyMode" />
            </div>
            <div v-if="showRechnungsadresse" class="items">
              <label class="text">Postleitzahl<span v-if="!readOnlyMode">*</span></label>
              <InputText id="postal_code" v-model="editCustomer.billing_address.postal_code"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '12345' : ''" :readonly="readOnlyMode" />
            </div>
            <div v-if="showRechnungsadresse" class="items">
              <label class="text">Straße<span v-if="!readOnlyMode">*</span></label>
              <InputText id="street" v-model="editCustomer.billing_address.street"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? 'Musterstraße' : ''" :readonly="readOnlyMode" />
            </div>
            <div v-if="showRechnungsadresse" class="items">
              <label class="text">Hausnummer<span v-if="!readOnlyMode">*</span></label>
              <InputText id="house_number" v-model="editCustomer.billing_address.house_number"
                :class="['flex-auto', { 'read-only-input': readOnlyMode }]" autocomplete="off"
                :placeholder="!readOnlyMode ? '1a' : ''" :readonly="readOnlyMode" />
            </div>
          </div>

          <div class="items-notes">
            <label class="text">Notizen</label>
            <Editor id="notes" v-model="editCustomer.notes" editorStyle="height: 300px"
              :placeholder="!readOnlyMode ? 'Notiz schreiben...' : ''" :readonly="readOnlyMode" />
          </div>
        </div>
      </div>
      <template v-if="!readOnlyMode" #footer>
        <div class="dialog-footer">
          <div class="dialog-footer-left">
            <span class="footer-note">*Pflichtfelder</span>
          </div>
          <div class="buttons">
            <Button type="button" label="Abbrechen" severity="secondary"
              @click="closeEditCustomerMode(); readOnlyMode = true" autofocus></Button>
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
      readOnlyMode: false,
      showRechnungsadresse: true,
    };
  },
  methods: {
    async sendDataToBackend() {
      if (!this.showRechnungsadresse) this.editCustomer.billing_address = this.editCustomer.delivery_address;
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
        this.readOnlyMode = true;
      } catch (error) {
        this.$refs.toast.toastAddError(
          "Kunde konnte nicht aktualisiert werden"
        );
        console.error("Upload error:", error);
      }
    },

    checkForDifferentAddress() {
      if(this.readOnlyMode) return;
      const delivery = this.editCustomer.delivery_address;
      const billing = this.editCustomer.billing_address;

      const isSameAdress =
        delivery.country === billing.country &&
        delivery.city === billing.city &&
        delivery.postal_code === billing.postal_code &&
        delivery.street === billing.street &&
        delivery.house_number === billing.house_number;

      this.showRechnungsadresse = !isSameAdress;
      console.log("deli", this.editCustomer.delivery_address);
      console.log("billy", this.editCustomer.billing_address);
    },

    onViewClick() {
      this.visible = true;
      this.readOnlyMode = true;
      this.editCustomer = JSON.parse(JSON.stringify(this.editableCustomer));
      this.checkForDifferentAddress();
    },

    closeEditCustomerMode() {
      this.showRechnungsadresse = true;
      this.editCustomer = JSON.parse(JSON.stringify(this.editableCustomer));
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
  display: flex;
  flex-direction: row;
  gap: 2rem;
  width: 100%;
  padding: 1rem 2rem;
  box-sizing: border-box;
}

.column-left,
.column-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.items-alone {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-left: 10px;
  margin-bottom: 4px;
  width: 80%;
}

.items {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
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
  position: relative;
  width: 100%;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.group-text::after {
  content: "";
  flex-grow: 1;
  height: 1px;
  background-color: #ccc;
  margin-left: 1rem;
}

.header-text {
  font-weight: bold;
  font-size: 1.5rem;
  text-decoration: underline;
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

.read-only-input {
  border: none !important;
  background-color: transparent !important;
  pointer-events: none;
  box-shadow: none !important;
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
  max-width: 90rem !important;
  width: 90vw !important;
  max-height: 70rem !important;
  overflow: hidden !important;
}

.p-dialog .p-dialog-content {
  max-height: 60vh;
  overflow-y: auto;
  border-radius: 1rem;
  padding-right: 1rem;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  gap: 1rem;
  width: 100%;
}
</style>