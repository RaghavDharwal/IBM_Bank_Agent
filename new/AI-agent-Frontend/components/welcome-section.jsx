"use client"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowRight, Users, TrendingUp, Shield, Award } from "lucide-react"

export function WelcomeSection() {
  const router = useRouter();
  return (
    <section className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-6 py-12 bg-gradient-to-b from-muted/50 to-background rounded-lg">
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-black font-serif text-foreground">Bank Loan Portal</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Access loan schemes designed to empower citizens, support businesses, and drive economic
            growth across India.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button
            size="lg"
            className="bg-accent hover:bg-accent/90 text-accent-foreground font-semibold px-8"
            onClick={() => router.push("/login")}
          >
            Apply for Loan
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <Button variant="outline" size="lg" className="font-semibold px-8 bg-transparent">
            Check Eligibility
          </Button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="text-center border-l-4 border-l-accent">
          <CardContent className="pt-6">
            <Users className="h-8 w-8 text-accent mx-auto mb-2" />
            <div className="text-2xl font-bold text-foreground">50L+</div>
            <p className="text-sm text-muted-foreground">Citizens Benefited</p>
          </CardContent>
        </Card>

        <Card className="text-center border-l-4 border-l-accent">
          <CardContent className="pt-6">
            <TrendingUp className="h-8 w-8 text-accent mx-auto mb-2" />
            <div className="text-2xl font-bold text-foreground">₹2,50,000 Cr</div>
            <p className="text-sm text-muted-foreground">Loans Disbursed</p>
          </CardContent>
        </Card>

        <Card className="text-center border-l-4 border-l-accent">
          <CardContent className="pt-6">
            <Shield className="h-8 w-8 text-accent mx-auto mb-2" />
            <div className="text-2xl font-bold text-foreground">100%</div>
            <p className="text-sm text-muted-foreground">Secure Platform</p>
          </CardContent>
        </Card>

        <Card className="text-center border-l-4 border-l-accent">
          <CardContent className="pt-6">
            <Award className="h-8 w-8 text-accent mx-auto mb-2" />
            <div className="text-2xl font-bold text-foreground">25+</div>
            <p className="text-sm text-muted-foreground">Loan Schemes</p>
          </CardContent>
        </Card>
      </div>

      {/* Important Notice */}
      <Card className="bg-accent/5 border-accent/20">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <Shield className="h-6 w-6 text-accent mt-1 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-foreground mb-2">Official Government Portal</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                This is the official government portal for loan applications. All information provided is secure and
                processed through authorized government channels. Beware of fraudulent websites and always verify the
                official URL.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  )
}
