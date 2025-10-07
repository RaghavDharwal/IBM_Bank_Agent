"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface PersonalDetailsData {
  fullName: string
  age: string
  gender: string
  location: string
  contact: string
}

interface PersonalDetailsStepProps {
  data: PersonalDetailsData
  updateData: (data: Partial<PersonalDetailsData>) => void
}

export function PersonalDetailsStep({ data, updateData }: PersonalDetailsStepProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="space-y-2">
        <Label htmlFor="fullName">Full Name *</Label>
        <Input
          id="fullName"
          placeholder="Enter your full name"
          value={data.fullName}
          onChange={(e) => updateData({ fullName: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="age">Age *</Label>
        <Input
          id="age"
          type="number"
          placeholder="Enter your age"
          value={data.age}
          onChange={(e) => updateData({ age: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="gender">Gender *</Label>
        <Select value={data.gender} onValueChange={(value) => updateData({ gender: value })}>
          <SelectTrigger>
            <SelectValue placeholder="Select gender" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="male">Male</SelectItem>
            <SelectItem value="female">Female</SelectItem>
            <SelectItem value="other">Other</SelectItem>
            <SelectItem value="prefer-not-to-say">Prefer not to say</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="location">Location *</Label>
        <Input
          id="location"
          placeholder="City, State"
          value={data.location}
          onChange={(e) => updateData({ location: e.target.value })}
        />
      </div>

      <div className="space-y-2 md:col-span-2">
        <Label htmlFor="contact">Contact Number *</Label>
        <Input
          id="contact"
          type="tel"
          placeholder="Enter your mobile number"
          value={data.contact}
          onChange={(e) => updateData({ contact: e.target.value })}
        />
      </div>
    </div>
  )
}
