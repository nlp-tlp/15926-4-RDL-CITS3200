<script setup lang="ts"></script>

<template>
  <div class="page">
    <section class="overview">
      <h1>Interactive Visualization of the ISO 15926-4 Reference Data Library</h1>
      <h2 class="section1">Overview: ISO and RDL</h2>
      <p>
        The International Organization for Standardization (ISO) develops and publishes standards. ISO 15926-4 standard has the title Industrial automation systems and integration — Integration of life-cycle data for process plants including oil and gas production facilities Part 4: Core reference data. The Reference Data Library (RDL) described in ISO 15926-4 is made available as a set of spreadsheets and through an endpoint. 
      </p>
    </section>

    <section class="purpose">
      <h2 class="section2">Purpose of this Visualization</h2>
      <p>
        The goal of this webpage is to allow users of the RDL to explore and understand the hierarchy and relationships between classes and their superclasses in the RDL. 
      </p>
    </section>

    <section class="explore">
      <p>Click the button below to explore the interactive visualization</p>
      <router-link to="/graph">
        <button>Graph</button>
      </router-link>
    </section>

    <section class="attribution">
      <p>
        The following UWA students developed and designed this visualization:<br />
        <strong
          >Cameron O'Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, Vinita Rathore</strong
        >
      </p>
    </section>

    <section class="logos">
      <a href="https://www.uwa.edu.au/" class="logoURL" target="_blank">
        <img src="/images/UWA Logo.png" class="logo1" alt="University of Western Australia Logo" />
      </a>
      <a href="https://nlp-tlp.org/" class="logoURL" target="_blank">
        <img
          src="/images/nlp-tlp-logo.png"
          class="logo2"
          alt="University of Western Australia Natural & Technical Language Processing Group Logo"
        />
      </a>
    </section>

    <section class="disclaimer">
      <h4>Disclaimer:</h4>
      <p>
        This project is not sponsored by the International Organization for Standardization (ISO).
        It is an initiative of the University of Western Australia (UWA) and is intended to assist
        the ISO/TC 184/SC 4 Committee.
      </p>
    </section>
  </div>
</template>

<style scoped>
.page {
  text-align: justify;
  color: black;
  margin-bottom: 70px;
}
.overview {
  margin-top: 120px;
  margin-bottom: 70px;
}
h1 {
  text-align: center;
  font-size: xx-large;
  font-weight: bold;
}
.section1 {
  margin-top: 70px;
  margin-bottom: 10px;
  font-weight: 600;
  position: relative;
}
.section1::before {
  content: '';
  position: absolute;
  bottom: -10px;
  width: 25%;
  height: 2px;
  background-color: black;
}
.overview p {
  text-align: block;
  margin-top: 30px;
}
.purpose {
  margin-bottom: 90px;
}
.section2 {
  margin-bottom: 10px;
  font-weight: 600;
  position: relative;
}
.section2::before {
  content: '';
  position: absolute;
  bottom: -10px;
  width: 30%;
  height: 2px;
  background-color: black;
}
.purpose p {
  margin-top: 30px;
}
.explore {
  margin-bottom: 85px;
  text-align: center;
  position: relative;
  padding: 50px 50px;
}
.explore::before {
  content: '';
  position: absolute;
  top: -20px;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: black;
}
.explore p {
  font-size: large;
  margin-bottom: 45px;
}
button {
  border: none;
  background-color: black;
  color: white;
  font-size: medium;
  font-weight: 900;
  padding: 16px 120px;
  cursor: pointer;
}
button:hover {
  background-color: gray;
}
.explore::after {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 0;
  width: 100%;
  height: 0.5px;
  background-color: black;
}
.attribution {
  margin-bottom: 60px;
  text-align: center;
}
.attribution strong {
  font-weight: 500;
}
.logos {
  text-align: center;
  margin-bottom: 50px;
}
.logo1 {
  max-width: 188px;
  margin-right: 52px;
  margin-bottom: 11.5px;
}
.logo2 {
  max-width: 90px;
}
.logoURL {
  display: inline-block;
  background-color: transparent;
  cursor: pointer;
}
.disclaimer {
  text-align: center;
  font-size: small;
}
h4 {
  font-weight: 500;
}
</style>
