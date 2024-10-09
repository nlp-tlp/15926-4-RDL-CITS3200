<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps({
  initialExpanded: {
    type: Boolean,
    default: false
  },
  nodeInfoDisplay: {
    type: Object,
    required: true
  },
  isExpandRightEd: {
    type: Boolean
  }
})

interface Emit {
  (e: 'toggleIsExpandRightEd'): void
}

const emit = defineEmits<Emit>()

const isExpandRightEd = computed(() => props.isExpandRightEd)

const isRightExpanded = ref(props.initialExpanded)

function toggleRightNav(): void {
  if (!isRightExpanded.value) {
    isRightExpanded.value = !isRightExpanded.value
  }
}

function toggleRightNavButton(): void {
  emit('toggleIsExpandRightEd')
  return
}

defineExpose({
  toggleRightNav
})

// Create a reactive object to hold the RDF data
const rdfData = ref(props.nodeInfoDisplay)
</script>

<script lang="ts">
/**
 * GraphInfoSidepane component represents the expandable side panel containing RDF information functionality.
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
  <div>
    <button
      class="right-btn fixed top-[5rem] right-2 bg-transparent cursor-pointer border-none text-[22px] font-bold z-20 text-nav-background transition-colors duration-300 ease-in-out"
      @click="toggleRightNavButton"
      :class="{ 'text-white': isExpandRightEd }"
    >
      &#9776;
    </button>

    <transition name="sidepanel">
      <div
        v-if="isExpandRightEd"
        class="right-sidebar fixed top-[var(--navbar-height,4.145rem)] right-0 w-[250px] h-[calc(100vh-var(--navbar-height,4.5rem))] bg-nav-background z-10 flex flex-col pt-1 transform transition-transform duration-500 ease-in-out"
      >
        <p class="ml-4 mt-3 text-white whitespace-nowrap">Node Information</p>

        <div class="flex-1 m-4 text-white overflow-y-auto scrollbar-none">
          <div v-for="(value, key) in rdfData" :key="key" class="mb-4">
            <strong class="block font-bold">{{ key }}:</strong>
            <span class="block ml-4 break-words">
              {{ value }}
            </span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.scrollbar-none::-webkit-scrollbar {
  display: none;
}

.sidepanel-enter-active,
.sidepanel-leave-active {
  transition:
    transform 0.5s ease,
    opacity 0.5s ease;
}

.sidepanel-enter-from,
.sidepanel-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.sidepanel-enter-to,
.sidepanel-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>
