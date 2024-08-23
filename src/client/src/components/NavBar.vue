<script setup lang="ts">
import IconDocumentation from './icons/IconDocumentation.vue'
import NavBarItem from './NavBarItem.vue'
</script>

<template>
  <nav class="navbar">
    <NavBarItem to="/" label="Home" />
    <NavBarItem to="/graph" label="Graph" />
    <NavBarItem to="/documentation" label="Documentation">
      <template #icon>
        <IconDocumentation class="navbar-icon" />
      </template>
    </NavBarItem>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  font-size: 16px;
  /* Centres items in navbar horizontally */
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  background-color: var(--color-nav-background);
  /* To ensure navbar is always on top */
  z-index: 1000;
  padding: 1rem 2rem;
  box-shadow: 0 1px 4px var(--color-nav-background);
}

.navbar-icon {
  vertical-align: middle;
  margin-right: 0.4rem;
  margin-bottom: 0.2rem;
}
</style>
