<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const isExpanded = ref(false);

function toggleNav() {
  isExpanded.value = !isExpanded.value;
}

function handleClickOutside(event: MouseEvent) {
  const sidepanel = document.querySelector('.sidepanel');
  const openbtn = document.querySelector('.openbtn');
  
  if (sidepanel && !sidepanel.contains(event.target as Node) && !openbtn?.contains(event.target as Node)) {
    isExpanded.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div :class="['sidepanel', { 'sidepanel-expanded': isExpanded }]">
    <a href="#">About</a>
    <a href="#">Services</a>
    <a href="#">Clients</a>
    <a href="#">Contact</a>
  </div>

  <button class="openbtn" @click="toggleNav">&#9776; Left sidepane</button>
  <h2>Collapsed Sidepanel</h2>
  <p>Content...</p>
</template>

<style scoped>
/* The sidepanel menu */
.sidepanel {
  height: 100%; /* Full height */
  width: 0; /* 0 width - change this with state */
  position: fixed; /* Stay in place */
  z-index: 1; /* Stay on top */
  top: 130px; /* Offset from top */
  left: 0;
  background-color: var(--color-nav-background); 
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 60px; /* Place content 60px from the top */
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
}

/* The sidepanel expanded state */
.sidepanel-expanded {
  width: 250px; /* Expanded width */
}

/* The sidepanel links */
.sidepanel a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 20px;
  color: var(--color-nav-title); 
  display: block;
  transition: 0.3s;
}

/* When you mouse over the navigation links, change their color */
.sidepanel a:hover {
  color: #f1f1f1;
}

/* Style the button that is used to open the sidepanel */
.openbtn {
  width: 250px; /* Match sidepanel width */
  height: 60px;
  font-size: 1.5rem; /* Match navbar title size */
  font-weight: bold; /* Match navbar title weight */
  cursor: pointer;
  background-color: var(--color-nav-background); 
  color: var(--color-nav-title); 
  padding: 10px 0px;
  border: none;
  position: absolute; 
  top: 74px; /* Adjust top value to ensure it doesn't overlap */
  left: 0;            
}

.openbtn:hover {
  background-color: #444;
}
</style>
