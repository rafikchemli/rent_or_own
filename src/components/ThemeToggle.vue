<template>
  <button
    class="theme-toggle"
    :aria-label="`Switch to ${isDark ? 'light' : 'dark'} mode`"
    @click="toggle"
  >
    <!-- Sun icon (shown when dark, click to go light) -->
    <svg v-if="isDark" width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="3.5" stroke="currentColor" stroke-width="1.5"/>
      <path d="M9 2V3.5M9 14.5V16M16 9H14.5M3.5 9H2M13.95 4.05L12.89 5.11M5.11 12.89L4.05 13.95M13.95 13.95L12.89 12.89M5.11 5.11L4.05 4.05" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    <!-- Moon icon (shown when light, click to go dark) -->
    <svg v-else width="18" height="18" viewBox="0 0 18 18" fill="none">
      <path d="M15.5 10.4a6.5 6.5 0 01-7.9-7.9A6.5 6.5 0 1015.5 10.4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const explicit = ref(null) // null = no user choice yet, follows system
const systemDark = ref(false)

const isDark = computed(() =>
  explicit.value !== null ? explicit.value === 'dark' : systemDark.value
)

function applyTheme() {
  const el = document.documentElement
  if (isDark.value) {
    el.setAttribute('data-theme', 'dark')
  } else {
    el.setAttribute('data-theme', 'light')
  }
}

function toggle() {
  explicit.value = isDark.value ? 'light' : 'dark'
  applyTheme()
  localStorage.setItem('theme', explicit.value)
}

let mql = null

function onSystemChange(e) {
  systemDark.value = e.matches
  if (explicit.value === null) applyTheme()
}

onMounted(() => {
  mql = window.matchMedia('(prefers-color-scheme: dark)')
  systemDark.value = mql.matches

  const stored = localStorage.getItem('theme')
  if (stored === 'light' || stored === 'dark') {
    explicit.value = stored
  }

  applyTheme()
  mql.addEventListener('change', onSystemChange)
})

onUnmounted(() => {
  if (mql) mql.removeEventListener('change', onSystemChange)
})
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.4rem;
  background: var(--bg-card-alt);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s ease-out, border-color 0.15s ease-out;
}

.theme-toggle:hover {
  color: var(--text-secondary);
  border-color: var(--border-focus);
}
</style>
