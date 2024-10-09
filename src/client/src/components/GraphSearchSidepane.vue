<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    initialExpanded?: boolean
    isExpandLeftEd: boolean
  }>(),
  {
    initialExpanded: false
  }
)

interface SearchResult {
  id?: string
  label?: string
  dep?: string | null // If you need the 'dep' property as well
}

// Reactive properties
const emit = defineEmits(['toggleLabels', 'toggleDeprecated', 'toggleIsExpandLeftEd']) // Defining emit events and leftsidepanel expand
const isExpandLeftEd = computed(() => props.isExpandLeftEd)
const searchTerm = ref('') // The search term entered by the user
const searchOption = ref('id') // The dropdown option selected by the user
const results = ref<SearchResult[]>([]) // Store search results
const isSearching = ref(false) // Track API call state
const showResults = ref(false) // Control whether search results are displayed
const errorMessage = ref('')
const showLabels = ref(true) // Control whether labels are displayed in the graph
const showDeprecated = ref(false) // Control whether deprecated nodes are displayed

const API_URL = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'

// Function to toggle the left nav
function toggleLeftNav(): void {
  emit('toggleIsExpandLeftEd')
}

// Function to debounce the search query -- ONLY QUERY AFTER USER STOPS TYPING
let debounceTimeout: number
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
    debounceSearch(() => search(newSearchTerm)) // Perform search
  }
})

// API search function
async function search(query: string): Promise<void> {
  isSearching.value = true
  errorMessage.value = ''
  results.value = [] // Clear previous results

  try {
    const endpoint = searchOption.value === 'id' ? '/search/id/' : '/search/label/'
    const response = await fetch(`${API_URL}${endpoint}${encodeURIComponent(query)}?limit=25`)
    const data = await response.json()

    if (data.results && data.results.length > 0) {
      results.value = data.results.map((result: any) => ({
        id: result.id,
        label: result.label,
        dep: result.dep
      }))
    } else {
      errorMessage.value = 'No results found.'
    }
  } catch (error) {
    console.error('Error fetching search results:', error)
    errorMessage.value = 'Failed to fetch search results. Please try again later.'
  } finally {
    isSearching.value = false
  }
}

// Handle result click
function clickResult(result: SearchResult): void {
  if (
    (searchOption.value === 'id' && result.id === searchTerm.value) ||
    (searchOption.value === 'rdf' && result.label === searchTerm.value)
  ) {
    // The currently clicked result matches the search term, hide the search results
    showResults.value = false
  } else {
    // Update the search term to the clicked result
    searchTerm.value = searchOption.value === 'id' ? result.id || '' : result.label || ''

    // Delay hiding the results after setting the search term to avoid triggering the search again via watch
    setTimeout(() => {
      showResults.value = false
    }, 100)
  }
}

// Triggers "toggleLabels" event and "toggleDeprecated" event when "Submit" is clicked
function handleSubmit() {
  emit('toggleLabels', showLabels.value)
  emit('toggleDeprecated', showDeprecated.value)
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
  <div>
    <button
      class="left-btn fixed top-20 left-2 bg-transparent cursor-pointer border-none text-2xl font-bold z-20 text-nav-background transition-colors duration-500 ease"
      @click="toggleLeftNav"
      :class="{ 'text-white': isExpandLeftEd }"
    >
      &#9776;
    </button>

    <transition name="sidepanel">
      <div
        v-if="isExpandLeftEd"
        class="left-sidebar fixed top-[var(--navbar-height,4.145rem)] left-0 sm:w-[250px] flex flex-col items-start pt-1 h-[calc(100vh-4.5rem)] bg-nav-background transition-transform duration-500 ease overflow-hidden"
      >
        <p class="ml-auto text-white mt-3 mr-4 whitespace-nowrap">Graph Search</p>

        <div v-if="isExpandLeftEd" class="overflow-hidden">
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
                class="w-full p-4 pl-12 mb-2 max-w-[220px] border border-white bg-nav-background text-white rounded-lg text-base transition-all duration-300 placeholder-white"
                type="text"
                placeholder="Search..."
              />
            </div>

            <div class="relative">
              <select
                v-model="searchOption"
                class="w-full p-3 max-w-[220px] border border-white bg-nav-background mb-[30px] text-white rounded-lg text-base cursor-pointer transition-all duration-300 focus:outline-none focus:border-accent focus:bg-nav-background-dark appearance-none"
              >
                <option value="id">ID/URI</option>
                <option value="rdf">RDF Label</option>
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
            class="max-h-[300px] overflow-y-auto bg-nav-background m-4 p-4 border border-white rounded-lg absolute top-[8.5rem] left-[-1rem] w-[calc(95%)] shadow-lg z-10 ml-[22px] scrollbar-none"
          >
            <div v-if="isSearching" class="text-center text-white">Searching...</div>
            <div v-if="errorMessage" class="text-center text-white">
              {{ errorMessage }}
            </div>
            <ul v-if="results.length > 0">
              <li
                v-for="(result, index) in results"
                :key="index"
                class="p-1 px-1 text-white cursor-pointer hover:bg-nav-background-dark break-words"
                @click="clickResult(result)"
              >
                <span v-if="searchOption === 'id'">{{ result.id }}</span>
                <span v-else>{{ result.label }}</span>
              </li>
            </ul>
          </div>

          <div v-if="isExpandLeftEd" class="m-4 mb-5">
            <label class="flex items-center text-white mb-[30px] mt-7 whitespace-nowrap">
              <input type="checkbox" class="mr-2" v-model="showDeprecated" />
              Show Deprecated
            </label>
            <label class="flex items-center text-white mb-2 whitespace-nowrap">
              <input type="checkbox" class="mr-2" v-model="showLabels" />
              View Labels in Graph
            </label>
            <!-- Comment 'Levels Above' and 'Levels Below' part -->
            <!--
            <div v-if="isExpandLeftEd" class="mt-12 flex justify-between">
              <div class="flex flex-col w-[45%]">
                <label class="text-white mb-2 text-sm font-medium whitespace-nowrap"
                  >Levels Above:</label
                >
                <input
                  type="number"
                  min="0"
                  max="6"
                  class="small-input p-2 bg-white text-nav-background border border-white rounded-lg text-sm shadow-sm transition-all duration-300 appearance-auto"
                  value="0"
                />
              </div>
              <div v-if="isExpandLeftEd" class="flex flex-col w-[45%]">
                <label class="text-white mb-2 text-sm font-medium whitespace-nowrap"
                  >Levels Below:</label
                >
                <input
                  type="number"
                  min="0"
                  max="6"
                  class="small-input p-2 bg-white text-nav-background border border-white rounded-lg text-sm shadow-sm transition-all duration-300 appearance-auto"
                  value="0"
                />
              </div>
            </div>
            -->
          </div>
          <button
            class="w-[80%] mx-auto p-3 bg-nav-background text-white ml-5 border-2 border-white rounded-lg text-sm font-extrabold cursor-pointer mt-5 text-center transition-all duration-300"
            @click="handleSubmit"
          >
            Submit
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
