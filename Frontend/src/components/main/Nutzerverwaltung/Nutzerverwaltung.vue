<template>
    <div class="user-table">
      <Toast ref="toast" />
      <DataTable
        dataKey="id"
        :value="this.currentlyLoading ? this.placeholderRows : this.userData"
        size="small"
        removableSort
        tableStyle="width: 80vw"
        responsiveLayout="scroll"
        paginator
        :rows="12"
        :filters="filters"
        :globalFilterFields="[
          'account_id',
          'vorname',
          'nachname',
          'role',
          'gruppe',
        ]"
      >
        <template #header>
          <div class="user-table-header">
            <p class="user-table-header-title">Nutzeransicht</p>
            <div class="user-table-header-button-container">
              <IconField class="user-table-header-button">
                <!--<AddUserButton @addUserData="fetchUserData" />-->
              </IconField>
              <IconField class="user-table-header-button">
                <InputIcon class="pi pi-search" />
                <InputText
                  v-model="filters['global'].value"
                  placeholder="Suchen"
                  icon="pi pi-search"
                />
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
            <span v-else v-html="highlightText(data.account_id)" />
          </template>
        </Column>
        <Column field="vorname" header="Vorname" sortable style="width: 20%">
          <template #body="{ data }">
            <Skeleton v-if="this.currentlyLoading" width="50%" />
            <span v-else v-html="highlightText(data.vorname)" />
          </template>
        </Column>
        <Column field="nachname" header="Nachname" sortable style="width: 20%">
          <template #body="{ data }">
            <Skeleton v-if="this.currentlyLoading" width="50%" />
            <span v-else v-html="highlightText(data.nachname)" />
          </template>
        </Column>
        <Column field="role" header="Rolle" sortable style="width: 10%">
          <template #body="{ data }">
            <Skeleton v-if="this.currentlyLoading" width="70%" />
            <span v-else v-html="highlightText(data.role)" />
          </template>
        </Column>
        <Column field="location" header="Standort" sortable style="width: 20%">
          <template #body="{ data }">
            <Skeleton v-if="this.currentlyLoading" width="40%" />
            <span v-else>
              {{ data.groups?.length ? highlightText(data.groups[0].location_name) : highlightText(data.fallbackLocationName || 'N/A') }}
            </span>
          </template>
        </Column>
        <Column field="groups" header="Gruppe" sortable style="width: 20%">
          <template #body="{ data }">
            <Skeleton v-if="this.currentlyLoading" width="40%" />
            <span
              v-else
              v-html="
                highlightText(
                  data.groups?.length ? data.groups[0].group_name : 'N/A'
                )
              "
            />
          </template>
        </Column>
        <Column header="Aktionen" style="width: 10%">
          <template #body="slotProps">
            <Skeleton v-if="this.currentlyLoading" width="100%" />
            <div v-else class="row">
              <div class="space">
                <!--<EditUserButton
                  :editableUser="slotProps.data"
                  @editUserData="fetchUserData"
                />-->
              </div>
              <div class="space">
                <DeleteUserButton
                  :deleteUser="slotProps.data.account_id"
                  @deleteUserData="fetchUserData"
                />
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
  
  const FilterMatchMode = { CONTAINS: "contains" };
  
  var baseUrl = window.location.origin;
  
  export default {
    name: "NutzerverwaltungTable",
    components: {
      DeleteUserButton,
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
        messageVisible: false,
        currentlyLoading: true,
        locationCache:{},
        placeholderRows: Array.from({ length: 12 }, () => ({
          account_id: 0,
          vorname: "",
          nachname: "",
          role: "",
          groups: "",
        })),
      };
    },
    mounted() {
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        this.currentlyLoading = true;
        try{
          const response= await fetch(`${baseUrl}/api/accounts`, {
            method: "GET",
            credentials: "include",
          });
              if (!response.ok) {
                throw new Error("Network response was not ok");
              }
              const data= await response.json();
              for(const user of data){
                if(!user.groups || user.groups.length===0){
                  user.fallbackLocationName = await this.getLocationNameByID(user.location_id);
                }
              }
          
              this.userData = data;
              this.currentlyLoading = false;
            
        } catch(error){
            console.error("Error fetching data:", error);
            this.$refs.toast.toastAddError("Daten konnten nicht geladen werden");
          }
      },
  
      async getLocationNameByID(location_id){
        if(!location_id) return "N/A";
        if(this.locationCache[location_id]){
          return this.locationCache[location_id];
        }
        try{
          const response = await fetch(`${baseUrl}/api/locations/${location_id}/name`,{method: "GET", credentials: "include"});
          if(!response.ok) throw new Error("Failed to fetch location");
          const data = await response.json();
          const name = data?.name || "N/A";
          this.locationCache[location_id] = name;
          return name;
        } catch (error){
          console.error(`Error fetching location for ID ${location_id}:`, error);
          return "N/A";
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
      showMessage() {
        this.messageVisible = true;
  
        setTimeout(() => {
          this.messageVisible = false;
        }, 1800);
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
  