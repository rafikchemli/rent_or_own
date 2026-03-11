<template>
  <header class="header animate-in">
    <div class="header-row">
      <div class="header-spacer"></div>
      <div class="header-center">
        <h1 class="header-title">Rent <span class="header-or">or</span> Own</h1>
        <p class="header-subtitle">The financial face-off that settles it once and for all.</p>
      </div>
      <div class="header-actions">
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>

<script setup>
import ThemeToggle from './ThemeToggle.vue'
</script>

<style scoped>
.header {
  padding: 1rem 0 1.5rem;
}

.header-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: start;
}

.header-center {
  text-align: center;
}

.header-actions {
  display: flex;
  justify-content: flex-end;
}

.header-title {
  font-size: 2.25rem;
  color: var(--text-primary);
}

.header-or {
  font-style: italic;
  font-weight: 400;
  color: var(--text-muted);
}

.header-subtitle {
  margin-top: 0.35rem;
  font-size: 0.95rem;
  color: var(--text-secondary);
}
</style>
