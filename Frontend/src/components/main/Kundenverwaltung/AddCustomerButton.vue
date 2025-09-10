<template>
    <div>
        <Toast ref="toast" />
        <Button class="custom-add-customer-button" label="Kunde hinzufügen" icon="pi pi-user" @click="
            openAddCustomerMode
        " />
        <Dialog v-model:visible="visible" modal header="Kunden erstellen" resizable>
            <div class="item-container">
                <div class="column-left">
                    <div class="item-group">
                        <div class="items-alone">
                            <label class="text">Privatperson</label>
                            <ToggleSwitch v-model="newCustomer.private" />
                        </div>
                        <div class="items-alone" v-if="!newCustomer.private">
                            <label class="text">Firma*</label>
                            <InputText id="account_number" v-model="newCustomer.company" class="flex-auto"
                                autocomplete="off" placeholder="Musterfirma GmbH" />
                        </div>
                        <div class="items-alone">
                            <label class="text">IBAN*</label>
                            <InputText id="account_number" v-model="newCustomer.account_number" class="flex-auto"
                                autocomplete="off" placeholder="DE01 2345 6789 1011 1213 14" />
                        </div>

                        <div class="items-alone">
                            <label class="text">Steuernummer*</label>
                            <InputText id="account_number" v-model="newCustomer.tax_number" class="flex-auto"
                                autocomplete="off" placeholder="012345678910" />
                        </div>
                    </div>
                    <div class="item-group">
                        <label class="group-text">Kontaktpersonen</label>
                        <div class="items">
                            <label class="text">Kontakt 1*</label>
                            <InputText id="contact1" v-model="newCustomer.contacts[0]" class="flex-auto"
                                autocomplete="off" placeholder="Max Mustermann" />
                        </div>
                        <div class="items">
                            <label class="text">Kontakt 2</label>
                            <InputText id="contact2" v-model="newCustomer.contacts[1]" class="flex-auto"
                                autocomplete="off" placeholder="Max Mustermann" />
                        </div>
                        <div class="items">
                            <label class="text">Kontakt 3</label>
                            <InputText id="contact3" v-model="newCustomer.contacts[2]" class="flex-auto"
                                autocomplete="off" placeholder="Max Mustermann" />
                        </div>
                    </div>
                    <div class="item-group">
                        <label class="group-text">E-Mail-Adressen</label>
                        <div class="items">
                            <label class="text">E-Mail 1*</label>
                            <InputText id="email1" v-model="newCustomer.emails[0]" class="flex-auto" autocomplete="off"
                                placeholder="Max.Mustermann@gmail.com" />
                        </div>
                        <div class="items">
                            <label class="text">E-Mail 2</label>
                            <InputText id="email2" v-model="newCustomer.emails[1]" class="flex-auto" autocomplete="off"
                                placeholder="Max.Mustermann@gmail.com" />
                        </div>
                        <div class="items">
                            <label class="text">E-Mail 3</label>
                            <InputText id="email3" v-model="newCustomer.emails[2]" class="flex-auto" autocomplete="off"
                                placeholder="Max.Mustermann@gmail.com" />
                        </div>
                    </div>
                    <div class="item-group">
                        <label class="group-text">Telefonnummern</label>
                        <div class="items">
                            <label class="text">Telef-Nr. 1*</label>
                            <InputText id="phone1" v-model="newCustomer.phone_numbers[0]" class="flex-auto"
                                autocomplete="off" placeholder="+4912345678910" />
                        </div>
                        <div class="items">
                            <label class="text">Telef-Nr. 2</label>
                            <InputText id="phone2" v-model="newCustomer.phone_numbers[1]" class="flex-auto"
                                autocomplete="off" placeholder="+4912345678910" />
                        </div>
                        <div class="items">
                            <label class="text">Telef-Nr. 3</label>
                            <InputText id="phone3" v-model="newCustomer.phone_numbers[2]" class="flex-auto"
                                autocomplete="off" placeholder="+4912345678910" />
                        </div>
                    </div>
                </div>
                <div class="column-right">
                    <div class="item-group" v-for="(address, index) in newCustomer.delivery_address" :key="index">
                        <label class="group-text">Lieferadresse {{index}}</label>
                        <div class="items-group" >
                            <div class="items">
                                <label class="text">Land*</label>
                                <InputText id="'country-' + index" v-model="address.country" class="flex-auto"
                                    autocomplete="off" placeholder="Musterland" />
                            </div>
                            <div class="items">
                                <label class="text">Stadt*</label>
                                <InputText id="'city-' + index" v-model="address.city" class="flex-auto"
                                    autocomplete="off" placeholder="Musterhausen" />
                            </div>
                            <div class="items">
                                <label class="text">Postleitzahl*</label>
                                <InputText id="'postal_code-' + index" v-model="address.postal_code"
                                    class="flex-auto" autocomplete="off" placeholder="12345" />
                            </div>
                            <div class="items">
                                <label class="text">Straße*</label>
                                <InputText id="'street-' + index" v-model="address.street" class="flex-auto"
                                    autocomplete="off" placeholder="Musterstraße" />
                            </div>
                            <div class="items">
                                <label class="text">Hausnummer*</label>
                                <InputText id="'house_number-' + index" v-model="address.house_number"
                                    class="flex-auto" autocomplete="off" placeholder="1a" />
                            </div>
                        </div>
                    </div>
                    <div class="items">
                        <Button outlined @click="addDeliveryAddress">Weitere Adresse hinzufügen</Button>
                    </div>    
                    <div class="item-group">
                        <div v-if="!multipleDeliveryAddress" class="items-alone">
                            <label class="text">Abweichende Rechnungsadresse?</label>
                            <ToggleSwitch v-model="showRechnungsadresse" />
                        </div>
                        <label v-if="showRechnungsadresse" class="group-text">Rechnungsadresse</label>
                        <div v-if="showRechnungsadresse" class="items">
                            <label class="text">Land*</label>
                            <InputText id="country" v-model="newCustomer.billing_address.country" class="flex-auto"
                                autocomplete="off" placeholder="Musterland" />
                        </div>
                        <div v-if="showRechnungsadresse" class="items">
                            <label class="text">Stadt*</label>
                            <InputText id="city" v-model="newCustomer.billing_address.city" class="flex-auto"
                                autocomplete="off" placeholder="Musterhausen" />
                        </div>
                        <div v-if="showRechnungsadresse" class="items">
                            <label class="text">Postleitzahl*</label>
                            <InputText id="postal_code" v-model="newCustomer.billing_address.postal_code"
                                class="flex-auto" autocomplete="off" placeholder="12345" />
                        </div>
                        <div v-if="showRechnungsadresse" class="items">
                            <label class="text">Straße*</label>
                            <InputText id="street" v-model="newCustomer.billing_address.street" class="flex-auto"
                                autocomplete="off" placeholder="Musterstraße" />
                        </div>
                        <div v-if="showRechnungsadresse" class="items">
                            <label class="text">Hausnummer*</label>
                            <InputText id="house_number" v-model="newCustomer.billing_address.house_number"
                                class="flex-auto" autocomplete="off" placeholder="1a" />
                        </div>
                    </div>
                    <div class="items-notes">
                        <label class="text">Notizen</label>
                        <Editor id="notes" v-model="newCustomer.notes" editorStyle="height: 300px"
                            placeholder="Notizen schreiben..." />
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <div class="dialog-footer-left">
                        <span class="footer-note">*Pflichtfelder</span>
                    </div>
                    <div class="buttons">
                        <Button type="button" label="Abbrechen" severity="secondary" @click="closeAddCustomerMode"
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
    name: "AddCustomerButton",
    emits: ["addCustomerData"],
    components: {
        Button,
        Dialog,
        InputText,
        Editor,
        ToggleSwitch,
        Select,
        Toast,
    },
    data() {
        return {
            visible: false,
            showRechnungsadresse: false,
            multipleDeliveryAddress: false,
            newCustomer: {
                "account_number": "",
                "billing_address": {
                    "city": "",
                    "country": "",
                    "house_number": "",
                    "postal_code": "",
                    "street": ""
                },
                "company": "",
                "contacts": [
                    "",
                    "",
                    ""
                ],
                "delivery_address": [
                    {
                        "city": "",
                        "country": "",
                        "house_number": "",
                        "postal_code": "",
                        "street": ""
                    }
                ],
                "emails": [
                    "",
                    "",
                    ""
                ],
                "notes": "",
                "phone_numbers": [
                    "",
                    "",
                    ""
                ],
                "private": false,
                "tax_number": ""
            }
        };
    },
    methods: {

        addDeliveryAddress(){
            this.multipleDeliveryAddress = true;
            this.newCustomer.delivery_address.push({
                city:"",
                country:"",
                house_number: "",
                postal_code: "",
                street: ""
            })
        },  

        async sendDataToBackend() {
            if (!this.showRechnungsadresse) this.newCustomer.billing_address = this.newCustomer.delivery_address[0];
            if (
                !this.newCustomer.account_number ||
                !this.newCustomer.billing_address ||
                !this.newCustomer.billing_address.city ||
                !this.newCustomer.billing_address.country ||
                !this.newCustomer.billing_address.house_number ||
                !this.newCustomer.billing_address.postal_code ||
                !this.newCustomer.billing_address.street ||
                this.newCustomer.contacts[0] === '' ||
                !this.newCustomer.contacts.length ||
                !this.newCustomer.delivery_address[0] ||
                !this.newCustomer.delivery_address[0].city ||
                !this.newCustomer.delivery_address[0].country ||
                !this.newCustomer.delivery_address[0].house_number ||
                !this.newCustomer.delivery_address[0].postal_code ||
                !this.newCustomer.delivery_address[0].street ||
                this.newCustomer.emails[0] === '' ||
                !this.newCustomer.emails.length ||
                this.newCustomer.phone_numbers[0] === '' ||
                !this.newCustomer.phone_numbers.length ||
                !this.newCustomer.tax_number ||
                !this.newCustomer.private && !this.newCustomer.company
            ) {
                this.$refs.toast.toastAddError(
                    "Bitte weisen Sie dem Kunden alle Pflichtfelder zu."
                );
                return;
            }
            let customer = {
                ...this.newCustomer
            };
            customer = toRaw(customer);
            try {
                const response = await fetch(`${baseUrl}/api/customers`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(customer),
                    credentials: "include",
                });
                if (!response.ok) {
                    throw new Error(`HTTP error. Status: ${response.status}`);
                }
                this.$refs.toast.toastAddSuccess(
                    "Kunde wurde erfolgreich erstellt"
                );
                this.$emit("addCustomerData");
                this.closeAddCustomerMode();
            } catch (error) {
                this.$refs.toast.toastAddError(
                    "Kunde konnte nicht erstellt werden"
                );
                console.error("Upload error:", error);
            }
        },

        closeAddCustomerMode() {
            this.visible = false;
            this.showRechnungsadresse = false;
            this.newCustomer = {
                "account_number": "",
                "billing_address": {
                    "city": "",
                    "country": "",
                    "house_number": "",
                    "postal_code": "",
                    "street": ""
                },
                "company": "",
                "contacts": [
                    "",
                    "",
                    ""
                ],
                "delivery_address": [
                    {
                        "city": "",
                        "country": "",
                        "house_number": "",
                        "postal_code": "",
                        "street": ""
                    }
                ],
                "emails": [
                    "",
                    "",
                    ""
                ],
                "notes": "",
                "phone_numbers": [
                    "",
                    "",
                    ""
                ],
                "private": false,
                "tax_number": ""
            }
        },

        openAddCustomerMode() {
            this.visible = true;
            this.showRechnungsadresse = false;
            this.newCustomer = {
                "account_number": "",
                "billing_address": {
                    "city": "",
                    "country": "",
                    "house_number": "",
                    "postal_code": "",
                    "street": ""
                },
                "company": "",
                "contacts": [
                    "",
                    "",
                    ""
                ],
                "delivery_address": [
                    {
                        "city": "",
                        "country": "",
                        "house_number": "",
                        "postal_code": "",
                        "street": ""
                    }
                ],
                "emails": [
                    "",
                    "",
                    ""
                ],
                "notes": "",
                "phone_numbers": [
                    "",
                    "",
                    ""
                ],
                "private": false,
                "tax_number": ""
            }
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

.custom-add-customer-button {
    background-color: var(--color-secondary) !important;
    border: 1px solid var(--color-secondary) !important;
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