<template>
    <div class="login-container">
      <div class="login-container-left">
        <div class="login-container-left-header">
          <a
            class="login-container-left-header-item"
            href="https://www.metcera-recycling.de"
            >Metcera-Recycling</a
          >
        </div>
        <Transition :css="false" appear @enter="onEnter" @appear="onEnter">
          <div class="login-container-left-body">
            <p class="login-container-left-body-title">Metci</p>
            <p class="login-container-left-body-subtitle">
              Diese Seite dient der Verwaltung der Betriebsinternen Daten von Metcera-Recycling.
            </p>
          </div>
        </Transition>
      </div>
      <div ref="box" class="login-container-right">
        <Transition :css="false" appear @appear="onEnter" @enter="onEnter">
          <LoginForm />
        </Transition>
      </div>
    </div>
  </template>
  
  <script>
  import LoginForm from "./LoginForm.vue";
  import { animate } from "motion";
  import { ref } from "vue";
  
  export default {
    name: "LogiN",
  
    components: {
      LoginForm,
    },
  
    data() {
      return {
        box: ref(null),
      };
    },
    methods: {
      async onEnter(el, onComplete) {
        el.style.opacity = 0;
        el.style.transform = "translateY(-10px)";
        const delay = el.classList.contains("login-form-container") ? 0.1 : 0;
  
        await animate(
          el,
          { opacity: 1, transform: ["translateY(-10px)", "translateY(0px)"] },
          { duration: 0.5, easing: "ease-out", delay }
        );
        onComplete();
      },
    },
  };
  </script>
  
  <style>
  .login-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100vw;
    height: 100vh;
    background-color: #fff;
  }
  
  .login-container-right {
    width: 31.25vw;
    min-width: 500px;
    max-width: 600px;
    height: 100vh;
    max-height: 100vh;
    background: linear-gradient(to bottom, #283d4d, #1b2c39);
  
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .login-container-left {
    flex: 1;
  }
  
  .login-container-left-header {
    display: flex;
    flex-direction: row-reverse;
    width: 100%;
    margin: 20px;
    margin-left: -30px;
  }
  
  .login-container-left-header-item {
    margin-left: 40px;
    color: var(--color-font-primary);
    text-decoration: none;
    text-decoration-line: underline;
  }
  
  .login-container-left-body {
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: left;
    margin-left: 16vw;
  }
  
  .login-container-left-body-title {
    font-size: 3.5rem;
    font-weight: 300;
    letter-spacing: -2.5px;
    font-family: var(--font-family2);
  
    margin-top: 15vh;
    margin-bottom: 5px;
    color: var(--color-font-primary);
  }
  
  .login-container-left-body-subtitle {
    font-size: var(--font-size-normal);
    color: var(--color-font-primary-lighter);
    font-weight: 400;
    width: 650px;
    text-align: left;
  }
  
  .login-container-left-body-title::after {
    position: absolute;
    content: "";
    left: 0;
    top: 0;
    height: 46px;
    width: 0px;
    background-color: var(--color-secondary);
  }
  </style>
  