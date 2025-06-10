<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useThemeStore } from './stores/theme';

const authStore = useAuthStore();
const themeStore = useThemeStore();

onMounted(async () => {
  themeStore.initTheme();
  await authStore.init();
});
</script>

<template>
  <div :class="{ 'dark': themeStore.isDark }">
    <router-view />
  </div>
</template>