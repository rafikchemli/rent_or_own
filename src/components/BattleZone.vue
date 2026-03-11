<template>
  <section class="battle animate-in" :style="{ animationDelay: '0.1s' }">
    <div class="battle-grid">
      <!-- Own Fighter -->
      <div class="fighter fighter-own">
        <div class="fighter-glow own-glow"></div>
        <div class="fighter-label">Own the Home</div>
        <div class="fighter-value tabular-nums">${{ formatCurrency(finalOwn) }}</div>
        <div class="fighter-detail">net worth after {{ loanTerm }} years</div>
        <div class="fighter-stat">
          <span class="stat-label">Monthly mortgage</span>
          <span class="stat-value tabular-nums">${{ formatCurrency(monthlyMortgage) }}</span>
        </div>
      </div>

      <!-- VS Badge -->
      <div class="vs-badge-wrap">
        <div class="battle-divider"></div>
        <div class="vs-badge">
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="28" cy="28" r="28" :fill="'var(--vs-bg)'" />
            <circle cx="28" cy="28" r="25" fill="none" :stroke="'var(--vs-text)'" stroke-width="0.5" stroke-opacity="0.3" />
            <text x="28" y="30" text-anchor="middle" dominant-baseline="central"
              :fill="'var(--vs-text)'" font-family="var(--font-display)" font-size="16" font-weight="700"
              font-style="italic">VS</text>
          </svg>
        </div>
      </div>

      <!-- Rent Fighter -->
      <div class="fighter fighter-rent">
        <div class="fighter-glow rent-glow"></div>
        <div class="fighter-label">Rent & Invest</div>
        <div class="fighter-value tabular-nums">${{ formatCurrency(finalRent) }}</div>
        <div class="fighter-detail">investment portfolio at year {{ loanTerm }}</div>
        <div class="fighter-stat">
          <span class="stat-label">Monthly rent</span>
          <span class="stat-value tabular-nums">${{ formatCurrency(monthlyRent) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  finalOwn: { type: Number, required: true },
  finalRent: { type: Number, required: true },
  monthlyMortgage: { type: Number, required: true },
  monthlyRent: { type: Number, required: true },
  loanTerm: { type: Number, required: true },
})

function formatCurrency(val) {
  return Math.round(val).toLocaleString('en-US')
}
</script>

<style scoped>
.battle {
  position: relative;
}

.battle-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 0;
  align-items: stretch;
}

@media (max-width: 600px) {
  .battle-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }
}

.fighter {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem 1.25rem;
  overflow: hidden;
}

.fighter-own {
  padding-right: 2.5rem;
  text-align: right;
  background: var(--own-bg);
  border-color: var(--own-border);
}

.fighter-rent {
  padding-left: 2.5rem;
  text-align: left;
  background: var(--rent-bg);
  border-color: var(--rent-border);
}

@media (max-width: 600px) {
  .fighter-own,
  .fighter-rent {
    text-align: center;
    padding: 1.25rem;
  }
}

.fighter-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  opacity: 0.4;
  pointer-events: none;
}

.own-glow {
  background: radial-gradient(ellipse at top right, var(--own-glow) 0%, transparent 60%);
}

.rent-glow {
  background: radial-gradient(ellipse at top left, var(--rent-glow) 0%, transparent 60%);
}

.fighter-label {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.fighter-own .fighter-label {
  color: var(--own);
}

.fighter-rent .fighter-label {
  color: var(--rent);
}

.fighter-value {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.1;
}

.fighter-detail {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

.fighter-stat {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
  font-size: 0.8rem;
}

.fighter-rent .fighter-stat {
  justify-content: flex-start;
}

@media (max-width: 600px) {
  .fighter-stat {
    justify-content: center;
  }
  .fighter-rent .fighter-stat {
    justify-content: center;
  }
}

.stat-label {
  color: var(--text-muted);
}

.stat-value {
  color: var(--text-secondary);
  font-weight: 600;
}

/* VS Badge */
.vs-badge-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  z-index: var(--z-base);
}

@media (max-width: 600px) {
  .vs-badge-wrap {
    width: 100%;
    height: 48px;
  }
}

.battle-divider {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  background: var(--border);
  transform: translateX(-50%);
}

@media (max-width: 600px) {
  .battle-divider {
    top: 50%;
    bottom: auto;
    left: 0;
    right: 0;
    width: 100%;
    height: 1px;
    transform: translateY(-50%);
  }
}

.vs-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: var(--z-badge);
  border-radius: 50%;
  animation: pulse-subtle 3s ease-in-out infinite, vs-glow 3s ease-in-out infinite;
}

.vs-badge svg {
  display: block;
}
</style>
