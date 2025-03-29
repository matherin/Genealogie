<template>
    <div class="footer-container">
      <div class="footer-container-table">
        <table>
          <thead>
            <tr>
              <th>Zusatzinformationen</th>
              <th>Lebenshilfe Borna</th>
              <th>Kontaktinformationen</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Diese Website ist durch eine</td>
              <td>
                <a href="https://lebenshilfe-borna.de/?page_id=39">Borna GmbH</a>
              </td>
              <td>E-Mail: TestMail@gmail.com</td>
            </tr>
            <tr>
              <td>Kooperation zwischen der</td>
              <td>E-Mail: info@lebenshilfe-borna.de</td>
              <td></td>
            </tr>
            <tr>
              <td>Lebenshilfe-Borna und der</td>
              <td>Tel.: 03433/ 20979-0</td>
              <td></td>
            </tr>
            <tr>
              <td>Universität Leipzig entstanden.</td>
              <td>Am Wilhelmschacht 1</td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td>04552 Borna</td>
              <td></td>
            </tr>
          </tbody>
        </table>
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
    flex-direction: column;
    align-items: left;
  }
  
  .footer-container-table {
    padding: 50px;
    display: flex;
    width: 100vw;
    min-width: 700px;
    align-items: center;
    justify-content: center;
  }
  
  table {
    margin-top: 0px;
    width: 70%;
    border-collapse: separate;
    border-spacing: 100px 0px;
  }
  
  th,
  td {
    width: 30%;
    padding: 8px;
    padding-bottom: 15px;
    text-align: left;
  }
  
  td {
    padding-bottom: 0px;
    padding-top: 5px;
    color: var(--color-font-basic-two);
  }
  
  a {
    color: var(--color-font-basic-two);
  }
  </style>
  