<script setup lang="ts">
import IconDocumentation from './icons/IconDocumentation.vue'
import IconGraph from './icons/IconGraph.vue'
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
  name: 'NavBar'
}
</script>

<template>
  <nav id="navbar" class="w-full bg-nav-background py-4 px-8 flex justify-center fixed top-0 left-0 z-50 text-[1.1rem] shadow-md md:py-4 md:px-4 md:text-[1rem]">
    <p id="navbar-title" @click="$router.push('/')" class="text-[1.5rem] md:text-[1.2rem] font-bold mr-auto text-nav-title hover:cursor-pointer">
      iso15926vis
    </p>
    <div id="navbar-items" class="flex">
      <NavBarItem to="/" label="Home" id="home-link" class="hidden md:inline" />
      <NavBarItem to="/graph" label="Graph" id="graph-link" class="border-0">
        <template #icon>
          <IconGraph class="navbar-icon mr-2 mt-1 align-middle" />
        </template>
      </NavBarItem>
      <NavBarItem to="https://docs.iso15926vis.org/" label="Documentation" id="documentation-link">
        <template #icon>
          <IconDocumentation class="navbar-icon mr-2 mt-1 align-middle" />
        </template>
      </NavBarItem>
    </div>
  </nav>
</template>

<style scoped>
#navbar {
  width: 100%;
  font-size: 1.1rem;
  /* Ensures NavBar items are on NavBar */
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  /* background-color: var(--color-nav-background); */
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

@media screen and (max-width: 1024px) {
  .navbar {
    padding: 1rem;
    font-size: 1rem;
  }
  #navbar-title {
    font-size: 1.2rem;
  }
  #home-link {
    display: none;
  }
  #graph-link {
    border: 0;
  }
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
