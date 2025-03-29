<template>
    <div></div>
  </template>
  
  <script>
  export default {
    components: {},
    data() {
      return {};
    },
    methods: {
      toastAddSuccess(text) {
        this.$toast.add({
          severity: "success",
          summary: "Success",
          detail: text,
          life: 3000,
        });
      },
      toastAddError(text) {
        this.$toast.add({
          severity: "error",
          summary: "Error",
          detail: text,
          life: 3000,
        });
      },
      toastAddGeneral(text) {
        this.$toast.add({
          severity: "secondary",
          summary: "Error",
          detail: text,
          life: 3000,
        });
      },
    },
  };
  </script>
  