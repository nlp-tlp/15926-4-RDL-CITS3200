<script setup lang="ts">
import { ref, watch } from 'vue'

import { search } from '../assets/apiFunctions'

const props = defineProps({
  /**
   * Determines if the side panel is initially expanded.
   */
  initialExpanded: {
    type: Boolean,
    default: false
  },
  /**
   * Flag to determine if the left side panel is expanded.
   */
  isLeftExpanded: {
    type: Boolean,
    required: true
  }
})

/**
 * Interface for search results.
 * @property `id` - The ID of the search result.
 * @property `label` - The label of the search result.
 * @property `dep` - The deprecation status of the search result.
 */
interface SearchResult {
  id?: string
  label?: string
  dep?: string | null
}

// Side panel state
const isLeftExpanded = ref(props.isLeftExpanded)
const labelsToggle = ref(true) // Control whether labels are displayed in the graph
const deprecatedToggle = ref(false) // Control whether deprecated nodes are displayed

// Search functionality
const searchTerm = ref('') // The search term entered by the user
const searchOption = ref('rdf') // The dropdown option selected by the user ('id' or 'rdf')
const results = ref<SearchResult[]>([]) // Store search results
const isSearching = ref(false) // Track API call state
const showResults = ref(false) // Control whether search results are displayed
const errorMessage = ref('') // Store error message from API
let debounceTimeout: number // Timeout for debouncing search

const emit = defineEmits([
  'toggleLabels',
  'toggleDeprecated',
  'nodeSelected',
  'toggleIsLeftExpanded'
])

watch(
  () => props.isLeftExpanded,
  (newVal) => {
    isLeftExpanded.value = newVal
  }
)

/**
 * Toggles the left side panel.
 */
function toggleLeftNav(): void {
  emit('toggleIsLeftExpanded')
}

/**
 * Debounce search function to prevent multiple API calls.
 * @param fn - The search function to be debounced.
 * @param delay - The delay in milliseconds.
 */
function debounceSearch(fn: () => void, delay: number = 450) {
  clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(fn, delay)
}

// Watch the search term and trigger the search function on changes
watch(searchTerm, (newSearchTerm) => {
  // If the length of the search term is less than 1, clear results and do not display
  if (newSearchTerm.length < 1) {
    results.value = [] // Clear results
    showResults.value = false // Hide search results
  } else {
    showResults.value = true // Show search results
    debounceSearch(() => performSearch(newSearchTerm)) // Perform search
  }
})

/**
 * Wrapper function to call the search API.
 * @param query - The search query.
 */
async function performSearch(query: string): Promise<void> {
  isSearching.value = true
  errorMessage.value = ''
  results.value = [] // Clear previous results

  const { results: searchResults, errorMessage: searchError } = await search(
    query,
    searchOption.value,
    deprecatedToggle.value
  )
  results.value = searchResults
  errorMessage.value = searchError

  isSearching.value = false
}

/**
 * Click event handler for search results.
 * @param result - The search result object.
 */
function clickResult(result: SearchResult): void {
  emit('nodeSelected', result.id)
  if (
    (searchOption.value === 'id' && result.id === searchTerm.value) ||
    (searchOption.value === 'rdf' && result.label === searchTerm.value)
  ) {
    // The currently clicked result matches the search term, hide the search results
    showResults.value = false
  } else {
    // Update the search term to the clicked result
    searchTerm.value = searchOption.value === 'id' ? result.id || '' : result.label || ''

    showResults.value = false // Hide search results after setting the search term

    // Delay hiding the results after setting the search term to avoid triggering the search again via watch
    setTimeout(() => {
      showResults.value = false
    }, 100)
  }
}

/**
 * Submit event handler for the search form.
 * @emits toggleLabels - Emits the toggleLabels event with the current labelsToggle value.
 * @emits toggleDeprecated - Emits the toggleDeprecated event with the current deprecatedToggle value.
 */
function handleSubmit() {
  emit('toggleLabels', labelsToggle.value)
  emit('toggleDeprecated', deprecatedToggle.value)
}
</script>

