<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();

onMounted(async () => {
  await authStore.init();
});
</script>

<template>
  <div>
    <router-view />
  </div>
</template>