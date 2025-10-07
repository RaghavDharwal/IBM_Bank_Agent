"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"

interface EmploymentData {
  status: string
  monthlyIncome: string
  creditScore: string
}

interface EmploymentStepProps {
  data: EmploymentData
  updateData: (data: Partial<EmploymentData>) => void
}

export function EmploymentStep({ data, updateData }: EmploymentStepProps) {
  const creditScore = Number.parseInt(data.creditScore) || 650

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="status">Employment Status *</Label>
          <Select value={data.status} onValueChange={(value) => updateData({ status: value })}>
            <SelectTrigger>
              <SelectValue placeholder="Select employment status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="student">Student</SelectItem>
              <SelectItem value="salaried">Salaried Employee</SelectItem>
              <SelectItem value="self-employed">Self-employed</SelectItem>
              <SelectItem value="business-owner">Business Owner</SelectItem>
              <SelectItem value="unemployed">Unemployed</SelectItem>
              <SelectItem value="retired">Retired</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="monthlyIncome">Monthly Income (₹) *</Label>
          <Input
            id="monthlyIncome"
            type="number"
            placeholder="Enter monthly income"
            value={data.monthlyIncome}
            onChange={(e) => updateData({ monthlyIncome: e.target.value })}
          />
        </div>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Label>Credit Score</Label>
          <div className="px-4">
            <Slider
              value={[creditScore]}
              onValueChange={(value) => updateData({ creditScore: value[0].toString() })}
              max={850}
              min={300}
              step={10}
              className="w-full"
            />
            <div className="flex justify-between text-sm text-muted-foreground mt-2">
              <span>300 (Poor)</span>
              <span className="font-medium text-foreground">{creditScore}</span>
              <span>850 (Excellent)</span>
            </div>
          </div>
        </div>

        <div className="p-4 bg-muted rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong>Credit Score Guide:</strong> 300-579 (Poor), 580-669 (Fair), 670-739 (Good), 740-799 (Very Good),
            800-850 (Excellent)
          </p>
        </div>
      </div>
    </div>
  )
}
