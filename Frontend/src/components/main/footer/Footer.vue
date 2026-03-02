<template>
    <div class="footer-container">
      <div class="footer-container-table">
        <p>This is a project for the module "Computergenealogie und digitale Sozialgeschichte" at the Leipzig University. </p>
        <p>We use the US census Data from Pittsburgh and Allegheny from the following site: 
          <a href="https://exhibit.library.pitt.edu/census/" target="_blank">
          https://exhibit.library.pitt.edu/census/
        </a> </p>
        <p>There is no direct affiliation between this site and the data origin.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AppFooter",
  };
  </script>
  
  <style scoped>
  .footer-container {
    min-height: 300px;
    background-color: #272f36;
    color: var(--color-basic);
    width: 100vw;
    min-width: 1250px;
    display: flex;
    align-items: left;
  }
  
  .footer-container-table {
    padding: 50px;
    display: flex;
    width: 100vw;
    min-width: 700px;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }
  
  p {
    width: 50%;
    padding: 8px;
    padding-bottom: 15px;
    text-align: center;
  }
  
  a {
    color: var(--color-font-basic-two);
  }
  </style>
  