"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle, Download, Home, FileText, Clock, Phone } from "lucide-react"
import Link from "next/link"

export function SubmissionSuccess() {
  const applicationId = `LOAN-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`

  return (
    <div className="space-y-6">
      {/* Success Message */}
      <Card className="border-green-200 bg-green-50">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="flex items-center justify-center w-16 h-16 bg-green-100 rounded-full">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </div>
          <CardTitle className="text-2xl text-green-800">Application Submitted Successfully!</CardTitle>
          <CardDescription className="text-green-700">
            Your loan application has been received and is being processed
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <div className="p-4 bg-white rounded-lg border">
            <p className="text-sm text-muted-foreground mb-1">Application Reference Number</p>
            <p className="text-lg font-mono font-semibold text-foreground">{applicationId}</p>
          </div>
          <p className="text-sm text-green-700">Please save this reference number for future correspondence</p>
        </CardContent>
      </Card>

      {/* Next Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-accent" />
            What Happens Next?
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
              <div className="flex items-center justify-center w-6 h-6 bg-accent text-accent-foreground rounded-full text-xs font-semibold">
                1
              </div>
              <div>
                <p className="font-medium text-sm">Document Verification</p>
                <p className="text-xs text-muted-foreground">
                  Our team will verify your submitted information within 24-48 hours
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
              <div className="flex items-center justify-center w-6 h-6 bg-accent text-accent-foreground rounded-full text-xs font-semibold">
                2
              </div>
              <div>
                <p className="font-medium text-sm">Credit Assessment</p>
                <p className="text-xs text-muted-foreground">
                  We'll assess your eligibility and determine the best loan options for you
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
              <div className="flex items-center justify-center w-6 h-6 bg-accent text-accent-foreground rounded-full text-xs font-semibold">
                3
              </div>
              <div>
                <p className="font-medium text-sm">Loan Approval</p>
                <p className="text-xs text-muted-foreground">
                  You'll receive approval notification with loan terms within 3-7 business days
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Important Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-accent" />
            Important Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="p-3 border rounded-lg">
              <h4 className="font-medium text-sm mb-2">Processing Time</h4>
              <p className="text-xs text-muted-foreground">
                Personal Loans: 1-3 days
                <br />
                Home Loans: 7-15 days
                <br />
                Business Loans: 5-10 days
              </p>
            </div>

            <div className="p-3 border rounded-lg">
              <h4 className="font-medium text-sm mb-2">Required Documents</h4>
              <p className="text-xs text-muted-foreground">
                You may be asked to submit additional documents during the verification process
              </p>
            </div>
          </div>

          <div className="p-4 bg-accent/5 border border-accent/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Phone className="w-4 h-4 text-accent" />
              <p className="font-medium text-sm">Need Help?</p>
            </div>
            <p className="text-xs text-muted-foreground mb-3">
              Our loan experts are available to assist you with any questions about your application
            </p>
            <div className="flex gap-2">
              <Button size="sm" variant="outline" className="gap-2 bg-transparent">
                <Phone className="w-3 h-3" />
                Call Support
              </Button>
              <Button size="sm" variant="outline" className="gap-2 bg-transparent">
                <FileText className="w-3 h-3" />
                Track Application
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4">
        <Button variant="outline" className="gap-2 bg-transparent">
          <Download className="w-4 h-4" />
          Download Application Copy
        </Button>
        <Link href="/" className="flex-1">
          <Button className="w-full gap-2">
            <Home className="w-4 h-4" />
            Return to Dashboard
          </Button>
        </Link>
      </div>
    </div>
  )
}
