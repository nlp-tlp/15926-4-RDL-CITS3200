<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const isLeftExpanded = ref(false)
const isRightExpanded = ref(false)
const activeSection = ref('')

function toggleLeftNav() {
  isLeftExpanded.value = !isLeftExpanded.value
}

function toggleRightNav() {
  isRightExpanded.value = !isRightExpanded.value
}

function handleClickOutside(event: MouseEvent) {
  const leftSidepanel = document.querySelector('.left-sidepanel')
  const rightSidepanel = document.querySelector('.right-sidepanel')
  const leftOpenbtn = document.querySelector('.left-openbtn')
  const rightOpenbtn = document.querySelector('.right-openbtn')

  if (
    leftSidepanel &&
    !leftSidepanel.contains(event.target as Node) &&
    !leftOpenbtn?.contains(event.target as Node)
  ) {
    isLeftExpanded.value = false
  }

  if (
    rightSidepanel &&
    !rightSidepanel.contains(event.target as Node) &&
    !rightOpenbtn?.contains(event.target as Node)
  ) {
    isRightExpanded.value = false
  }
}

function showSection(section: string) {
  activeSection.value = section
  isLeftExpanded.value = false
  isRightExpanded.value = false
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <!-- Left Sidepanel -->
  <div :class="['left-sidepanel', { 'sidepanel-expanded': isLeftExpanded }]">
    <a v-if="isLeftExpanded" href="#" @click.prevent="showSection('Text1')">Text1</a>
    <a v-if="isLeftExpanded" href="#" @click.prevent="showSection('Text2')">Text2</a>
    <a v-if="isLeftExpanded" href="#" @click.prevent="showSection('Text3')">Text3</a>
    <a v-if="isLeftExpanded" href="#" @click.prevent="showSection('Text4')">Text4</a>
  </div>

  <button class="left-openbtn" @click="toggleLeftNav">
    <span class="button-symbol">&#9776;</span>
    <span class="sidepane-text">Left Sidepane</span>
  </button>

  <!-- Right Sidepanel -->
  <div :class="['right-sidepanel', { 'right-sidepanel-expanded': isRightExpanded }]">
    <a v-if="isRightExpanded" href="#" @click.prevent="showSection('Text5')">Text5</a>
    <a v-if="isRightExpanded" href="#" @click.prevent="showSection('Text6')">Text6</a>
    <a v-if="isRightExpanded" href="#" @click.prevent="showSection('Text7')">Text7</a>
    <a v-if="isRightExpanded" href="#" @click.prevent="showSection('Text8')">Text8</a>
  </div>

  <button class="right-openbtn" @click="toggleRightNav">
    <span class="right-sidepane-text">Right Sidepane</span>
    <span class="button-symbol">&#9776;</span>
  </button>

  <h2>
    {{ activeSection ? activeSection.charAt(0).toUpperCase() + activeSection.slice(1) : 'Graph' }}
  </h2>

  <div v-if="activeSection === 'Text1'">
    <p>Text1 Content... About the project...</p>
  </div>
  <div v-if="activeSection === 'Text2'">
    <p>Text2 Content... About the ISO ...</p>
  </div>
  <div v-if="activeSection === 'Text3'">
    <p>Text3 Content...</p>
  </div>
  <div v-if="activeSection === 'Text4'">
    <p>Text4 Content...</p>
  </div>

  <div v-if="activeSection === 'Text5'">
    <p>Text5 Content...</p>
  </div>
  <div v-if="activeSection === 'Text6'">
    <p>Text6 Content...</p>
  </div>
  <div v-if="activeSection === 'Text7'">
    <p>Text7 Content...</p>
  </div>
  <div v-if="activeSection === 'Text8'">
    <p>Text8 Content...</p>
  </div>

  <p v-if="!activeSection">Content...</p>
</template>

<style scoped>
/* The left sidepanel menu */
.left-sidepanel {
  height: 100%;
  width: 0; /* Initial width */
  position: fixed;
  z-index: 1;
  top: 130px;
  left: 0;
  background-color: var(--color-nav-background);
  overflow-x: hidden;
  padding-top: 60px;
  transition: width 0.5s ease; /* Smooth transition */
}

/* The left sidepanel expanded state */
.sidepanel-expanded {
  width: 250px; /* Expanded width */
}

/* The left sidepanel links */
.left-sidepanel a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 20px;
  color: var(--color-nav-title);
  display: block;
  transition: color 0.3s;
}

/* When you mouse over the navigation links, change their color */
.left-sidepanel a:hover {
  color: #f1f1f1;
}

/* Style the button that is used to open the left sidepanel */
.left-openbtn {
  width: 50px; /* Initial width */
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  background-color: white; /* Background color before expansion */
  color: var(--color-nav-background); /* Icon color before expansion */
  padding: 10px 0;
  border: none;
  position: absolute;
  top: 74px;
  left: 0;
  text-align: center; /* Center the symbol */
  display: flex;
  align-items: center;
  transform: translateX(30px); /* Move button right by 30px */
  transition:
    transform 0.5s ease,
    background-color 0.5s ease,
    color 0.5s ease; /* Smooth transition for transform */
  z-index: 2; /* Ensure button is above sidepanel */
}

