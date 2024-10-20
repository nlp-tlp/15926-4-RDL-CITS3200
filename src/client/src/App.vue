<script setup lang="ts">
import { RouterView } from 'vue-router'

import NavBar from './components/NavBar.vue'
</script>

<template>
  <div id="container">
    <header class="flex place-items-start max-h-screen leading-7 lg:pr-section-gap-half">
      <div class="flex place-items-center flex-wrap">
        <NavBar />
      </div>
    </header>

    <main id="main-content" class="bg-background py-8">
      <RouterView />
    </main>
  </div>
</template>
