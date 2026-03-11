<template>
  <div class="stack">
    <AppHeader />
    <InputControls v-model="inputs" />
    <BattleZone
    :finalOwn="results.own[results.own.length - 1]"
    :finalRent="results.rent[results.rent.length - 1]"
    :monthlyMortgage="results.monthlyMortgage"
    :monthlyRent="inputs.rent"
    :loanTerm="inputs.loanTerm"
  />
  <EquationBar
    :annualOwnCost="results.ownCosts[1] || 0"
    :annualRentCost="results.rentCosts[1] || 0"
  />
  <ArenaChart
    :own="results.own"
    :rent="results.rent"
    :contributions="results.contributions"
    :loanTerm="inputs.loanTerm"
  />
  <VerdictBar
    :finalOwn="results.own[results.own.length - 1]"
    :finalRent="results.rent[results.rent.length - 1]"
    :loanTerm="inputs.loanTerm"
  />
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { calculate } from './calculator.js'
import AppHeader from './components/AppHeader.vue'
import InputControls from './components/InputControls.vue'
import BattleZone from './components/BattleZone.vue'
import EquationBar from './components/EquationBar.vue'
import ArenaChart from './components/ArenaChart.vue'
import VerdictBar from './components/VerdictBar.vue'

const inputs = reactive({
  homeValue: 500000,
  rent: 2000,
  mortgageRate: 0.065,
  downPaymentPct: 0.2,
  loanTerm: 30,
  homeGrowthRate: 0.03,
  investmentReturnRate: 0.08,
  rentGrowthRate: 0.03,
  maintenanceRate: 0.01,
  propertyTaxRate: 0.012,
})

const results = computed(() => calculate(inputs))
</script>

<style scoped>
.stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
