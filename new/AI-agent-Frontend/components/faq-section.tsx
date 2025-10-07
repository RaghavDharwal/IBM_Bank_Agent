"use client"

import React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp, HelpCircle, FileText, CreditCard, Clock, Shield, Calculator } from "lucide-react"

interface FAQ {
  id: string
  question: string
  answer: string
  category: "documents" | "eligibility" | "process" | "schemes" | "general"
  icon: React.ComponentType<{ className?: string }>
}

const faqs: FAQ[] = [
  {
    id: "documents-required",
    question: "What documents are required for loan application?",
    answer:
      "Common documents include: Identity proof (Aadhaar, PAN), Address proof, Income proof (salary slips, ITR), Bank statements (6 months), Employment certificate, and Property documents (for secured loans). Specific requirements may vary by loan type and lender.",
    category: "documents",
    icon: FileText,
  },
  {
    id: "mudra-loan-limit",
    question: "What is the maximum loan amount under MUDRA scheme?",
    answer:
      "MUDRA loans are categorized into three types: Shishu (up to ₹50,000), Kishore (₹50,001 to ₹5 lakhs), and Tarun (₹5,00,001 to ₹10 lakhs). The maximum loan amount under MUDRA is ₹10 lakhs without any collateral requirement.",
    category: "schemes",
    icon: Calculator,
  },
  {
    id: "credit-score-requirement",
    question: "What credit score is required for loan approval?",
    answer:
      "Generally, a credit score of 650+ is considered good for loan approval. Scores above 750 get the best interest rates. However, some lenders may approve loans with lower scores (600+) but at higher interest rates. First-time borrowers without credit history may also be considered.",
    category: "eligibility",
    icon: CreditCard,
  },
  {
    id: "processing-time",
    question: "How long does loan processing take?",
    answer:
      "Processing time varies by loan type and lender: Personal loans: 1-7 days, Home loans: 15-30 days, Business loans: 7-21 days, Education loans: 15-30 days. Digital lenders often provide faster processing, while traditional banks may take longer for verification.",
    category: "process",
    icon: Clock,
  },
  {
    id: "pmegp-eligibility",
    question: "Who is eligible for PMEGP loans?",
    answer:
      "PMEGP (Prime Minister's Employment Generation Programme) is for individuals above 18 years with minimum 8th standard education. For SC/ST/OBC/Minorities/Women/Ex-servicemen/Physically handicapped: minimum 8th pass. For General category: Graduate or equivalent. The project cost ranges from ₹2 lakhs to ₹25 lakhs.",
    category: "schemes",
    icon: Shield,
  },
  {
    id: "loan-against-property",
    question: "Can I get a loan against my property?",
    answer:
      "Yes, Loan Against Property (LAP) allows you to mortgage your residential/commercial property for funds. You can get up to 60-70% of property value as loan amount. Interest rates are typically lower than personal loans (9-15%) with longer tenure options (up to 20 years).",
    category: "general",
    icon: HelpCircle,
  },
  {
    id: "prepayment-charges",
    question: "Are there any prepayment charges?",
    answer:
      "Prepayment charges vary by lender and loan type. For floating rate loans, RBI guidelines prohibit prepayment charges on home loans. Personal and business loans may have prepayment charges of 2-4% of outstanding amount. Some lenders waive charges after a certain period (usually 1-2 years).",
    category: "general",
    icon: Calculator,
  },
  {
    id: "co-applicant-benefits",
    question: "What are the benefits of adding a co-applicant?",
    answer:
      "Adding a co-applicant can: Increase loan eligibility amount, Improve chances of approval, Get better interest rates, Combine income for higher loan amount, Share tax benefits (for home loans), and Provide additional security to the lender.",
    category: "eligibility",
    icon: Shield,
  },
]

const categoryIcons = {
  documents: FileText,
  eligibility: CreditCard,
  process: Clock,
  schemes: Shield,
  general: HelpCircle,
}

const categoryColors = {
  documents: "text-blue-600",
  eligibility: "text-green-600",
  process: "text-orange-600",
  schemes: "text-purple-600",
  general: "text-gray-600",
}

export function FAQSection() {
  const [openItems, setOpenItems] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("all")

  const toggleItem = (id: string) => {
    setOpenItems((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }

  const filteredFAQs = selectedCategory === "all" ? faqs : faqs.filter((faq) => faq.category === selectedCategory)

  const categories = [
    { id: "all", label: "All Questions", count: faqs.length },
    { id: "documents", label: "Documents", count: faqs.filter((f) => f.category === "documents").length },
    { id: "eligibility", label: "Eligibility", count: faqs.filter((f) => f.category === "eligibility").length },
    { id: "process", label: "Process", count: faqs.filter((f) => f.category === "process").length },
    { id: "schemes", label: "Schemes", count: faqs.filter((f) => f.category === "schemes").length },
    { id: "general", label: "General", count: faqs.filter((f) => f.category === "general").length },
  ]

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 bg-accent/10 rounded-lg">
            <HelpCircle className="w-5 h-5 text-accent" />
          </div>
          <div>
            <CardTitle className="text-xl">Frequently Asked Questions</CardTitle>
            <CardDescription>Find answers to common loan-related questions</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <Button
              key={category.id}
              variant={selectedCategory === category.id ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCategory(category.id)}
              className="gap-2 "
            >
              {category.id !== "all" && (
                <div className={categoryColors[category.id as keyof typeof categoryColors]}>
                  {React.createElement(categoryIcons[category.id as keyof typeof categoryIcons], {
                    className: "w-3 h-3",
                  })}
                </div>
              )}
              {category.label}
              <span className="text-xs bg-muted px-1.5 py-0.5 rounded-full">{category.count}</span>
            </Button>
          ))}
        </div>

        {/* FAQ Items */}
        <div className="space-y-3">
          {filteredFAQs.map((faq) => {
            const IconComponent = faq.icon
            const isOpen = openItems.includes(faq.id)

            return (
              <Collapsible key={faq.id} open={isOpen} onOpenChange={() => toggleItem(faq.id)}>
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full justify-between p-4 h-auto text-left hover:text-black hover:bg-transparent"
                  >
                    <div className="flex items-start gap-3">
                      <div className={`${categoryColors[faq.category]} mt-0.5`}>
                        <IconComponent className="w-4 h-4" />
                      </div>
                      <span className="font-medium text-sm">{faq.question}</span>
                    </div>
                    {isOpen ? (
                      <ChevronUp className="w-4 h-4 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-muted-foreground" />
                    )}
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="px-4 pb-4">
                  <div className="pl-7">
                    <p className="text-sm text-muted-foreground leading-relaxed">{faq.answer}</p>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            )
          })}
        </div>

        {filteredFAQs.length === 0 && (
          <div className="text-center py-8">
            <HelpCircle className="w-12 h-12 text-muted-foreground mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">No questions found in this category</p>
          </div>
        )}

        {/* Contact Support */}
        <div className="p-4 bg-accent/5 border border-accent/20 rounded-lg">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 bg-accent rounded-lg">
              <HelpCircle className="w-4 h-4 text-accent-foreground" />
            </div>
            <div className="flex-1">
              <p className="font-medium text-sm">Still have questions?</p>
              <p className="text-xs text-muted-foreground">Our loan experts are here to help you</p>
            </div>
            <Button size="sm" className="gap-2">
              Contact Support
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
