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
 * Each navigation item is represented by the {@link NavBarItem} component.
 *
 * @example
 * <NavBar />
 */
export default {
  name: 'NavBar'
}
</script>

<template>
  <nav
    id="navbar"
    class="w-full bg-nav-background py-4 px-4 sm:px-8 flex justify-center fixed top-0 left-0 z-50 text-[1rem] shadow-nav-custom md:py-5 md:px-4 md:text-[1.1rem]"
  >
    <p
      id="navbar-title"
      @click="$router.push('/')"
      class="hidden md:inline mt-1 text-[1.2rem] md:text-[1.1rem] font-bold mr-auto text-gray-200 hover:cursor-pointer"
    >
      Iso15926Visualiser
    </p>
    <p
      id="navbar-title"
      @click="$router.push('/')"
      class="text-[1.2rem mt-1 md:text-[1.1rem] font-bold mr-auto text-gray-200 hover:cursor-pointer md:hidden"
    >
      Iso15926Vis
    </p>
    <div id="navbar-items" class="flex">
      <NavBarItem to="/" label="Home" id="home-link" class="hidden md:flex" />
      <NavBarItem to="/graph" label="Graph" id="graph-link" class="flex !border-l-0 md:!border-l-2">
        <template #icon>
          <IconGraph class="navbar-icon mr-2 mt-1 align-middle" />
        </template>
      </NavBarItem>
      <NavBarItem
        to="https://docs.iso15926vis.org/"
        label="Documentation"
        id="documentation-link"
        class="flex"
      >
        <template #icon>
          <IconDocumentation class="navbar-icon mr-2 mt-1 align-middle" />
        </template>
      </NavBarItem>
    </div>
  </nav>
</template>
