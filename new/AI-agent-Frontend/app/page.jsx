import { DashboardHeader } from "@/components/dashboard-header"
import { WelcomeSection } from "@/components/welcome-section"
import { LoanSchemesOverview } from "@/components/loan-schemes-overview"
import { FAQSection } from "@/components/faq-section"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      <main className="container mx-auto px-4 py-6 space-y-8">
        <WelcomeSection />
        <LoanSchemesOverview />
        <FAQSection />
      </main>
    </div>
  )
}
