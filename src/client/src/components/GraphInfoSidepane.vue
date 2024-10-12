<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const props = defineProps({
  /**
   * Determines if the side panel is initially expanded.
   */
  initialExpanded: {
    type: Boolean,
    default: false
  },
  /**
   * The RDF data to display in the side panel.
   */
  nodeInfoDisplay: {
    type: Object,
    required: true
  },
  /**
   * Flag to determine if the right side panel is expanded.
   */
  isRightExpanded: {
    type: Boolean,
    required: true
  }
})

// State variables for side panel
const isRightExpanded = ref(props.initialExpanded)
const currentLabel = ref('')
const rdfData = ref(props.nodeInfoDisplay)

watch(
  () => props.isRightExpanded,
  (newVal) => {
    console.log('isRightExpanded changed:', newVal)
    isRightExpanded.value = newVal
  }
)

/**
 * Toggles the right side panel.
 * If a label is provided, it toggles based on the label.
 * Otherwise, it toggles based on the button click.
 * @param {string} label - The label to toggle the side panel for.
 */
function toggleRightNav(label?: string): void {
  if (label) {
    if (currentLabel.value === label) {
      isRightExpanded.value = !isRightExpanded.value
    } else {
      currentLabel.value = label
      isRightExpanded.value = true
    }
  } else {
    isRightExpanded.value = !isRightExpanded.value
  }
}

// Expose toggleRightNav function to parent component - GraphView.vue
defineExpose({
  toggleRightNav
})

// Watch for changes in the nodeInfoDisplay prop and update RDF data
watch(
  () => props.nodeInfoDisplay,
  (newValue) => {
    rdfData.value = newValue
  }
)

/**
 * Handles label click to update RDF data or toggle side panel.
 * @param {string} label - The label of the RDF data.
 * @param {object} newData - The new RDF data to display.
 */
function handleLabelClick(label: string, newData: object): void {
  if (currentLabel.value === label) {
    toggleRightNav(label)
  } else {
    currentLabel.value = label
    rdfData.value = newData
    isRightExpanded.value = true
  }
}

// Wrapper function for button click to bypass event type error on parameter
function handleButtonClick(event: MouseEvent): void {
  toggleRightNav()
}

// Computed property to filter rdfData
const filteredRdfData = computed(() => {
  return Object.entries(rdfData.value).filter(([key, value]) => value.trim() !== '')
})
</script>

<script lang="ts">
/**
 * GraphInfoSidepane component represents the expandable side panel containing RDF data for the selected node.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 * @param {object} nodeInfoDisplay - The RDF data to display in the side panel.
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
      @click="handleButtonClick"
      :class="{ 'text-white': isRightExpanded }"
    >
      &#9776;
    </button>

    <transition name="sidepanel">
      <div
        v-if="isRightExpanded"
        class="right-sidebar fixed top-[var(--navbar-height,4.145rem)] right-0 w-[250px] lg:w-[300px] h-full bg-nav-background z-10 flex flex-col pt-1 pb-10 transform transition-transform duration-500 ease-in-out"
      >
        <p class="ml-4 mt-3 text-white whitespace-normal">Node Information</p>

        <div class="flex-1 m-4 lg:pr-2 text-white overflow-y-auto scrollbar-none">
          <div v-if="filteredRdfData.length === 0" class="mb-4">
            <p class="ml-4 text-white">Click on a node's label to display the information</p>
          </div>
          <div v-else v-for="([key, value], index) in filteredRdfData" :key="index" class="mb-4">
            <strong class="block font-bold" @click="handleLabelClick(key, value)"
              >{{ key.charAt(0).toUpperCase() + key.slice(1) }}:</strong
            >
            <span class="block ml-4 break-words whitespace-pre-line break-all">
              <slot :name="key" :value="value">{{ value }}</slot>
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

sidepanel-enter-to,
.sidepanel-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>
