import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Calendar, FileText, IndianRupee, MapPin, Phone, User, Briefcase, CreditCard } from 'lucide-react'
import { DownloadApplication } from './download-application'

interface Application {
  id: number
  application_id: string
  personal: {
    name: string
    age: number
    gender: string
    location: string
    contact: string
  }
  employment: {
    status: string
    income: number
    credit_score: number
  }
  loan: {
    type: string
    amount: number
    tenure: string
  }
  status: string
  submitted_at: string
  admin_notes?: string
  documents_required?: string
  reviewed_at?: string
}

export function MyApplications() {
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    setIsHydrated(true)
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setError('Please login to view applications')
        return
      }

      const response = await fetch('http://localhost:5001/api/loan-applications', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const data = await response.json()
        setApplications(data.applications || [])
      } else {
        setError('Failed to fetch applications')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'bg-green-100 text-green-800 border-green-200'
      case 'rejected': return 'bg-red-100 text-red-800 border-red-200'
      case 'under_review': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'documents_pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (!isHydrated) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-gray-200 h-48 rounded-lg"></div>
          </div>
        ))}
      </div>
    )
  }

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-gray-200 h-48 rounded-lg"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Applications</h3>
        <p className="text-gray-600 mb-4">{error}</p>
        <Button onClick={fetchApplications} variant="outline">
          Try Again
        </Button>
      </div>
    )
  }

  if (applications.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Applications Found</h3>
        <p className="text-gray-600 mb-4">You haven't submitted any loan applications yet.</p>
        <Button asChild>
          <a href="/application">Apply for Loan</a>
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">My Applications</h2>
          <p className="text-gray-600">Track your loan application status and download copies</p>
        </div>
        <Badge variant="secondary" className="text-sm">
          {applications.length} Application{applications.length !== 1 ? 's' : ''}
        </Badge>
      </div>

      <div className="space-y-4">
        {applications.map((application) => (
          <Card key={application.id} className="border-l-4 border-l-blue-500">
            <CardHeader className="pb-4">
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <FileText className="h-5 w-5 text-blue-600" />
                    Application #{application.application_id}
                  </CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-1">
                    <Calendar className="h-4 w-4" />
                    Submitted on {formatDate(application.submitted_at)}
                  </CardDescription>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <Badge className={getStatusColor(application.status)}>
                    {application.status.replace('_', ' ').toUpperCase()}
                  </Badge>
                  <DownloadApplication application={application} />
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* Loan Summary */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                  <IndianRupee className="h-4 w-4" />
                  Loan Details
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-blue-600 font-medium">Type:</span>
                    <p className="text-blue-900 capitalize">{application.loan.type.replace('_', ' ')}</p>
                  </div>
                  <div>
                    <span className="text-blue-600 font-medium">Amount:</span>
                    <p className="text-blue-900 font-semibold text-lg">{formatCurrency(application.loan.amount)}</p>
                  </div>
                  <div>
                    <span className="text-blue-600 font-medium">Tenure:</span>
                    <p className="text-blue-900">{application.loan.tenure}</p>
                  </div>
                </div>
              </div>

              {/* Personal & Employment Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <User className="h-4 w-4" />
                    Personal Information
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600 w-16">Name:</span>
                      <span className="text-gray-900">{application.personal.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600 w-16">Age:</span>
                      <span className="text-gray-900">{application.personal.age} years</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-3 w-3 text-gray-400" />
                      <span className="text-gray-900">{application.personal.location}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Phone className="h-3 w-3 text-gray-400" />
                      <span className="text-gray-900">{application.personal.contact}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Briefcase className="h-4 w-4" />
                    Employment Information
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600 w-16">Status:</span>
                      <span className="text-gray-900 capitalize">{application.employment.status.replace('_', ' ')}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600 w-16">Income:</span>
                      <span className="text-gray-900">{formatCurrency(application.employment.income)}/month</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CreditCard className="h-3 w-3 text-gray-400" />
                      <span className="text-gray-900">Credit Score: {application.employment.credit_score}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Admin Notes */}
              {application.admin_notes && (
                <>
                  <Separator />
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-yellow-900 mb-2">Admin Notes</h4>
                    <p className="text-yellow-800 text-sm">{application.admin_notes}</p>
                    {application.reviewed_at && (
                      <p className="text-yellow-600 text-xs mt-2">
                        Reviewed on {formatDate(application.reviewed_at)}
                      </p>
                    )}
                  </div>
                </>
              )}

              {/* Documents Required */}
              {application.documents_required && (
                <>
                  <Separator />
                  <div className="bg-red-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-red-900 mb-2">Documents Required</h4>
                    <div className="text-red-800 text-sm whitespace-pre-line">
                      {application.documents_required}
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
