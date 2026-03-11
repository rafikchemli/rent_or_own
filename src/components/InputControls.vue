<template>
  <section class="controls animate-in" :style="{ animationDelay: '0.05s' }">
    <div class="controls-main">
      <div class="input-group">
        <label class="input-label" for="home-value">Home Value</label>
        <div class="input-wrap">
          <span class="input-prefix">$</span>
          <input
            id="home-value"
            type="number" inputmode="decimal"
            :value="inputs.homeValue"
            @input="inputs.homeValue = +$event.target.value"
            min="50000"
            max="5000000"
            step="10000"
          />
        </div>
      </div>
      <div class="input-group">
        <label class="input-label" for="monthly-rent">Monthly Rent</label>
        <div class="input-wrap">
          <span class="input-prefix">$</span>
          <input
            id="monthly-rent"
            type="number" inputmode="decimal"
            :value="inputs.rent"
            @input="inputs.rent = +$event.target.value"
            min="200"
            max="20000"
            step="100"
          />
        </div>
      </div>
      <div class="input-group">
        <label class="input-label" for="mortgage-rate">Mortgage Rate</label>
        <div class="input-wrap">
          <input
            id="mortgage-rate"
            type="number" inputmode="decimal"
            :value="(inputs.mortgageRate * 100).toFixed(1)"
            @input="inputs.mortgageRate = +$event.target.value / 100"
            min="0"
            max="15"
            step="0.1"
          />
          <span class="input-suffix">%</span>
        </div>
      </div>
    </div>

    <button class="assumptions-toggle" @click="showAssumptions = !showAssumptions">
      <span>Assumptions</span>
      <svg
        :class="['toggle-chevron', { open: showAssumptions }]"
        width="14" height="14" viewBox="0 0 14 14" fill="none"
      >
        <path d="M3.5 5.25L7 8.75L10.5 5.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div v-if="showAssumptions" class="assumptions">
      <div class="assumptions-grid">
        <div class="input-group small">
          <label class="input-label" for="down-pct">Down Payment</label>
          <div class="input-wrap">
            <input
              id="down-pct"
              type="number" inputmode="decimal"
              :value="(inputs.downPaymentPct * 100).toFixed(0)"
              @input="inputs.downPaymentPct = +$event.target.value / 100"
              min="0" max="100" step="1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="loan-term">Loan Term</label>
          <div class="input-wrap">
            <input
              id="loan-term"
              type="number" inputmode="decimal"
              :value="inputs.loanTerm"
              @input="inputs.loanTerm = +$event.target.value"
              min="5" max="40" step="1"
            />
            <span class="input-suffix">yr</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="home-growth">Home Appreciation</label>
          <div class="input-wrap">
            <input
              id="home-growth"
              type="number" inputmode="decimal"
              :value="(inputs.homeGrowthRate * 100).toFixed(1)"
              @input="inputs.homeGrowthRate = +$event.target.value / 100"
              min="0" max="15" step="0.1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="invest-return">Investment Return</label>
          <div class="input-wrap">
            <input
              id="invest-return"
              type="number" inputmode="decimal"
              :value="(inputs.investmentReturnRate * 100).toFixed(1)"
              @input="inputs.investmentReturnRate = +$event.target.value / 100"
              min="0" max="20" step="0.1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="rent-growth">Rent Inflation</label>
          <div class="input-wrap">
            <input
              id="rent-growth"
              type="number" inputmode="decimal"
              :value="(inputs.rentGrowthRate * 100).toFixed(1)"
              @input="inputs.rentGrowthRate = +$event.target.value / 100"
              min="0" max="15" step="0.1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="maintenance">Maintenance</label>
          <div class="input-wrap">
            <input
              id="maintenance"
              type="number" inputmode="decimal"
              :value="(inputs.maintenanceRate * 100).toFixed(1)"
              @input="inputs.maintenanceRate = +$event.target.value / 100"
              min="0" max="5" step="0.1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
        <div class="input-group small">
          <label class="input-label" for="prop-tax">Property Tax</label>
          <div class="input-wrap">
            <input
              id="prop-tax"
              type="number" inputmode="decimal"
              :value="(inputs.propertyTaxRate * 100).toFixed(1)"
              @input="inputs.propertyTaxRate = +$event.target.value / 100"
              min="0" max="5" step="0.1"
            />
            <span class="input-suffix">%</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  inputs: { type: Object, required: true },
})

const showAssumptions = ref(false)
</script>

<style scoped>
.controls {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
}

.controls-main {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

@media (max-width: 600px) {
  .controls-main {
    grid-template-columns: 1fr;
  }
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.input-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.input-wrap {
  display: flex;
  align-items: center;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0 0.6rem;
  transition: border-color 0.15s ease-out;
}

.input-wrap:focus-within {
  border-color: var(--border-focus);
}

.input-prefix,
.input-suffix {
  font-size: 0.85rem;
  color: var(--text-muted);
  flex-shrink: 0;
}

.input-wrap input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  padding: 0.55rem 0.25rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-variant-numeric: tabular-nums;
  color: var(--text-primary);
  outline: none;
}

.input-wrap input::-webkit-inner-spin-button,
.input-wrap input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.input-wrap input[type='number'] {
  -moz-appearance: textfield;
}

.assumptions-toggle {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 1rem;
  padding: 0.4rem 0;
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s ease-out;
}

.assumptions-toggle:hover {
  color: var(--text-secondary);
}

.toggle-chevron {
  transition: transform 0.2s ease-out;
}

.toggle-chevron.open {
  transform: rotate(180deg);
}

.assumptions {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
}

.assumptions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

@media (max-width: 600px) {
  .assumptions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.input-group.small .input-label {
  font-size: 0.65rem;
}

.input-group.small .input-wrap {
  padding: 0 0.5rem;
}

.input-group.small .input-wrap input {
  padding: 0.4rem 0.2rem;
  font-size: 0.85rem;
}
</style>
