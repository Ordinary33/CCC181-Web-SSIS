<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'

const props = defineProps({
  query: String,
  filter: String,
  filters: {
    type: Array,
    default: () => ["All","ID","First Name","Last Name"]
  },
  sortBy: String,
  sortDesc: Boolean,
  sortOptions: {
    type: Array,
    default: () => []
  },
  selectedProgram: String,
  selectedYear: String,
  selectedGender: String,
  selectedCollege: String,
  programOptions: {
    type: Array,
    default: () => []
  },
  collegeOptions: {
    type: Array,
    default: () => []
  },
  showFilters: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:query', 
  'update:filter', 
  'update:sortBy', 
  'update:sortDesc',
  'update:selectedProgram',
  'update:selectedYear',
  'update:selectedGender',
  'update:selectedCollege'
])

const localQuery = ref(props.query)
let timer = null

const onInput = () => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    emit('update:query', localQuery.value)
  }, 500)
}

watch(() => props.query, (newVal) => {
  if (newVal !== localQuery.value) {
    localQuery.value = newVal
  }
})

const isFilterActive = computed(() => {
  return props.selectedProgram || props.selectedYear || props.selectedGender || props.selectedCollege
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
})
</script>

<template>
  <div class="max-w-7xl mx-auto mt-8 px-4">
    <div class="flex flex-col xl:flex-row gap-4 items-center justify-between p-4 bg-white rounded-xl shadow-lg border border-gray-100">
      
      <label class="input input-bordered flex items-center gap-2 w-full xl:w-1/3 transition-all duration-300 focus-within:border-[#0F766E] focus-within:ring-1 focus-within:ring-[#0F766E] rounded-lg shadow-sm">
        <svg class="w-4 h-4 text-[#0F766E] opacity-70" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </g>
        </svg>
        <input 
          type="search" 
          class="grow placeholder-gray-400 focus:outline-none focus:ring-0 text-sm font-medium" 
          v-model="localQuery"
          @input="onInput" 
          placeholder="Search records..."
        />
      </label>
      
      <div class="flex flex-wrap items-center gap-2 w-full xl:w-2/3 justify-end">
        
        <div class="dropdown dropdown-end" v-if="showFilters">
          <div 
            tabindex="0" 
            role="button" 
            class="btn btn-sm border border-[#0F766E] transition-colors duration-200"
            :class="isFilterActive ? 'bg-[#0F766E] text-white hover:bg-[#0d6e66]' : 'bg-white text-[#0F766E] hover:bg-[#CCFBF1]'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
            </svg>
            Filters
            <span v-if="isFilterActive" class="w-2 h-2 rounded-full bg-white ml-1"></span>
          </div>
          
          <div tabindex="0" class="dropdown-content card card-compact bg-white z-20 w-72 shadow-xl border border-gray-100 mt-2">
            <div class="card-body p-4 space-y-3">
              <h3 class="font-bold text-gray-700 text-sm border-b pb-2">Filter Records</h3>

              <div class="form-control w-full">
                <label class="label pt-0"><span class="label-text text-xs font-bold text-gray-500">College</span></label>
                <select 
                  class="select select-sm select-bordered w-full focus:border-[#0F766E] focus:outline-none"
                  :value="selectedCollege"
                  @change="$emit('update:selectedCollege', $event.target.value)"
                >
                  <option value="">All Colleges</option>
                  <option v-for="col in collegeOptions" :key="col.college_code" :value="col.college_code">
                    {{ col.college_code }} - {{ col.college_name }}
                  </option>
                </select>
              </div>
              
              <div class="form-control w-full">
                <label class="label pt-0"><span class="label-text text-xs font-bold text-gray-500">Program</span></label>
                <select 
                  class="select select-sm select-bordered w-full focus:border-[#0F766E] focus:outline-none"
                  :value="selectedProgram"
                  @change="$emit('update:selectedProgram', $event.target.value)"
                >
                  <option value="">All Programs</option>
                  <option v-for="prog in programOptions" :key="prog.program_code" :value="prog.program_code">
                    {{ prog.program_code }}
                  </option>
                </select>
              </div>

              <div class="form-control w-full">
                <label class="label pt-0"><span class="label-text text-xs font-bold text-gray-500">Year Level</span></label>
                <select 
                  class="select select-sm select-bordered w-full focus:border-[#0F766E] focus:outline-none"
                  :value="selectedYear"
                  @change="$emit('update:selectedYear', $event.target.value)"
                >
                  <option value="">All Years</option>
                  <option value="1">1st Year</option>
                  <option value="2">2nd Year</option>
                  <option value="3">3rd Year</option>
                  <option value="4">4th Year</option>
                </select>
              </div>

              <div class="form-control w-full">
                <label class="label pt-0"><span class="label-text text-xs font-bold text-gray-500">Gender</span></label>
                <select 
                  class="select select-sm select-bordered w-full focus:border-[#0F766E] focus:outline-none"
                  :value="selectedGender"
                  @change="$emit('update:selectedGender', $event.target.value)"
                >
                  <option value="">All Genders</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div v-if="isFilterActive" class="pt-2">
                <button 
                  @click="$emit('update:selectedProgram', ''); $emit('update:selectedYear', ''); $emit('update:selectedGender', ''); $emit('update:selectedCollege', '')"
                  class="btn btn-xs btn-ghost text-red-500 w-full hover:bg-red-50"
                >
                  Clear Filters
                </button>
              </div>

            </div>
          </div>
        </div>

        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-sm text-[#0F766E] border border-[#0F766E] bg-white hover:bg-[#CCFBF1] transition-colors duration-200">
            Search In: <span class="font-bold ml-1">{{ filter }}</span>
          </div>
          <div tabindex="0" class="dropdown-content card card-sm bg-white z-10 w-48 shadow-xl border border-gray-100">
            <div class="card-body flex flex-col gap-2 p-4">
              <label v-for="f in filters" :key="f" class="flex items-center space-x-3 text-sm text-gray-700 hover:bg-gray-50 p-2 rounded-lg transition-colors cursor-pointer">
                <input
                  type="radio"
                  :value="f"
                  name="filter"
                  :checked="filter === f"
                  @change="$emit('update:filter', f)"
                  class="radio radio-xs checked:bg-[#0F766E]"
                />
                <span>{{ f }}</span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="dropdown dropdown-end">
          <div tabindex="0" class="btn btn-sm text-[#0F766E] border border-[#0F766E] bg-white hover:bg-[#CCFBF1] transition-colors duration-200">
            Sort: <span class="font-bold ml-1">{{ sortBy }}</span>
          </div>
          <div tabindex="0" class="dropdown-content card card-sm bg-white z-10 w-48 shadow-xl border border-gray-100">
            <div class="card-body flex flex-col gap-2 p-4">
              <label v-for="option in sortOptions" :key="option" class="flex items-center space-x-3 text-sm text-gray-700 hover:bg-gray-50 p-2 rounded-lg transition-colors cursor-pointer">
                <input 
                  type="radio" 
                  :value="option" 
                  name="sort" 
                  :checked="sortBy===option" 
                  @change="$emit('update:sortBy', option)" 
                  class="radio radio-xs checked:bg-[#0F766E]"
                />
                <span>{{ option }}</span>
              </label>
            </div>
          </div>
        </div>

        <button 
          class="btn btn-square btn-sm border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] transition-colors duration-200"
          @click="$emit('update:sortDesc', !sortDesc)"
          :title="sortDesc ? 'Descending' : 'Ascending'"
        >
          <svg v-if="!sortDesc" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h9.75M18.75 16.5L16.5 19.5m0 0l-2.25-3m2.25 3V2.25" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h9.75M18.75 7.5L16.5 4.5m0 0L14.25 7.5m2.25-3v14.25" />
          </svg>
        </button>
      </div>
      
    </div>
  </div>
</template>