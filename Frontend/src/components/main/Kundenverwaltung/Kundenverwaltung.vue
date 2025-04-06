<template>
  <div class="user-table">
    <Toast ref="toast" />
    <DataTable dataKey="kid" :value="this.currentlyLoading ? this.placeholderRows : this.customerData" size="small"
      removableSort tableStyle="width: 80vw" responsiveLayout="scroll" paginator :rows="12" :filters="filters"
      :globalFilterFields="[
        'kid',
        'company',
        'contact1',
        'phone1',
      ]">
      <template #header>
        <div class="user-table-header">
          <p class="user-table-header-title">Kundentabelle</p>
          <div class="user-table-header-button-container">
            <IconField class="user-table-header-button">
              <AddCustomerButton @addCustomerData="fetchCustomerData" />
            </IconField>
            <IconField class="user-table-header-button">
              <InputIcon class="pi pi-search" />
              <InputText v-model="filters['global'].value" placeholder="Suchen" icon="pi pi-search" />
            </IconField>
          </div>
        </div>
      </template>
      <template #empty> Keine Kunden gefunden.</template>
      <Column field="kid" header="ID" sortable style="width: 10%">
        <template #body="{ data }">
          <div class="custom-row-div" v-if="this.currentlyLoading">
            <Skeleton width="50%" />
          </div>
          <span v-else v-html="highlightText(data.id)" />
        </template>
      </Column>
      <Column field="company" header="Firma" sortable style="width: 20%">
        <template #body="{ data }">
          <Skeleton v-if="this.currentlyLoading" width="50%" />
          <div v-else>
            <div v-if="!data.private">
              <span v-html="highlightText(data.company)" />
            </div>
            <div v-else>
              <span v-html="highlightText('-')" />
            </div>
          </div>
        </template>
      </Column>
      <Column field="contact1" header="Kontakt" sortable style="width: 20%">
        <template #body="{ data }">
          <Skeleton v-if="this.currentlyLoading" width="70%" />
          <span v-else v-html="highlightText(data.contacts[0])" />
        </template>
      </Column> 
      <Column field="phone1" header="Telefonnummer" sortable style="width: 15%">
        <template #body="{ data }">
          <Skeleton v-if="this.currentlyLoading" width="70%" />
          <span v-else v-html="highlightText(data.phone_numbers[0])" />
        </template>
      </Column>
      <Column header="Aktionen" style="width: 10%">
        <template #body="slotProps">
          <Skeleton v-if="this.currentlyLoading" width="100%" />
          <div v-else class="row">
            <div class="space">
              <EditCustomerButton :editableCustomer="slotProps.data" @editCustomerData="fetchCustomerData" />
            </div>
            <div class="space">
              <DeleteCustomerButton :deleteCustomer="slotProps.data.id" @deleteCustomerData="fetchCustomerData" />
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
import DeleteCustomerButton from "./DeleteCustomerButton.vue";
import Skeleton from "primevue/skeleton";
import Toast from "@/components/custom/toast/Toast.vue";
import AddCustomerButton from "./AddCustomerButton.vue";
import EditCustomerButton from "./EditCustomerButton.vue";

const FilterMatchMode = { CONTAINS: "contains" };

var baseUrl = window.location.origin;

export default {
  name: "NutzerverwaltungTable",
  components: {
    DeleteCustomerButton,
    AddCustomerButton,
    EditCustomerButton,
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
      customerData: [],
      currentlyLoading: true,
    };
  },
  mounted() {
    this.fetchCustomerData();
  },
  methods: {
    async fetchCustomerData() {
      this.currentlyLoading = true;
      try {
        const response = await fetch(`${baseUrl}/api/customers`, {
          method: "GET",
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        this.customerData = data;
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
  