/* The button symbol */
.button-symbol {
  display: inline-block;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}

/* The button text */
.sidepane-text {
  display: inline-block;
  margin-left: 10px; /* Space between button and text */
  transition:
    opacity 0.8s ease,
    transform 0.5s ease;
  transform: translateX(0); /* Always in view */
  opacity: 0;
  visibility: hidden; /* Hide initially */
}

/* When the left sidepanel is expanded, adjust button and text */
.sidepanel-expanded + .left-openbtn {
  width: 250px; /* Expanded width */
  background-color: var(--color-nav-background); /* Background color when expanded */
  color: white; /* Icon color when expanded */
  text-align: left; /* Align text to the left */
  padding-left: 15px; /* Add padding to the left */
  transform: translateX(0); /* Reset the button position */
}

/* Ensure the background color transition aligns properly */
.sidepanel-expanded + .left-openbtn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--color-nav-background);
  z-index: -1; /* Behind the button content */
}

/* When expanded, the button text should slide in */
.sidepanel-expanded + .left-openbtn .sidepane-text {
  opacity: 1;
  visibility: visible; /* Make visible when expanded */
  transform: translateX(0); /* Ensure text is fully visible */
}

.left-openbtn:hover {
  cursor: pointer;
}

/* The right sidepanel menu */
.right-sidepanel {
  height: 100%;
  width: 0; /* Initial width */
  position: fixed;
  z-index: 1;
  top: 130px;
  right: 0; /* Position on the right */
  background-color: var(--color-nav-background);
  overflow-x: hidden;
  padding-top: 60px;
  transition: width 0.5s ease; /* Smooth transition */
}

/* The right sidepanel expanded state */
.right-sidepanel-expanded {
  width: 250px; /* Expanded width */
}

/* The right sidepanel links */
/* The right sidepanel links */
.right-sidepanel a {
  padding: 8px 32px 8px 40px; /* Adjust padding for right side */
  text-decoration: none;
  font-size: 20px;
  color: var(--color-nav-title);
  display: block;
  position: relative; /* Ensure pseudo-element is positioned correctly */
  overflow: hidden; /* Hide overflow for hover effect */
  padding-left: 150px;
}

/* Add a pseudo-element for hover effect */
.right-sidepanel a::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1; /* Ensure it is above text */
  transform: translateX(-100%); /* Initially hidden to the left */
  transition:
    transform 0.3s ease,
    background-color 0.3s ease; /* Smooth transition */
}

/* On hover, move the pseudo-element to cover the text */
.right-sidepanel a:hover::after {
  transform: translateX(0); /* Move to cover the text */
}

/* On hover, change text color */
.right-sidepanel a:hover {
  color: #f1f1f1;
}

/* Adjust padding to maintain alignment with the text movement */
.right-sidepanel a:hover::after {
  padding-left: 150px; /* Adjust this to align with the text */
}

/* Style the button that is used to open the right sidepanel */
.right-openbtn {
  width: 50px; /* Initial width */
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  background-color: white; /* Background color before expansion */
  color: var(--color-nav-background); /* Icon color before expansion */
  padding: 10px 0;
  border: none;
  position: absolute;
  top: 74px;
  right: 0;
  text-align: center; /* Center the symbol */
  display: flex;
  align-items: center;
  transform: translateX(-100px); /* Move button left by 30px */
  transition:
    transform 0.5s ease,
    background-color 0.5s ease,
    color 0.5s ease; /* Smooth transition for transform */
  z-index: 2; /* Ensure button is above sidepanel */
}

/* The button symbol */
.button-symbol {
  display: inline-block;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}

/* The button text */
.right-sidepane-text {
  display: inline-block;
  margin-right: 10px; /* Space between text and button */
  transition:
    opacity 0.8s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden; /* Hide initially */
}

/* When the right sidepanel is expanded, adjust button and text */
.right-sidepanel-expanded + .right-openbtn {
  width: 250px; /* Expanded width */
  background-color: var(--color-nav-background); /* Background color when expanded */
  color: white; /* Icon color when expanded */
  text-align: right; /* Align text to the right */
  transform: translateX(70px); /* Move button right by 70px */
  z-index: 2; /* Ensure button is above the sidepanel */
}

/* Ensure the background color transition aligns properly */
.right-sidepanel-expanded + .right-openbtn::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0; /* Align with the right edge */
  width: 100%;
  height: 100%;
  background-color: var(--color-nav-background); /* Background color to match button */
  z-index: -1; /* Ensure it is behind the button content */
  transform: translateX(-70px); /* Compensate for the button's move */
}

/* When expanded, the button text should slide in */
.right-sidepanel-expanded + .right-openbtn .right-sidepane-text {
  opacity: 1;
  visibility: visible; /* Make visible when expanded */
  transform: translateX(0); /* Ensure text is fully visible */
}

.right-openbtn:hover {
  cursor: pointer;
}
</style>
