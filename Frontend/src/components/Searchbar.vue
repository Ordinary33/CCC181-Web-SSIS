<script setup>
defineProps({
  query: String,
  filter: String,
  filters: {
    type: Array,
    default: () => ["All","ID","First Name","Last Name","Year","Gender","Program"]
  },
  sortBy: String,
  sortDesc: Boolean,
  sortOptions: {
    type: Array,
    default: () => []
  }
})
defineEmits(['update:query','update:filter','update:sortBy','update:sortDesc'])
</script>

<template>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <div class="flex flex-col lg:flex-row gap-4 lg:gap-8 items-center justify-between p-4 bg-white rounded-xl shadow-lg border border-gray-100">
      
      <label class="input input-bordered flex items-center gap-2 w-full lg:w-1/3 transition-all duration-300 focus-within:border-[#0F766E] focus-within:ring-1 focus-within:ring-[#0F766E] rounded-lg shadow-sm">
        
        <svg class="w-4 h-4 text-[#0F766E] opacity-70" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </g>
        </svg>

        <input 
          type="search" 
          class="grow placeholder-gray-400 focus:outline-none focus:ring-0 text-sm font-medium" 
          :value="query" 
          @input="$emit('update:query', $event.target.value)" 
          placeholder="Search records..."
        />
      </label>
      
      <div class="flex items-center gap-3 lg:gap-4 w-full lg:w-2/3 justify-end">
        
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-sm text-[#0F766E] border border-[#0F766E] bg-white hover:bg-[#CCFBF1] transition-colors duration-200">
            Search By: <span class="font-bold ml-1">{{ filter }}</span>
          </div>
          
          <div tabindex="0" class="dropdown-content card card-sm bg-white z-10 w-64 shadow-xl border border-gray-100">
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
            Sort By: <span class="font-bold ml-1">{{ sortBy }}</span>
          </div>
          
          <div tabindex="0" class="dropdown-content card card-sm bg-white z-10 w-64 shadow-xl border border-gray-100">
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
              
              <button 
                class="btn btn-sm mt-2 border-none text-white bg-[#0F766E] hover:bg-[#0d6e66]" 
                @click="$emit('update:sortDesc', !sortDesc)"
              >
                {{ sortDesc ? 'Descending (Z-A / 9-1)' : 'Ascending (A-Z / 1-9)' }}
              </button>
            </div>
          </div>
        </div>

        <button 
          class="btn btn-square btn-sm border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] transition-colors duration-200"
          @click="$emit('update:sortDesc', !sortDesc)"
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
  

  