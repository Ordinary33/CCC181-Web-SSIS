<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
<div class="min-h-screen bg-[#A2D5AB]">
  <header>
    <Navbar />
  </header>
 
  <RouterView />
</div>
</template>

<style scoped>
</style>
