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

const isRightExpanded = ref(props.initialExpanded)

function toggleRightNav(): void {
  isRightExpanded.value = !isRightExpanded.value
}
</script>

<script lang="ts">
/**
 * GraphInfoSidepane component represents the expandable side panel containing information functionality.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 *
 * @example
 * <GraphInfoSidepane :initialExpanded="true" />
 * <GraphInfoSidepane initialExpanded />
 * <GraphInfoSidepane />
 */
export default {
  name: 'GraphInfoSidepane'
}
</script>

<template>
  <button class="right-btn" @click="toggleRightNav" :class="{ 'expanded-btn': isRightExpanded }">
    &#9776;
  </button>

  <transition name="sidepanel">
    <div v-if="isRightExpanded" class="right-sidepanel">
      <p class="right-text">Right Sidepanel</p>
    </div>
  </transition>
</template>

<style scoped>
.right-btn {
  position: fixed;
  top: 5rem;
  right: 0.5rem;
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

.right-sidepanel {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: 100%;
  width: 250px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  right: 0;
  background-color: var(--color-nav-background);
  transition:
    transform 0.5s ease,
    background-color 0.5s ease;
  transform: translateX(0);
}

.right-text {
  margin: 0.75rem 0 0 1rem;
  color: white;
  white-space: nowrap;
}

.sidepanel-enter-active,
.sidepanel-leave-active {
  transition: all 0.5s ease;
}

.sidepanel-enter-from,
.sidepanel-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
