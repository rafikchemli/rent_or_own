<template>
  <section class="arena animate-in" :style="{ animationDelay: '0.2s' }">
    <div class="arena-header">
      <h2 class="arena-title">The Arena</h2>
      <p class="arena-subtitle">Net worth trajectory over {{ loanTerm }} years</p>
    </div>
    <div class="chart-wrap">
      <canvas ref="canvasRef"></canvas>
    </div>
    <div v-if="crossoverYear" class="crossover-note">
      Lines cross at year {{ crossoverYear }} &mdash;
      <template v-if="ownLeadsFirst">owning leads early, renting catches up.</template>
      <template v-else>renting leads early, owning catches up.</template>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip,
  Legend,
  annotationPlugin,
)

const props = defineProps({
  own: { type: Array, required: true },
  rent: { type: Array, required: true },
  contributions: { type: Array, required: true },
  loanTerm: { type: Number, required: true },
})

const canvasRef = ref(null)
let chart = null

const crossoverYear = computed(() => {
  for (let i = 1; i < props.own.length; i++) {
    const prevDiff = props.own[i - 1] - props.rent[i - 1]
    const currDiff = props.own[i] - props.rent[i]
    if (prevDiff * currDiff < 0) return i
  }
  return null
})

const ownLeadsFirst = computed(() => {
  if (!crossoverYear.value) return false
  return props.own[0] > props.rent[0] || props.own[1] > props.rent[1]
})

function getThemeColors() {
  const style = getComputedStyle(document.documentElement)
  return {
    own: style.getPropertyValue('--own').trim(),
    rent: style.getPropertyValue('--rent').trim(),
    textPrimary: style.getPropertyValue('--text-primary').trim(),
    textMuted: style.getPropertyValue('--text-muted').trim(),
    border: style.getPropertyValue('--border').trim(),
    bgPage: style.getPropertyValue('--bg-page').trim(),
    ownBg: style.getPropertyValue('--own-bg').trim(),
    rentBg: style.getPropertyValue('--rent-bg').trim(),
  }
}

function buildChart() {
  if (!canvasRef.value) return
  if (chart) chart.destroy()

  const c = getThemeColors()
  const labels = Array.from({ length: props.loanTerm + 1 }, (_, i) => `${i}`)

  const annotations = {}
  if (crossoverYear.value) {
    annotations.crossover = {
      type: 'line',
      xMin: crossoverYear.value,
      xMax: crossoverYear.value,
      borderColor: c.textMuted,
      borderWidth: 1,
      borderDash: [4, 4],
      label: {
        display: true,
        content: `Year ${crossoverYear.value}`,
        position: 'start',
        backgroundColor: 'transparent',
        color: c.textMuted,
        font: { size: 11, family: "'Plus Jakarta Sans', sans-serif" },
      },
    }
  }

  chart = new Chart(canvasRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Home Equity',
          data: props.own,
          borderColor: c.own,
          backgroundColor: c.ownBg,
          borderWidth: 2.5,
          pointRadius: 0,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: c.own,
          pointHoverBorderColor: c.own,
          tension: 0.3,
          order: 1,
        },
        {
          label: 'Investment Value',
          data: props.rent,
          borderColor: c.rent,
          backgroundColor: c.rentBg,
          borderWidth: 2.5,
          pointRadius: 0,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: c.rent,
          pointHoverBorderColor: c.rent,
          tension: 0.3,
          order: 2,
        },
        {
          label: 'Contributions',
          data: props.contributions,
          borderColor: c.rent,
          borderWidth: 1,
          borderDash: [4, 4],
          backgroundColor: c.rentBg,
          fill: '-1',
          pointRadius: 0,
          pointHoverRadius: 4,
          pointHoverBackgroundColor: c.rent,
          pointHoverBorderColor: c.rent,
          tension: 0.3,
          order: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'nearest',
        intersect: false,
        axis: 'xy',
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            color: c.textMuted,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
            boxWidth: 12,
            boxHeight: 2,
            padding: 16,
            usePointStyle: false,
          },
        },
        tooltip: {
          backgroundColor: c.textPrimary,
          titleColor: c.bgPage,
          bodyColor: c.bgPage,
          titleFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
          bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 13 },
          padding: { top: 8, bottom: 8, left: 12, right: 12 },
          cornerRadius: 8,
          displayColors: true,
          boxWidth: 8,
          boxHeight: 8,
          boxPadding: 4,
          callbacks: {
            title: (items) => `Year ${items[0].label}`,
            label: (ctx) => {
              const val = Math.round(ctx.parsed.y).toLocaleString('en-US')
              return ` ${ctx.dataset.label}: $${val}`
            },
          },
        },
        annotation: {
          annotations,
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            color: c.textMuted,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
            maxTicksLimit: 10,
          },
          border: { display: false },
        },
        y: {
          grid: {
            color: c.border,
            lineWidth: 0.5,
          },
          ticks: {
            color: c.textMuted,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
            callback: (v) => {
              if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}M`
              if (v >= 1_000) return `$${(v / 1_000).toFixed(0)}K`
              return `$${v}`
            },
          },
          border: { display: false },
        },
      },
    },
  })
}

let mql = null
let themeObserver = null

function onSchemeChange() {
  buildChart()
}

onMounted(() => {
  buildChart()
  mql = window.matchMedia('(prefers-color-scheme: dark)')
  mql.addEventListener('change', onSchemeChange)

  // Watch for manual theme toggle (data-theme attribute changes)
  themeObserver = new MutationObserver(onSchemeChange)
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  })
})

onUnmounted(() => {
  if (chart) chart.destroy()
  if (mql) mql.removeEventListener('change', onSchemeChange)
  if (themeObserver) themeObserver.disconnect()
})

watch(() => [props.own, props.rent, props.contributions, props.loanTerm], buildChart, { deep: true })
</script>

<style scoped>
.arena {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem 1.25rem;
  box-shadow: var(--shadow-md);
}

.arena-header {
  text-align: center;
  margin-bottom: 1rem;
}

.arena-title {
  font-size: 1.15rem;
  color: var(--text-primary);
}

.arena-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.15rem;
}

.chart-wrap {
  position: relative;
  height: 340px;
}

@media (max-width: 600px) {
  .chart-wrap {
    height: 260px;
  }
}

.crossover-note {
  text-align: center;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 0.75rem;
}
</style>
