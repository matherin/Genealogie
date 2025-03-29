<template>
    <div class="footer-container">
      <div class="footer-container-table">
        <table>
          <thead>
            <tr>
              <th>Metcera-Recycling</th>
              <th>Kontaktinformationen</th>
              <th>Öffnungszeiten</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <a href="https://www.metcera-recycling.de">Metcera GmbH</a>
              </td>
              <td>E-Mail: info@metcera-recycling.de</td>
              <td style="font-weight: bold;">Montag bis Freitag:</td>
            </tr>
            <tr>
              <td>Sestewitzer Str. 7</td>
              <td>Tel.: 034297 - 778066</td>
              <td>8:00 - 12:00 Uhr, 12:30- 16:30 Uhr</td>
            </tr>
            <tr>
              <td>04463 Großpösna</td>
              <td></td>
              <td style="font-weight: bold;">Samstag und Sonntag:</td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td>geschlossen</td>
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
  