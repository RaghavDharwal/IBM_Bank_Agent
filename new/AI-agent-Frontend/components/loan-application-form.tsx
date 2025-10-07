"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { PersonalDetailsStep } from "@/components/form-steps/personal-details-step"
import { EmploymentStep } from "@/components/form-steps/employment-step"
import { LoanRequirementsStep } from "@/components/form-steps/loan-requirements-step"
import { SubmissionSuccess } from "@/components/submission-success"
import { ChevronLeft, ChevronRight, CheckCircle, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export interface FormData {
  personal: {
    fullName: string
    age: string
    gender: string
    location: string
    contact: string
  }
  employment: {
    status: string
    monthlyIncome: string
    creditScore: string
  }
  loan: {
    type: string
    amount: string
    tenure: string
  }
}

const steps = [
  { id: 1, title: "Personal Details", description: "Basic information about you" },
  { id: 2, title: "Employment & Eligibility", description: "Your employment and financial status" },
  { id: 3, title: "Loan Requirements", description: "Details about your loan needs" },
]

interface LoanApplicationFormProps {
  formData?: FormData
  setFormData?: (data: FormData) => void
  currentStep?: number
  setCurrentStep?: (step: number) => void
  onSuccess?: () => void
}

export function LoanApplicationForm({
  formData: externalFormData,
  setFormData: externalSetFormData,
  currentStep: externalCurrentStep,
  setCurrentStep: externalSetCurrentStep,
  onSuccess
}: LoanApplicationFormProps) {
  const initialFormData: FormData = {
    personal: {
      fullName: "",
      age: "",
      gender: "",
      location: "",
      contact: "",
    },
    employment: {
      status: "",
      monthlyIncome: "",
      creditScore: "",
    },
    loan: {
      type: "",
      amount: "",
      tenure: "",
    },
  }

  const [internalCurrentStep, setInternalCurrentStep] = useState(1)
  const [internalFormData, setInternalFormData] = useState<FormData>(initialFormData)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [validationErrors, setValidationErrors] = useState<string[]>([])

  const currentStep = externalCurrentStep ?? internalCurrentStep
  const setCurrentStep = externalSetCurrentStep ?? setInternalCurrentStep
  const formData = externalFormData ?? internalFormData
  const setFormData = externalSetFormData ?? setInternalFormData

  const updateFormData = (section: keyof FormData, data: Partial<FormData[keyof FormData]>) => {
    if (!externalSetFormData) {
      // Internal state: can use updater function
      setInternalFormData((prev) => ({
        ...prev,
        [section]: { ...prev[section], ...data },
      }))
    } else {
      // External prop: must pass new value directly
      if (!formData) return;
      externalSetFormData({
        ...formData,
        [section]: { ...formData[section], ...data },
      })
    }
    // Clear validation errors when user updates data
    if (validationErrors.length > 0) {
      setValidationErrors([])
    }
  }

  const validateCurrentStep = (): boolean => {
    const errors: string[] = []

    if (currentStep === 1) {
      if (!formData.personal.fullName.trim()) errors.push("Full name is required")
      if (!formData.personal.age.trim()) errors.push("Age is required")
      if (!formData.personal.gender.trim()) errors.push("Gender is required")
      if (!formData.personal.location.trim()) errors.push("Location is required")
      if (!formData.personal.contact.trim()) errors.push("Contact number is required")

      // Additional validations
      const age = Number.parseInt(formData.personal.age)
      if (age && (age < 18 || age > 80)) errors.push("Age must be between 18 and 80 years")

      const contact = formData.personal.contact.replace(/\D/g, "")
      if (contact && contact.length !== 10) errors.push("Contact number must be 10 digits")
    }

    if (currentStep === 2) {
      if (!formData.employment.status.trim()) errors.push("Employment status is required")
      if (!formData.employment.monthlyIncome.trim()) errors.push("Monthly income is required")
      if (!formData.employment.creditScore.trim()) errors.push("Credit score is required")

      // Additional validations
      const income = Number.parseInt(formData.employment.monthlyIncome)
      if (income && income < 0) errors.push("Monthly income must be a positive number")

      const creditScore = Number.parseInt(formData.employment.creditScore)
      if (creditScore && (creditScore < 300 || creditScore > 850)) {
        errors.push("Credit score must be between 300 and 850")
      }
    }

    if (currentStep === 3) {
      if (!formData.loan.type.trim()) errors.push("Loan type is required")
      if (!formData.loan.amount.trim()) errors.push("Loan amount is required")
      if (!formData.loan.tenure.trim()) errors.push("Tenure preference is required")

      // Additional validations
      const amount = Number.parseInt(formData.loan.amount)
      if (amount && amount < 10000) errors.push("Minimum loan amount is ₹10,000")
      if (amount && amount > 50000000) errors.push("Maximum loan amount is ₹5 Crores")
    }

    setValidationErrors(errors)
    return errors.length === 0
  }

  const nextStep = () => {
    if (validateCurrentStep() && currentStep < steps.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
      setValidationErrors([]) // Clear errors when going back
    }
  }

  const handleSubmit = async () => {
    if (!validateCurrentStep()) {
      return
    }

    setIsSubmitting(true)

    try {
      // Get token from localStorage for authentication
      const token = localStorage.getItem('token')
      if (!token) {
        setValidationErrors(["Please login to submit your application."])
        setIsSubmitting(false)
        return
      }

      // Format the data for submission
      const submissionData = {
        personal: {
          name: formData.personal.fullName,
          age: Number.parseInt(formData.personal.age),
          gender: formData.personal.gender,
          location: formData.personal.location,
          contact: formData.personal.contact,
        },
        employment: {
          status: formData.employment.status,
          income: Number.parseInt(formData.employment.monthlyIncome),
          creditScore: Number.parseInt(formData.employment.creditScore),
        },
        loan: {
          type: formData.loan.type,
          amount: Number.parseInt(formData.loan.amount),
          tenure: formData.loan.tenure,
        },
        metadata: {
          submittedAt: new Date().toISOString(),
          applicationId: `LOAN-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
          source: "loan-advisor-dashboard",
        },
      }

      // Log the formatted data (as specified in requirements)
      console.log("=== LOAN APPLICATION SUBMITTED ===")
      console.log(JSON.stringify(submissionData, null, 2))
      console.log("===================================")

      // Send data to backend
      const response = await fetch('http://localhost:5001/api/loan-applications', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(submissionData)
      })

      if (response.ok) {
        const responseData = await response.json()
        console.log("Application submitted successfully:", responseData)
        setIsSubmitted(true)
        // Call onSuccess callback if provided
        if (onSuccess) {
          onSuccess()
        }
      } else {
        const errorData = await response.json()
        setValidationErrors([errorData.message || "Failed to submit application. Please try again."])
      }
    } catch (error) {
      console.error("Submission error:", error)
      setValidationErrors(["Network error. Please check your connection and try again."])
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSubmitted) {
    return <SubmissionSuccess />
  }

  const progress = (currentStep / steps.length) * 100

  return (
    <div className="space-y-6">
      {/* Validation Errors */}
      {validationErrors.length > 0 && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            <div className="space-y-1">
              <p className="font-medium">Please fix the following errors:</p>
              <ul className="list-disc list-inside space-y-1">
                {validationErrors.map((error, index) => (
                  <li key={index} className="text-sm">
                    {error}
                  </li>
                ))}
              </ul>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Progress Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <div>
              <CardTitle>
                Step {currentStep} of {steps.length}
              </CardTitle>
              <CardDescription>{steps[currentStep - 1].description}</CardDescription>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-foreground">{Math.round(progress)}% Complete</p>
            </div>
          </div>
          <Progress value={progress} className="h-2" />
        </CardHeader>
      </Card>

      {/* Step Indicators */}
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center">
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                currentStep > step.id
                  ? "bg-accent border-accent text-accent-foreground"
                  : currentStep === step.id
                    ? "border-accent text-accent"
                    : "border-muted-foreground text-muted-foreground"
              }`}
            >
              {currentStep > step.id ? (
                <CheckCircle className="w-5 h-5" />
              ) : (
                <span className="text-sm font-medium">{step.id}</span>
              )}
            </div>
            <div className="ml-3 hidden md:block">
              <p
                className={`text-sm font-medium ${
                  currentStep >= step.id ? "text-foreground" : "text-muted-foreground"
                }`}
              >
                {step.title}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div className={`hidden md:block w-24 h-0.5 mx-4 ${currentStep > step.id ? "bg-accent" : "bg-border"}`} />
            )}
          </div>
        ))}
      </div>

      {/* Form Content */}
      <Card>
        <CardHeader>
          <CardTitle>{steps[currentStep - 1].title}</CardTitle>
          <CardDescription>{steps[currentStep - 1].description}</CardDescription>
        </CardHeader>
        <CardContent>
          {currentStep === 1 && (
            <PersonalDetailsStep data={formData.personal} updateData={(data) => updateFormData("personal", data)} />
          )}
          {currentStep === 2 && (
            <EmploymentStep data={formData.employment} updateData={(data) => updateFormData("employment", data)} />
          )}
          {currentStep === 3 && (
            <LoanRequirementsStep data={formData.loan} updateData={(data) => updateFormData("loan", data)} />
          )}
        </CardContent>
      </Card>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between">
        <Button variant="outline" onClick={prevStep} disabled={currentStep === 1} className="gap-2 bg-transparent">
          <ChevronLeft className="w-4 h-4" />
          Previous
        </Button>

        {currentStep < steps.length ? (
          <Button onClick={nextStep} className="gap-2">
            Next
            <ChevronRight className="w-4 h-4" />
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={isSubmitting} className="gap-2">
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Submitting...
              </>
            ) : (
              <>
                Submit Application
                <CheckCircle className="w-4 h-4" />
              </>
            )}
          </Button>
        )}
      </div>
    </div>
  )
}
