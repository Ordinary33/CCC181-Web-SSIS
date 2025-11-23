<script setup>
import { onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import { useProgramsStore } from '@/stores/programs'
import { useCollegesStore } from '@/stores/colleges'

import StudentIcon from '@/components/icons/student.svg'
import ProgramIcon from '@/components/icons/program.svg'
import CollegeIcon from '@/components/icons/college.svg'
import Footer from '@/components/Footer.vue'

const studentsStore = useStudentsStore()
const programsStore = useProgramsStore()
const collegesStore = useCollegesStore()

onMounted(async () => {
  await Promise.all([
    studentsStore.fetchStudents(),
    programsStore.fetchPrograms(),
    collegesStore.fetchColleges()
  ])
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 min-h-[80vh] flex flex-col justify-center py-8">
    
    <div class="bg-gradient-to-r from-[#0F766E] to-[#0d9488] rounded-2xl p-8 md:p-12 text-white shadow-xl mb-10 relative overflow-hidden">
      <div class="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
      <div class="relative z-10">
        <h1 class="text-3xl md:text-4xl font-bold mb-4">Welcome Back, Admin!</h1>
        <p class="text-teal-100 text-lg max-w-2xl">
          Here is an overview of the university database. You can manage students, update academic programs, and organize college departments from this dashboard.
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      
      <RouterLink to="/students" class="group">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 relative overflow-hidden">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-500 text-sm font-bold uppercase tracking-wider">Total Students</p>
              <h2 class="text-4xl font-bold text-[#0F766E] mt-2">{{ studentsStore.students.length }}</h2>
            </div>
            <div class="p-3 bg-[#CCFBF1] rounded-lg text-[#0F766E]">
              <img :src="StudentIcon" alt="Student" class="w-8 h-8">
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-gray-400 group-hover:text-[#0F766E] transition-colors">
            <span>View all students</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>
          </div>
        </div>
      </RouterLink>

      <RouterLink to="/programs" class="group">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 relative overflow-hidden">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-500 text-sm font-bold uppercase tracking-wider">Academic Programs</p>
              <h2 class="text-4xl font-bold text-[#0F766E] mt-2">{{ programsStore.programs.length }}</h2>
            </div>
            <div class="p-3 bg-[#CCFBF1] rounded-lg text-[#0F766E]">
              <img :src="ProgramIcon" alt="Program" class="w-8 h-8">
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-gray-400 group-hover:text-[#0F766E] transition-colors">
            <span>Manage programs</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>
          </div>
        </div>
      </RouterLink>

      <RouterLink to="/colleges" class="group">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 relative overflow-hidden">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-500 text-sm font-bold uppercase tracking-wider">Colleges</p>
              <h2 class="text-4xl font-bold text-[#0F766E] mt-2">{{ collegesStore.colleges.length }}</h2>
            </div>
            <div class="p-3 bg-[#CCFBF1] rounded-lg text-[#0F766E]">
              <img :src="CollegeIcon" alt="College" class="w-8 h-8">
            </div>
          </div>
          <div class="mt-4 flex items-center text-sm text-gray-400 group-hover:text-[#0F766E] transition-colors">
            <span>View departments</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>
          </div>
        </div>
      </RouterLink>

    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div class="bg-[#F0FDFA] border border-[#CCFBF1] p-6 rounded-xl">
        <h3 class="font-bold text-[#0F766E] mb-2">Getting Started?</h3>
        <p class="text-sm text-gray-600">To add a new student, navigate to the Students page or use the floating action button (+) in the bottom right corner.</p>
      </div>
      <div class="bg-[#F0FDFA] border border-[#CCFBF1] p-6 rounded-xl">
        <h3 class="font-bold text-[#0F766E] mb-2">Search & Filter</h3>
        <p class="text-sm text-gray-600">
            You can find records quickly by typing an ID, Name, or Code into the search bar on any management page.
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <div class="bg-white border border-gray-100 p-6 rounded-xl shadow-sm">
        <h3 class="font-bold text-gray-700 mb-6 text-sm uppercase flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          System Health
        </h3>
        
        <div class="space-y-5">
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-xs font-bold text-gray-500">Database Storage</span>
              <span class="text-xs font-bold text-[#0F766E]">45%</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2">
              <div class="bg-[#0F766E] h-2 rounded-full transition-all duration-1000" style="width: 45%"></div>
            </div>
          </div>
          
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-xs font-bold text-gray-500">Server Load</span>
              <span class="text-xs font-bold text-emerald-500">Optimal</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2">
              <div class="bg-emerald-400 h-2 rounded-full transition-all duration-1000" style="width: 25%"></div>
            </div>
          </div>

          <div>
            <div class="flex justify-between mb-1">
              <span class="text-xs font-bold text-gray-500">API Status</span>
              <span class="text-xs font-bold text-emerald-500">Online</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2">
              <div class="bg-emerald-400 h-2 rounded-full transition-all duration-1000" style="width: 98%"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-gray-100 rounded-xl shadow-sm lg:col-span-2 overflow-hidden flex flex-col">
        <div class="p-6 border-b border-gray-50">
          <h3 class="font-bold text-gray-700 text-sm uppercase">Recent System Logs</h3>
        </div>
        <div class="flex-grow overflow-y-auto">
          <table class="w-full text-sm text-left">
            <tbody class="divide-y divide-gray-50">
              <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 font-medium text-gray-700">Database Backup</td>
                <td class="px-6 py-4 text-gray-500">Automated System</td>
                <td class="px-6 py-4 text-right text-gray-400 text-xs">2 mins ago</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 font-medium text-gray-700">User Login</td>
                <td class="px-6 py-4 text-gray-500">Admin</td>
                <td class="px-6 py-4 text-right text-gray-400 text-xs">15 mins ago</td>
              </tr>
              <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 font-medium text-gray-700">System Update</td>
                <td class="px-6 py-4 text-gray-500">v2.4.0 Patch</td>
                <td class="px-6 py-4 text-right text-gray-400 text-xs">1 day ago</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="p-4 bg-gray-50 border-t border-gray-100 text-center">
          <button class="text-xs font-bold text-[#0F766E] hover:underline">View All Logs</button>
        </div>
      </div>

    </div>

  </div>
  <Footer />
</template>