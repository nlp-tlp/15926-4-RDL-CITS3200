<script setup lang="ts">
import { RouterView } from 'vue-router'

import NavBar from './components/NavBar.vue'
</script>

<template>
  <div id="container">
    <header>
      <div class="wrapper">
        <NavBar />
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
header {
  line-height: 1.75;
  max-height: 100vh;
}

.main-content {
  padding-top: 4.5rem;
  padding-left: 1rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
