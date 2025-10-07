"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { Badge } from "@/components/ui/badge"
import { Building2, Users, Briefcase, GraduationCap, Home, Tractor } from "lucide-react"

export function LoanSchemesOverview() {
  const router = useRouter();
  const schemes = [
    {
      title: "MUDRA Loan Scheme",
      description: "Micro Units Development and Refinance Agency loans for small businesses and entrepreneurs.",
      icon: Building2,
      amount: "Up to ₹10 Lakhs",
      interest: "7.5% - 12%",
      category: "Business",
      features: ["No Collateral", "Quick Processing", "Flexible Repayment"],
    },
    {
      title: "PMEGP Scheme",
      description: "Prime Minister's Employment Generation Programme for new entrepreneurs.",
      icon: Briefcase,
      amount: "Up to ₹25 Lakhs",
      interest: "8% - 10%",
      category: "Employment",
      features: ["Subsidy Available", "Training Support", "Mentorship"],
    },
    {
      title: "Education Loan Scheme",
      description: "Government-backed education loans for higher studies in India and abroad.",
      icon: GraduationCap,
      amount: "Up to ₹1.5 Crores",
      interest: "6.5% - 9.5%",
      category: "Education",
      features: ["Moratorium Period", "Tax Benefits", "No Processing Fee"],
    },
    {
      title: "PM Awas Yojana",
      description: "Pradhan Mantri Awas Yojana for affordable housing for all citizens.",
      icon: Home,
      amount: "Up to ₹12 Lakhs",
      interest: "6.5% - 8.5%",
      category: "Housing",
      features: ["Interest Subsidy", "Long Tenure", "Easy Documentation"],
    },
    {
      title: "Kisan Credit Card",
      description: "Agricultural loans for farmers to meet crop production and maintenance needs.",
      icon: Tractor,
      amount: "Based on Land Holding",
      interest: "4% - 7%",
      category: "Agriculture",
      features: ["Crop Insurance", "Flexible Repayment", "Renewal Facility"],
    },
    {
      title: "Stand-Up India",
      description: "Loans for SC/ST and women entrepreneurs for greenfield enterprises.",
      icon: Users,
      amount: "₹10 Lakhs - ₹1 Crore",
      interest: "Base Rate + 3%",
      category: "Inclusive",
      features: ["Handholding Support", "Credit Guarantee", "Skill Development"],
    },
  ]

  return (
    <section id="schemes" className="space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-3xl font-black font-serif text-foreground">Government Loan Schemes</h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Explore various government-backed loan schemes designed to support different sectors and promote inclusive
          economic growth.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {schemes.map((scheme, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow border-l-4 border-l-accent">
            <CardHeader className="pb-4">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-accent/10 rounded-lg">
                    <scheme.icon className="h-6 w-6 text-accent" />
                  </div>
                  <div>
                    <CardTitle className="text-lg font-bold">{scheme.title}</CardTitle>
                    <Badge variant="secondary" className="mt-1 text-xs">
                      {scheme.category}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground leading-relaxed">{scheme.description}</p>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Loan Amount:</span>
                  <span className="text-sm font-semibold text-accent">{scheme.amount}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Interest Rate:</span>
                  <span className="text-sm font-semibold text-accent">{scheme.interest}</span>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold">Key Features:</h4>
                <div className="flex flex-wrap gap-1">
                  {scheme.features.map((feature, idx) => (
                    <Badge key={idx} variant="outline" className="text-xs">
                      {feature}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="flex gap-2 pt-2">
                <Button
                  size="sm"
                  className="flex-1 bg-accent hover:bg-accent/90"
                  onClick={() => router.push("/login")}
                >
                  Apply Now
                </Button>
                <Button size="sm" variant="outline" className="flex-1 bg-transparent">
                  Learn More
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="text-center">
        <Button variant="outline" size="lg" className="font-semibold bg-transparent">
          View All Schemes
        </Button>
      </div>
    </section>
  )
}
