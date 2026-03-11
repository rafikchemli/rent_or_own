<template>
  <section class="verdict animate-in" :style="{ animationDelay: '0.25s' }">
    <div class="verdict-inner">
      <span class="verdict-marker" :class="winner"></span>
      <p class="verdict-text">
        <template v-if="winner === 'own'">
          <strong>Owning wins</strong> by
          <span class="verdict-amount tabular-nums">${{ formatCurrency(Math.abs(diff)) }}</span>
          after {{ loanTerm }} years. Your home equity outpaces the investment portfolio.
        </template>
        <template v-else-if="winner === 'rent'">
          <strong>Renting & investing wins</strong> by
          <span class="verdict-amount tabular-nums">${{ formatCurrency(Math.abs(diff)) }}</span>
          after {{ loanTerm }} years. The market returns beat home appreciation.
        </template>
        <template v-else>
          <strong>It's a tie.</strong> Both paths end at roughly the same net worth after {{ loanTerm }} years.
        </template>
      </p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  finalOwn: { type: Number, required: true },
  finalRent: { type: Number, required: true },
  loanTerm: { type: Number, required: true },
})

const diff = computed(() => props.finalOwn - props.finalRent)

const winner = computed(() => {
  const threshold = Math.max(props.finalOwn, props.finalRent) * 0.01
  if (Math.abs(diff.value) < threshold) return 'tie'
  return diff.value > 0 ? 'own' : 'rent'
})

function formatCurrency(val) {
  return Math.round(val).toLocaleString('en-US')
}
</script>

<style scoped>
.verdict {
  background: var(--verdict-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
}

.verdict-inner {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.verdict-marker {
  width: 4px;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 2px;
  background: var(--text-muted);
}

.verdict-marker.own {
  background: var(--own);
}

.verdict-marker.rent {
  background: var(--rent);
}

.verdict-text {
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.verdict-text strong {
  color: var(--text-primary);
}

.verdict-amount {
  font-weight: 700;
  color: var(--text-primary);
}
</style>
