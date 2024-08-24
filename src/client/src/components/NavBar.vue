<script setup lang="ts">
import IconDocumentation from './icons/IconDocumentation.vue'
import NavBarItem from './NavBarItem.vue'
</script>

<script lang="ts">
/**
 * NavBar component represents the navigation bar for the application.
 *
 * This component includes the title of the application and a set of navigation items.
 * Each navigation item is represented by the NavBarItem component. 
 *
 * @example
 * <NavBar />
 */
export default {
  name: 'NavBar',
}
</script>

<template>
  <nav class="navbar">
    <p id="navbar-title" @click="$router.push('/')">iso15926vis</p>
    <div class="navbar-items">
      <NavBarItem to="/" label="Home" />
      <NavBarItem to="/graph" label="Graph" />
      <NavBarItem to="/documentation" label="Documentation">
        <template #icon>
          <IconDocumentation class="navbar-icon" />
        </template>
      </NavBarItem>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  font-size: 16px;
  /* Ensures NavBar items are on NavBar */
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

#navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: auto;
  color: var(--color-nav-title);
}

#navbar-title:hover {
  cursor: pointer;
}

.navbar-items {
  /* Centres items in navbar vertically i.e. row instead of column */
  display: flex;
  /* Centres items in navbar horizontally - currently right aligned*/
  /* margin-right: auto; */
}

.navbar-icon {
  vertical-align: middle;
  margin-right: 0.4rem;
  margin-top: 0.3rem;
}
</style>
