"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Bot, TrendingUp, AlertCircle, CheckCircle, Lightbulb, ExternalLink } from "lucide-react"
import type { FormData } from "./loan-application-form"

interface AISuggestion {
  id: string
  type: "recommendation" | "warning" | "tip" | "eligibility"
  title: string
  description: string
  details?: string[]
  action?: string
}

interface AISuggestionsPanelProps {
  formData: FormData
  currentStep: number
}

export function AISuggestionsPanel({ formData, currentStep }: AISuggestionsPanelProps) {
  const [suggestions, setSuggestions] = useState<AISuggestion[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // Generate AI suggestions based on form data
  useEffect(() => {
    const generateSuggestions = () => {
      setIsLoading(true)
      const newSuggestions: AISuggestion[] = []

      // Personal details suggestions
      if (currentStep >= 1 && formData.personal.age) {
        const age = Number.parseInt(formData.personal.age)
        if (age < 25) {
          newSuggestions.push({
            id: "young-professional",
            type: "recommendation",
            title: "Young Professional Benefits",
            description: "As a young applicant, you may qualify for special interest rates and longer tenure options.",
            details: ["0.25% interest rate reduction", "Extended repayment period", "Lower processing fees"],
          })
        }
      }

      // Employment-based suggestions
      if (currentStep >= 2 && formData.employment.status && formData.employment.monthlyIncome) {
        const income = Number.parseInt(formData.employment.monthlyIncome)
        const status = formData.employment.status

        if (status === "salaried" && income >= 50000) {
          newSuggestions.push({
            id: "high-income-salaried",
            type: "eligibility",
            title: "Premium Loan Eligibility",
            description: "Based on your salaried status and income, you're eligible for premium loan products.",
            details: ["Up to ₹50 Lakhs loan amount", "Interest rates from 8.5%", "Quick approval process"],
            action: "View Premium Options",
          })
        }

        if (status === "self-employed") {
          newSuggestions.push({
            id: "self-employed-schemes",
            type: "recommendation",
            title: "Government Schemes Available",
            description: "MUDRA and PMEGP loans offer excellent terms for self-employed individuals.",
            details: ["MUDRA: Up to ₹10 Lakhs", "PMEGP: Up to ₹25 Lakhs", "Subsidized interest rates: 7-9%"],
          })
        }

        if (income < 25000) {
          newSuggestions.push({
            id: "low-income-warning",
            type: "warning",
            title: "Income Consideration",
            description: "Your current income may limit loan options. Consider a co-applicant to improve eligibility.",
            details: [
              "Co-applicant can increase loan amount",
              "Better interest rates possible",
              "Higher approval chances",
            ],
          })
        }
      }

      // Credit score suggestions
      if (formData.employment.creditScore) {
        const creditScore = Number.parseInt(formData.employment.creditScore)

        if (creditScore >= 750) {
          newSuggestions.push({
            id: "excellent-credit",
            type: "recommendation",
            title: "Excellent Credit Score Benefits",
            description: "Your high credit score qualifies you for the best interest rates and terms.",
            details: ["Lowest interest rates available", "Higher loan amounts", "Faster approval process"],
          })
        } else if (creditScore < 650) {
          newSuggestions.push({
            id: "improve-credit",
            type: "tip",
            title: "Credit Score Improvement",
            description: "Consider improving your credit score for better loan terms.",
            details: ["Pay existing EMIs on time", "Reduce credit utilization", "Check credit report for errors"],
          })
        }
      }

      // Loan type specific suggestions
      if (currentStep >= 3 && formData.loan.type && formData.loan.amount) {
        const loanType = formData.loan.type
        const amount = Number.parseInt(formData.loan.amount)

        if (loanType === "education" && amount > 1000000) {
          newSuggestions.push({
            id: "education-loan-benefits",
            type: "recommendation",
            title: "Education Loan Tax Benefits",
            description: "Education loans offer significant tax deductions under Section 80E.",
            details: ["Interest deduction for 8 years", "No upper limit on deduction", "Moratorium period available"],
          })
        }

        if (loanType === "home" && amount > 2000000) {
          newSuggestions.push({
            id: "home-loan-benefits",
            type: "recommendation",
            title: "Home Loan Tax Benefits",
            description: "Maximize your tax savings with home loan deductions.",
            details: [
              "₹2 Lakhs interest deduction (Section 24)",
              "₹1.5 Lakhs principal deduction (Section 80C)",
              "Additional ₹1.5 Lakhs for first-time buyers",
            ],
          })
        }

        if (loanType === "business") {
          newSuggestions.push({
            id: "business-loan-schemes",
            type: "eligibility",
            title: "Government Business Schemes",
            description: "Multiple government schemes available for business loans with subsidized rates.",
            details: [
              "MUDRA Yojana: Up to ₹10 Lakhs",
              "Stand-Up India: ₹10 Lakhs to ₹1 Crore",
              "PMEGP: Up to ₹25 Lakhs with subsidy",
            ],
            action: "Explore Schemes",
          })
        }
      }

      // Always show a general tip
      newSuggestions.push({
        id: "general-tip",
        type: "tip",
        title: "Pro Tip",
        description: "Compare offers from multiple lenders to get the best deal on your loan.",
        details: ["Check interest rates", "Compare processing fees", "Review prepayment charges"],
      })

      setTimeout(() => {
        setSuggestions(newSuggestions)
        setIsLoading(false)
      }, 500)
    }

    generateSuggestions()
  }, [formData, currentStep])

  const getSuggestionIcon = (type: AISuggestion["type"]) => {
    switch (type) {
      case "recommendation":
        return <TrendingUp className="w-4 h-4" />
      case "warning":
        return <AlertCircle className="w-4 h-4" />
      case "tip":
        return <Lightbulb className="w-4 h-4" />
      case "eligibility":
        return <CheckCircle className="w-4 h-4" />
      default:
        return <Bot className="w-4 h-4" />
    }
  }

  const getSuggestionColor = (type: AISuggestion["type"]) => {
    switch (type) {
      case "recommendation":
        return "text-accent"
      case "warning":
        return "text-destructive"
      case "tip":
        return "text-chart-4"
      case "eligibility":
        return "text-green-600"
      default:
        return "text-accent"
    }
  }

  const getBadgeVariant = (type: AISuggestion["type"]) => {
    switch (type) {
      case "recommendation":
        return "secondary" as const
      case "warning":
        return "destructive" as const
      case "tip":
        return "outline" as const
      case "eligibility":
        return "default" as const
      default:
        return "secondary" as const
    }
  }

  return (
    <Card className="sticky top-6">
      <CardHeader>
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-8 h-8 bg-accent rounded-lg">
            <Bot className="w-4 h-4 text-accent-foreground" />
          </div>
          <div>
            <CardTitle className="text-lg">AI Loan Advisor</CardTitle>
            <CardDescription>Personalized recommendations for you</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
          </div>
        ) : suggestions.length > 0 ? (
          suggestions.map((suggestion) => (
            <div key={suggestion.id} className="p-4 border rounded-lg space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <div className={getSuggestionColor(suggestion.type)}>{getSuggestionIcon(suggestion.type)}</div>
                  <h4 className="font-medium text-sm">{suggestion.title}</h4>
                </div>
                <Badge variant={getBadgeVariant(suggestion.type)} className="text-xs">
                  {suggestion.type}
                </Badge>
              </div>

              <p className="text-sm text-muted-foreground">{suggestion.description}</p>

              {suggestion.details && (
                <ul className="space-y-1">
                  {suggestion.details.map((detail, index) => (
                    <li key={index} className="flex items-center gap-2 text-xs text-muted-foreground">
                      <div className="w-1 h-1 bg-accent rounded-full" />
                      {detail}
                    </li>
                  ))}
                </ul>
              )}

              {suggestion.action && (
                <Button variant="outline" size="sm" className="w-full gap-2 text-xs bg-transparent">
                  {suggestion.action}
                  <ExternalLink className="w-3 h-3" />
                </Button>
              )}
            </div>
          ))
        ) : (
          <div className="text-center py-8">
            <Bot className="w-12 h-12 text-muted-foreground mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">Fill out the form to get personalized loan recommendations</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
