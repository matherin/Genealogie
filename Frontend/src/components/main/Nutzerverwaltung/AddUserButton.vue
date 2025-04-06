<template>
    <div>
        <Toast ref="toast" />
        <Button class="custom-add-user-button" label="Nutzer hinzufügen" icon="pi pi-user" @click="
            visible = true;
        setPassword();
        " />
        <Dialog v-model:visible="visible" modal header="Nutzer hinzufügen" :style="{ width: '30rem' }">
            <div class="items">
                <label for="username" class="text">Nutzername</label>
                <InputText id="username" v-model="newUser.username" class="flex-auto" autocomplete="off"
                    placeholder="Username eingeben" />
            </div>
            <div class="items">
                <label for="role" class="text">Rolle</label>
                <Select v-model="newUser.role" optionValue="role" :options="rollen" optionLabel="role"
                    placeholder="Rolle auswählen" />
            </div>
            <div class="items-password">
                <label class="password-text">Passwort:</label>
                <label>{{ this.newPassword }}</label>
                <Button @click="copyPassword" icon="pi pi-clone" class="copy-User" />
            </div>
            <div class="buttons">
                <Button type="button" label="Abbrechen" severity="secondary" @click="closeAddUserMode"></Button>
                <Button type="button" label="Speichern" @click="sendNewUserDataToBackend"></Button>
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
    emits: ["addUserData"],
    components: {
        Button,
        Dialog,
        InputText,
        Select,
        Toast,
    },
    data() {
        return {
            visible: false,
            hashedPassword: "",
            newPassword: "",
            newUser: {
                role: "",
                username: "",
                password: "",
            },
            rollen: [{ role: "Nutzer" }, { role: "Administrator" }],
        };
    },
    methods: {
        async sendNewUserDataToBackend() {
            if (!this.newUser.username || !this.newUser.role) {
                this.$refs.toast.toastAddError(
                    "Bitte füllen Sie alle Felder aus."
                );
                return;
            }
            const roleMap={
                Nutzer: "user",
                Administrator: "admin",
            };
            let user = {
                ...this.newUser, 
                role: roleMap[this.newUser.role],
                password: this.hashedPassword
            };
            user = toRaw(user);
            try {
                const response = await fetch(`${baseUrl}/api/users`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(user), credentials: 'include' });
                if (!response.ok) {
                    throw new Error(`HTTP error. Status: ${response.status}`);
                }
                this.$refs.toast.toastAddSuccess("Nutzer erfolgreich hinzugefügt");
                this.$emit('addUserData');
                this.closeAddUserMode();
            } catch (error) {
                console.error("Upload error:", error);
                this.$refs.toast.toastAddError("Nutzer konnte nicht hinzugefügt werden");
            }
        },

        copyPassword() {
            const text = this.newPassword;
            navigator.clipboard.writeText(text).then(() => {
                this.$refs.toast.toastAddSuccess("Passwort wurde kopiert");
            }).catch(err => {
                console.error('Failed to copy: ', err);
                this.$refs.toast.toastAddError("Passwort konnte nicht kopiert werden");
            });
        },

        closeAddUserMode() {
            this.visible = false;
            this.newUser = {
                role: "",
                username: "",
                password: "",
            };
        },

        async setPassword() {
            this.hashedPassword = await this.generateHashedPassword(
                this.generatePassword(12)
            );
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

<style scoped>
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
    width: 40px;
}

.password-text {
    font-weight: 600;
}

.buttons {
    display: flex;
    justify-content: end;
    gap: 1rem;
    margin-top: 1rem;
}

.flex-auto {
    display: flex;
    flex: auto;
}

.custom-add-user-button {
    background-color: var(--color-secondary) !important;
    border: 1px solid var(--color-secondary) !important;
}

.custom-add-user-button:hover {
    border-color: #fdab3f !important;
    background-color: #fdab3f !important;
}

.custom-add-user-button:active {
    background-color: #c78915 !important;
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
