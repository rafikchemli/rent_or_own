import { describe, it, expect } from 'vitest'
import { calculate } from './calculator.js'

const defaults = {
  homeValue: 500000,
  mortgageRate: 0.065,
  maintenanceRate: 0.01,
  propertyTaxRate: 0.012,
  homeGrowthRate: 0.03,
  rent: 2000,
  rentGrowthRate: 0.03,
  investmentReturnRate: 0.08,
  loanTerm: 30,
  downPaymentPct: 0.2,
}

describe('calculate', () => {
  const r = calculate(defaults)

  it('returns arrays of correct length', () => {
    expect(r.own).toHaveLength(31) // year 0..30
    expect(r.rent).toHaveLength(31)
    expect(r.ownCosts).toHaveLength(31)
    expect(r.rentCosts).toHaveLength(31)
    expect(r.contributions).toHaveLength(31)
  })

  it('year 0 starts at down payment for both sides', () => {
    expect(r.own[0]).toBe(100000)
    expect(r.rent[0]).toBe(100000)
  })

  it('year 0 costs are zero', () => {
    expect(r.ownCosts[0]).toBe(0)
    expect(r.rentCosts[0]).toBe(0)
  })

  describe('mortgage payment', () => {
    it('computes standard amortization for 400K at 6.5% over 30yr', () => {
      // Known value: ~$2,528/mo
      expect(r.monthlyMortgage).toBeCloseTo(2528.27, 0)
    })

    it('handles zero interest rate', () => {
      const r0 = calculate({ ...defaults, mortgageRate: 0 })
      // 400K / (30*12) = 1111.11
      expect(r0.monthlyMortgage).toBeCloseTo(1111.11, 0)
    })
  })

  describe('owning costs', () => {
    it('year 1 = mortgage + maintenance + property tax on home value', () => {
      const annualMortgage = r.monthlyMortgage * 12
      const expectedMaint = 500000 * 0.01
      const expectedTax = 500000 * 0.012
      expect(r.ownCosts[1]).toBeCloseTo(annualMortgage + expectedMaint + expectedTax, 2)
    })

    it('maintenance and tax are on home value, not equity', () => {
      // If they were on equity (~100K), costs would be much lower
      const annualMortgage = r.monthlyMortgage * 12
      const costOnEquity = annualMortgage + 100000 * (0.01 + 0.012)
      expect(r.ownCosts[1]).toBeGreaterThan(costOnEquity)
    })
  })

  describe('renting costs', () => {
    it('year 1 rent = monthly * 12', () => {
      expect(r.rentCosts[1]).toBe(2000 * 12)
    })

    it('rent inflates each year', () => {
      expect(r.rentCosts[2]).toBeCloseTo(2000 * 12 * 1.03, 2)
      expect(r.rentCosts[3]).toBeCloseTo(2000 * 12 * 1.03 ** 2, 2)
    })
  })

  describe('home equity', () => {
    it('appreciates over time', () => {
      expect(r.own[30]).toBeGreaterThan(r.own[1])
    })

    it('year 1 equity = appreciated home - remaining mortgage', () => {
      const appreciated = 500000 * 1.03
      const annualMortgage = r.monthlyMortgage * 12
      const interest = 400000 * 0.065
      const remainingMortgage = 400000 - (annualMortgage - interest)
      expect(r.own[1]).toBeCloseTo(appreciated - remainingMortgage, 0)
    })

    it('outstanding never goes below zero in equity calc', () => {
      // With a short term, outstanding could go negative due to rounding
      const short = calculate({ ...defaults, loanTerm: 5 })
      short.own.forEach((val) => {
        expect(val).toBeGreaterThanOrEqual(0)
      })
    })
  })

  describe('investment fund', () => {
    it('grows with returns', () => {
      expect(r.rent[30]).toBeGreaterThan(r.rent[0])
    })

    it('year 1 = (downPayment + savings) * (1 + return)', () => {
      const savings = r.ownCosts[1] - r.rentCosts[1]
      const expected = (100000 + savings) * 1.08
      expect(r.rent[1]).toBeCloseTo(expected, 2)
    })
  })

  describe('contributions tracking', () => {
    it('starts at down payment', () => {
      expect(r.contributions[0]).toBe(100000)
    })

    it('only increases when savings are positive', () => {
      for (let i = 1; i < r.contributions.length; i++) {
        expect(r.contributions[i]).toBeGreaterThanOrEqual(r.contributions[i - 1])
      }
    })
  })

  describe('edge cases', () => {
    it('100% down payment means zero mortgage', () => {
      const r100 = calculate({ ...defaults, downPaymentPct: 1 })
      expect(r100.monthlyMortgage).toBe(0)
    })

    it('0% down payment uses full home value as principal', () => {
      const r0 = calculate({ ...defaults, downPaymentPct: 0 })
      // Mortgage on 500K at 6.5%
      expect(r0.monthlyMortgage).toBeGreaterThan(3000)
      expect(r0.own[0]).toBe(0)
      expect(r0.rent[0]).toBe(0)
    })

    it('no appreciation means home value stays flat', () => {
      const rFlat = calculate({ ...defaults, homeGrowthRate: 0, loanTerm: 5 })
      // After 5 years equity = 500K - outstanding (no appreciation)
      expect(rFlat.own[5]).toBeLessThan(500000)
    })

    it('no investment return means fund only grows by contributions', () => {
      const rNoReturn = calculate({ ...defaults, investmentReturnRate: 0 })
      // Year 1: fund = downPayment + savings (no compounding)
      const savings = rNoReturn.ownCosts[1] - rNoReturn.rentCosts[1]
      expect(rNoReturn.rent[1]).toBeCloseTo(100000 + savings, 2)
    })
  })
})
