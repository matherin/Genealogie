<template>
  <div class="user-table">
    <Toast ref="toast" />
    <DataTable dataKey="id" :value="this.currentlyLoading ? this.placeholderRows : this.userData" size="small"
      removableSort tableStyle="width: 80vw" responsiveLayout="scroll" paginator :rows="12" :filters="filters"
      :globalFilterFields="[
        'id',
        'username',
        'role',
      ]">
      <template #header>
        <div class="user-table-header">
          <p class="user-table-header-title">Nutzertabelle</p>
          <div class="user-table-header-button-container">
            <IconField class="user-table-header-button">
              <AddUserButton @addUserData="fetchUserData" />
            </IconField>
            <IconField class="user-table-header-button">
              <InputIcon class="pi pi-search" />
              <InputText v-model="filters['global'].value" placeholder="Suchen" icon="pi pi-search" />
            </IconField>
          </div>
        </div>
      </template>
      <template #empty> Keine Nutzer gefunden.</template>
      <Column field="account_id" header="ID" sortable style="width: 10%">
        <template #body="{ data }">
          <div class="custom-row-div" v-if="this.currentlyLoading">
            <Skeleton width="50%" />
          </div>
          <span v-else v-html="highlightText(data.id)" />
        </template>
      </Column>
      <Column field="username" header="Username" sortable style="width: 20%">
        <template #body="{ data }">
          <Skeleton v-if="this.currentlyLoading" width="50%" />
          <span v-else v-html="highlightText(data.username)" />
        </template>
      </Column>
      <Column field="role" header="Rolle" sortable style="width: 10%">
        <template #body="{ data }">
          <Skeleton v-if="this.currentlyLoading" width="70%" />
          <span v-else v-html="highlightText(data.role)" />
        </template>
      </Column>
      <Column header="Aktionen" style="width: 10%">
        <template #body="slotProps">
          <Skeleton v-if="this.currentlyLoading" width="100%" />
          <div v-else class="row">
            <div class="space">
              <EditUserButton :editableUser="slotProps.data" @editUserData="fetchUserData" />
            </div>
            <div class="space">
              <DeleteUserButton :deleteUser="slotProps.data.id" @deleteUserData="fetchUserData" />
            </div>
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import IconField from "primevue/iconfield";
import InputText from "primevue/inputtext";
import InputIcon from "primevue/inputicon";
import DeleteUserButton from "./DeleteUserButton.vue";
import Skeleton from "primevue/skeleton";
import Toast from "@/components/custom/toast/Toast.vue";
import AddUserButton from "./AddUserButton.vue";
import EditUserButton from "./EditUserButton.vue";

const FilterMatchMode = { CONTAINS: "contains" };

var baseUrl = window.location.origin;

export default {
  name: "NutzerverwaltungTable",
  components: {
    DeleteUserButton,
    AddUserButton,
    EditUserButton,
    Column,
    DataTable,
    IconField,
    InputText,
    InputIcon,
    Skeleton,
    Toast,
  },
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      userData: [],
      currentlyLoading: true,
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      this.currentlyLoading = true;
      try {
        const response = await fetch(`${baseUrl}/api/users`, {
          method: "GET",
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        this.userData = data;
        this.currentlyLoading = false;
      } catch (error) {
        console.error("Error fetching data:", error);
        this.$refs.toast.toastAddError("Daten konnten nicht geladen werden");
      }
    },

    highlightText(text) {
      const searchValue = this.filters.global.value;
      if (!searchValue || !text) return text;
      const regex = new RegExp(`(${searchValue})`, "gi");
      return text
        .toString()
        .replace(regex, '<span class="highlight">$1</span>');
    },
  },
};
</script>

<style>
.p-paginator-page-active {
  background: #a16464 !important;
}

.p-inputtext:focus {
  border-color: var(--color-secondary) !important;
}

.p-datatable-footer {
  background: #000 !important;
  color: white;
}

.user-table {
  display: flex;
  flex-direction: column;
  padding: 1vw;
  padding-top: 0rem;
  padding-bottom: 1vw;
  margin: 1vw;
  background-color: #fff;
  border-radius: 7px;
  margin-bottom: 50px;
}

.user-table-header-title {
  font-size: var(--font-size-medium);
  font-weight: 700;
}

.user-table-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;

  padding-top: 1.5vw;
  padding-bottom: 2rem;
}

.space {
  margin-right: 5px;
  max-width: 40%;
}

.row {
  align-items: row;
  display: flex;
}

.highlight {
  background-color: lightskyblue;
  font-weight: bold;
}

.custom-row-div {
  display: flex;
  min-height: 28px;
  align-items: center;
}

.user-table-header-button {
  margin-left: 10px;
}

.user-table-header-button-container {
  display: flex;
}

.user-table-header-title {
  font-size: var(--font-size-medium);
  font-weight: 700;
  }
  
</style>
  
