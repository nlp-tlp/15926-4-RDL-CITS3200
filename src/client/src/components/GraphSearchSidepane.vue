<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    initialExpanded?: boolean
  }>(),
  {
    initialExpanded: false
  }
)

const isLeftExpanded = ref(props.initialExpanded)

function toggleLeftNav(): void {
  isLeftExpanded.value = !isLeftExpanded.value
}
</script>

<script lang="ts">
/**
 * GraphSearchSidepane component represents the expandable side panel containing search functionality.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 *
 * @example
 * <GraphSearchSidepane :initialExpanded="true" />
 * <GraphSearchSidepane initialExpanded />
 * <GraphSearchSidepane />
 */
export default {
  name: 'GraphSearchSidepane'
}
</script>

<template>
  <button class="left-btn" @click="toggleLeftNav" :class="{ 'expanded-btn': isLeftExpanded }">
    &#9776;
  </button>

  <transition name="sidepanel">
    <div v-if="isLeftExpanded" class="left-sidepanel">
      <p class="left-text">Left Sidepanel</p>
    </div>
  </transition>
</template>

<style scoped>
.left-btn {
  position: fixed;
  top: var(--navbar-height, 5rem);
  left: 0.5rem;
  background-color: transparent;
  cursor: pointer;
  border: none;
  font-size: 22px;
  font-weight: bold;
  z-index: 2; /* Ensure the button is always on top */
  color: var(--color-nav-background);
  transition: color 0.5s ease;
}

.expanded-btn {
  color: white;
}

.left-sidepanel {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: 100%;
  width: 250px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  left: 0;
  background-color: var(--color-nav-background);
  transition:
    transform 0.5s ease,
    background-color 0.5s ease;
  transform: translateX(0);
}

.left-text {
  margin: 0.75rem 1rem 0 auto;
  color: white;
  white-space: nowrap;
}

.sidepanel-enter-active,
.sidepanel-leave-active {
  transition: all 0.5s ease;
}

.sidepanel-enter-from,
.sidepanel-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
</style>
