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
          <p class="user-table-header-title">Census Tabelle</p>
          <div class="user-table-header-button-container">
            <div class="user-table-header-search">
              <IconField class="user-table-header-button">
                <InputIcon class="pi pi-search" />
                <InputText v-model="filters['global'].value" placeholder="Search" icon="pi pi-search" />
              </IconField>
            </div>
            <div class="user-table-header-columnselect">
              <MultiSelect class="user-table-header-columnselect-toggle"
                :pt="{ labelContainer: { style: 'padding-right:2.5rem' }, clearIcon: { style: 'right:2.5rem' } }"
                :modelValue="selectedColumns" showClear selectionLimit="10" :maxSelectedLabels="5" :options="columns" optionLabel="header"
                @update:modelValue="onToggle" display="chip" :optionDisabled="isOptionDisabled" placeholder="Select Columns" />
            </div>
          </div>
        </div>
      </template>
      <template #empty> Nothing found</template>
      <Column v-for="(col, index) of selectedColumns" :field="col.field" :header="col.header"
        :key="col.field + '_' + index">
        <template #body="{ data }">
          <div class="custom-row-div" v-if="this.currentlyLoading">
            <Skeleton width="50%" />
          </div>
          <span v-else v-html="highlightText(data.id)" />
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
import Skeleton from "primevue/skeleton";
import MultiSelect from "primevue/multiselect";
import Toast from "@/components/custom/toast/Toast.vue";

const FilterMatchMode = { CONTAINS: "contains" };

var baseUrl = window.location.origin;

export default {
  name: "censusData",
  components: {
    Column,
    DataTable,
    IconField,
    InputText,
    InputIcon,
    Skeleton,
    MultiSelect,
    Toast,
  },
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      userData: [],
      currentlyLoading: true,
      selectedColumns: [],
      columns: [],
      maxColumns: 10,
    };
  },
  created() {
    this.columns = [
      { field: 'firstName', header: 'First Name' },
      { field: 'lastName', header: 'Last Name' },
      { field: 'alternateLastName', header: 'Alternate Last Name' },
      { field: 'alternateFirstName', header: 'Alternate Last Name' },
      { field: 'age', header: 'Age' },
      { field: 'monthBorn', header: 'Month Born' },
      { field: 'sex', header: 'Sex' },
      { field: 'monthMarried', header: 'Month Married' },
      { field: 'color', header: 'Color' },
      { field: 'occupation', header: 'Occupation' },
      { field: 'skillLevel', header: 'Skill Level' },
      { field: 'wardNumber', header: 'Ward Number' },
      { field: 'fatherForeignBorn', header: 'Father Foreign Born' },
      { field: 'motherForeignBorn', header: 'Mother Foreign Born' },
      { field: 'attendSchool', header: 'Attend School' },
      { field: 'read', header: 'Read' },
      { field: 'write', header: 'Write' },
      { field: 'dwelling', header: 'Dwelling' },
      { field: 'personalEstate', header: 'Personal Estate' },
      { field: 'realEstate', header: 'Real Estate' },
      { field: 'vote', header: 'Vote' },
      { field: 'sane', header: 'Sane' },
      { field: 'soundexCode', header: 'Soundex Code' },
      { field: 'alternateSoundexCode', header: 'Alternate Soundex Code' },
      { field: 'addNotes', header: 'Additional Notes' }
    ];
    this.selectedColumns = this.columns.slice(0, 2);
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    isOptionDisabled(option) {
      if (!this.selectedColumns) return false;
      return (
        this.selectedColumns.length >= this.maxColumns && !this.selectedColumns.includes(option)
      );
    },
    onToggle(value) {
      this.selectedColumns = value;
    },
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
        const roleMap = {
          user: "Nutzer",
          admin: "Administrator",
        };
        this.userData = data.map(user => ({
          ...user,
          role: roleMap[user.role] || user.role
        }));
        this.currentlyLoading = false;
      } catch (error) {
        console.error("Error fetching data:", error);
        this.$refs.toast.toastAddError("Data could not load");
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

.user-table-header-columnselect {
  margin-left: 10px;
}
</style>
