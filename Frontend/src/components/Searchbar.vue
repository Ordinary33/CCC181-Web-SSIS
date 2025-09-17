<template>
    <div class="flex justify-center items-center mt-10 space-x-4">
      <!-- Search input -->
      <label class="input">
        <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </g>
        </svg>
        <input type="search" :value="query" @input="$emit('update:query', $event.target.value)" placeholder="Search"/>
      </label>
  
      <!-- Search filter -->
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn m-1">Search By</div>
        <div tabindex="0" class="dropdown-content card card-sm bg-base-100 z-10 w-64 shadow-md">
          <div class="card-body flex flex-col gap-2">
            <label v-for="f in filters" :key="f">
            <input
                type="radio"
                :value="f"
                name="filter"
                :checked="filter === f"
                @change="$emit('update:filter', f)"
            />
            {{ f }}
            </label>
          </div>
        </div>
      </div>
  
      <!-- Sort filter -->
      <div class="dropdown">
        <div tabindex="0" class="btn m-1">Sort By</div>
        <div tabindex="0" class="dropdown-content card card-sm bg-base-100 w-64 shadow-md">
          <div class="card-body flex flex-col gap-2">
            <label v-for="option in sortOptions" :key="option">
              <input type="radio" :value="option" name="sort" :checked="sortBy===option" @change="$emit('update:sortBy', option)" />
              {{ option }}
            </label>
            <button class="btn btn-sm mt-2" @click="$emit('update:sortDesc', !sortDesc)">
              {{ sortDesc ? 'Descending' : 'Ascending' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
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
  