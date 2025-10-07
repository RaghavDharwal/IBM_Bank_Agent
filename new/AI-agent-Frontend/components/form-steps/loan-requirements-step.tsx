"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { GraduationCap, Home, Briefcase, User } from "lucide-react"

interface LoanRequirementsData {
  type: string
  amount: string
  tenure: string
}

interface LoanRequirementsStepProps {
  data: LoanRequirementsData
  updateData: (data: Partial<LoanRequirementsData>) => void
}

const loanTypes = [
  { value: "education", label: "Education Loan", icon: GraduationCap, description: "For academic expenses" },
  { value: "home", label: "Home Loan", icon: Home, description: "For property purchase" },
  { value: "business", label: "Business Loan", icon: Briefcase, description: "For business needs" },
  { value: "personal", label: "Personal Loan", icon: User, description: "For personal expenses" },
]

export function LoanRequirementsStep({ data, updateData }: LoanRequirementsStepProps) {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <Label>Loan Type *</Label>
        <RadioGroup
          value={data.type}
          onValueChange={(value) => updateData({ type: value })}
          className="grid gap-4 md:grid-cols-2"
        >
          {loanTypes.map((type) => {
            const IconComponent = type.icon
            return (
              <div key={type.value} className="flex items-center space-x-2">
                <RadioGroupItem value={type.value} id={type.value} />
                <Label
                  htmlFor={type.value}
                  className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-muted flex-1"
                >
                  <IconComponent className="w-5 h-5 text-accent" />
                  <div>
                    <p className="font-medium">{type.label}</p>
                    <p className="text-sm text-muted-foreground">{type.description}</p>
                  </div>
                </Label>
              </div>
            )
          })}
        </RadioGroup>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="amount">Loan Amount (₹) *</Label>
          <Input
            id="amount"
            type="number"
            placeholder="Enter loan amount"
            value={data.amount}
            onChange={(e) => updateData({ amount: e.target.value })}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="tenure">Tenure Preference *</Label>
          <Select value={data.tenure} onValueChange={(value) => updateData({ tenure: value })}>
            <SelectTrigger>
              <SelectValue placeholder="Select tenure" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1-year">1 Year</SelectItem>
              <SelectItem value="2-years">2 Years</SelectItem>
              <SelectItem value="3-years">3 Years</SelectItem>
              <SelectItem value="5-years">5 Years</SelectItem>
              <SelectItem value="7-years">7 Years</SelectItem>
              <SelectItem value="10-years">10 Years</SelectItem>
              <SelectItem value="15-years">15 Years</SelectItem>
              <SelectItem value="20-years">20 Years</SelectItem>
              <SelectItem value="30-years">30 Years</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="p-4 bg-accent/5 border border-accent/20 rounded-lg">
        <p className="text-sm text-foreground">
          <strong>Note:</strong> The final loan amount and tenure will be subject to eligibility criteria and bank
          approval. Interest rates may vary based on your credit profile and chosen loan type.
        </p>
      </div>
    </div>
  )
}