<script lang="ts">
/**
 * GraphSearchSidepane component represents the expandable side panel containing search functionality as well as options to toggle labels and deprecated nodes.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 * @param {boolean} isLeftExpanded - Flag to determine if the left side panel is expanded.
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
  <div>
    <button
      class="left-btn fixed top-20 left-2 bg-transparent cursor-pointer border-none text-2xl font-bold z-20 text-nav-background transition-colors duration-500 ease"
      @click="toggleLeftNav"
      :class="{ 'text-white': isLeftExpanded }"
    >
      &#9776;
    </button>

    <transition name="sidepanel">
      <div
        v-if="isLeftExpanded"
        class="left-sidebar fixed top-[var(--navbar-height,4.145rem)] left-0 sm:w-[250px] flex flex-col items-start pt-1 h-full bg-nav-background pb-10 transition-transform duration-500 ease overflow-hidden"
      >
        <p class="ml-auto text-white mt-5 mr-4 whitespace-nowrap">Graph Search</p>

        <div v-if="isLeftExpanded" class="overflow-hidden">
          <div class="flex flex-col m-4 mt-12">
            <div class="relative">
              <svg
                class="absolute left-2 top-[1.75rem] transform -translate-y-1/2 fill-current text-white transition-all duration-300"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="24"
                height="24"
              >
                <path
                  d="M23 21l-5.5-5.5a9.5 9.5 0 1 0-1.4 1.4L21 22.4a1 1 0 0 0 1.4-1.4zM10 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"
                />
              </svg>
              <input
                v-model="searchTerm"
                class="w-full p-4 pl-12 mb-2 max-w-[220px] border border-white bg-cyan-950 text-white rounded-lg text-base transition-all duration-300 placeholder-white"
                type="text"
                placeholder="Search..."
              />
            </div>

            <div class="relative">
              <select
                v-model="searchOption"
                class="w-full p-3 max-w-[220px] border border-white bg-cyan-950 mb-[30px] text-white rounded-lg text-base cursor-pointer transition-all duration-300 focus:outline-none focus:border-accent focus:bg-nav-background-dark appearance-none"
              >
                <option value="rdf">RDF Label</option>
                <option value="id">ID/URI</option>
              </select>
              <div class="absolute top-4 right-[-2px] flex items-center px-2 pointer-events-none">
                <svg
                  class="w-4 h-4 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  ></path>
                </svg>
              </div>
            </div>
          </div>

          <div
            v-if="showResults"
            class="max-h-[300px] overflow-y-auto bg-cyan-950 m-4 p-4 border border-white rounded-lg absolute top-[9rem] left-[-1rem] w-[calc(95%)] shadow-lg z-10 ml-[22px] scrollbar-none"
          >
            <div v-if="isSearching" class="text-center text-white">Searching...</div>
            <div v-if="errorMessage" class="text-center text-white">
              {{ errorMessage }}
            </div>
            <ul v-if="results.length > 0">
              <li
                v-for="(result, index) in results"
                :key="index"
                :class="[
                  'p-1 px-1 cursor-pointer break-words',
                  result.dep
                    ? 'bg-[#ce033c] text-white italic hover:bg-[#fd4277]'
                    : 'text-white bg-nav-background-dark hover:bg-[#55789a]'
                ]"
                @click="clickResult(result)"
              >
                <span v-if="searchOption === 'id'">{{ result.id }}</span>
                <span v-else>{{ result.label }}</span>
              </li>
            </ul>
          </div>

          <div v-if="isLeftExpanded" class="m-4 mb-5">
            <label class="flex items-center text-white mb-4 mt-7 whitespace-nowrap">
              <input type="checkbox" class="mr-2" v-model="deprecatedToggle" />
              Show Deprecated
            </label>
            <label class="flex items-center text-white mb-6 whitespace-nowrap">
              <input type="checkbox" class="mr-2" v-model="labelsToggle" />
              View Labels in Graph
            </label>
          </div>
          <button
            class="w-[80%] mx-auto p-3 bg-cyan-950 text-white ml-5 border border-white rounded-lg text-sm cursor-pointer text-center transition-all duration-300"
            @click="handleSubmit"
          >
            Apply filters
          </button>
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
  transform: translateX(-100%);
  opacity: 0;
}

.sidepanel-enter-to,
.sidepanel-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>
