"use client"
import { DashboardHeader } from "@/components/dashboard-header"
import { LoanApplicationForm } from "@/components/loan-application-form"
import { AISuggestionsPanel } from "@/components/ai-suggestions-panel"
import { FAQSection } from "@/components/faq-section"
import { MyApplications } from "@/components/my-applications"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Plus, FileText } from "lucide-react"
import type { FormData } from "@/components/loan-application-form"

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

export default function ApplicationPage() {
  const router = useRouter()
  const [formData, setFormData] = useState<FormData>(initialFormData)
  const [currentStep, setCurrentStep] = useState(1)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isHydrated, setIsHydrated] = useState(false)
  const [activeTab, setActiveTab] = useState("applications")

  useEffect(() => {
    // Mark as hydrated first
    setIsHydrated(true)
    
    // Check authentication
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }
    
    setIsAuthenticated(true)
    setIsLoading(false)
  }, [router])

  // Prevent hydration mismatch by not rendering until hydrated
  if (!isHydrated) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      <main className="container mx-auto px-4 py-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-semibold text-foreground mb-2">Loan Portal</h1>
            <p className="text-muted-foreground">Manage your loan applications and apply for new loans</p>
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 max-w-md">
              <TabsTrigger value="applications" className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                My Applications
              </TabsTrigger>
              <TabsTrigger value="new-application" className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                New Application
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="applications" className="mt-8">
              <MyApplications />
            </TabsContent>
            
            <TabsContent value="new-application" className="mt-8">
              <div className="grid gap-8 lg:grid-cols-3">
                <div className="lg:col-span-2 space-y-8">
                  <LoanApplicationForm
                    formData={formData}
                    setFormData={setFormData}
                    currentStep={currentStep}
                    setCurrentStep={setCurrentStep}
                    onSuccess={() => setActiveTab("applications")}
                  />
                  <FAQSection />
                </div>
                <div className="lg:col-span-1">
                  <AISuggestionsPanel formData={formData} currentStep={currentStep} />
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}
