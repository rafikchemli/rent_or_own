<template>
  <section class="equation animate-in" :style="{ animationDelay: '0.15s' }">
    <div class="equation-inner">
      <div class="eq-term own-term">
        <span class="eq-label">Owning costs</span>
        <span class="eq-value tabular-nums">${{ formatCurrency(annualOwnCost) }}/yr</span>
      </div>
      <span class="eq-operator">&minus;</span>
      <div class="eq-term rent-term">
        <span class="eq-label">Renting costs</span>
        <span class="eq-value tabular-nums">${{ formatCurrency(annualRentCost) }}/yr</span>
      </div>
      <span class="eq-operator">=</span>
      <div class="eq-term result-term" :class="{ negative: savings < 0 }">
        <span class="eq-label">{{ savings >= 0 ? 'Invested monthly' : 'Extra cost to rent' }}</span>
        <span class="eq-value tabular-nums">${{ formatCurrency(Math.abs(savings) / 12) }}/mo</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  annualOwnCost: { type: Number, required: true },
  annualRentCost: { type: Number, required: true },
})

const savings = computed(() => props.annualOwnCost - props.annualRentCost)

function formatCurrency(val) {
  return Math.round(val).toLocaleString('en-US')
}
</script>

<style scoped>
.equation {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.85rem 1.25rem;
  box-shadow: var(--shadow-sm);
}

.equation-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.eq-term {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
}

.eq-label {
  font-size: 0.65rem;
  font-weight: 500;
  text-transform: uppercase;
  color: var(--text-muted);
}

.eq-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.own-term .eq-value {
  color: var(--own);
}

.rent-term .eq-value {
  color: var(--rent);
}

.result-term .eq-value {
  color: var(--text-primary);
}

.result-term.negative .eq-value {
  color: var(--rent);
}

.eq-operator {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-muted);
  padding: 0 0.15rem;
}
</style>
