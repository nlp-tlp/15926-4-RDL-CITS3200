<script setup lang="ts">
import { ref } from 'vue'

// interface NodeInfo {
//   label: 'Thing'
//   definition: 'Thing is anything'
//   id: 'http://data.15926.org/dm/Thing'
//   dep: 'null'
// }

// const nodeInfo: Ref<NodeInfo | null> = ref(null)

const props = defineProps({
  // nodeinfo: {
  //   type: Object as () => NodeInfo | null,
  //   default: null
  // },
  initialExpanded: {
    type: Boolean,
    default: false
  },
  nodeInfoDisplay: {
    type: Object,
    required: true
  }
})

const isRightExpanded = ref(props.initialExpanded)

function toggleRightNav(): void {
  isRightExpanded.value = !isRightExpanded.value
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
    <!-- <GraphVisualisation @open-side-panel="toggleRightNav" /> -->

    <button class="right-btn" @click="toggleRightNav" :class="{ 'expanded-btn': isRightExpanded }">
      &#9776;
    </button>

    <transition name="sidepanel">
      <div v-if="isRightExpanded" class="right-sidepanel">
        <p class="right-text">Node Information</p>

        <div class="rdf-info">
          <div v-for="(value, key) in rdfData" :key="key" class="rdf-field">
            <strong class="rdf-field-name">{{ key }}:</strong>
            <span class="rdf-field-value">
              <slot :name="key" :value="value">
                {{ value }}
              </slot>
            </span>
          </div>
        </div>
      </div>
    </transition>
  </div>
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
  flex-direction: column;
  align-items: left;
  padding-top: 0.25rem;
  height: calc(100vh - var(--navbar-height, 4.5rem));
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
  overflow: hidden; /* Ensure the side panel itself does not scroll */
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

.rdf-info {
  flex: 1; /* Allow rdf-info to take up remaining space */
  margin: 1rem;
  color: white;
  /* Allow scrolling within the rdf-info div but no scrollbars */
  overflow-y: auto;
  overflow-x: hidden;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.rdf-info::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.rdf-field {
  margin-bottom: 1rem;
}

.rdf-field-name {
  display: block;
  font-weight: bold;
}

.rdf-field-value {
  display: block;
  margin-left: 1rem;
  white-space: normal;
  word-wrap: break-word;
}
</style>
