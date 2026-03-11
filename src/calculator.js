/**
 * Core financial calculation engine.
 * Compares net worth trajectory of buying a home vs renting and investing the difference.
 */
export function calculate({
  homeValue,
  mortgageRate,
  maintenanceRate,
  propertyTaxRate,
  homeGrowthRate,
  rent,
  rentGrowthRate,
  investmentReturnRate,
  loanTerm,
  downPaymentPct,
}) {
  const downPayment = homeValue * downPaymentPct
  const principal = homeValue - downPayment

  let monthlyMortgage
  if (mortgageRate === 0) {
    monthlyMortgage = principal / (loanTerm * 12)
  } else {
    const mpf = mortgageRate / 12
    monthlyMortgage = (mpf * principal) / (1 - Math.pow(1 + mpf, -(loanTerm * 12)))
  }

  let outstanding = principal
  let currentHome = homeValue
  let investmentFund = downPayment
  let totalContributed = downPayment

  const netWorthOwn = [downPayment]
  const owningCosts = [0]
  const netWorthRent = [downPayment]
  const rentingCosts = [0]
  const cumulativeContributions = [downPayment]

  for (let i = 1; i <= loanTerm; i++) {
    const annualMortgage = monthlyMortgage * 12
    const interest = outstanding * mortgageRate
    outstanding -= (annualMortgage - interest)

    const annualOwnCost =
      annualMortgage +
      (currentHome - outstanding) * (maintenanceRate + propertyTaxRate)
    owningCosts.push(annualOwnCost)

    currentHome *= 1 + homeGrowthRate
    netWorthOwn.push(currentHome - Math.max(outstanding, 0))

    const annualRent = rent * 12 * Math.pow(1 + rentGrowthRate, i - 1)
    rentingCosts.push(annualRent)

    const savings = annualOwnCost - annualRent
    if (savings > 0) {
      totalContributed += savings
    }
    investmentFund += savings
    investmentFund *= 1 + investmentReturnRate

    netWorthRent.push(investmentFund)
    cumulativeContributions.push(totalContributed)
  }

  return {
    own: netWorthOwn,
    rent: netWorthRent,
    ownCosts: owningCosts,
    rentCosts: rentingCosts,
    contributions: cumulativeContributions,
    monthlyMortgage,
  }
}
