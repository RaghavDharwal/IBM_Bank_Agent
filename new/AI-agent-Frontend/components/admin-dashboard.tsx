"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import { 
  Users, 
  FileText, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertTriangle,
  Shield,
  Download,
  LogOut,
  Search,
  Filter,
  Eye,
  MessageSquare,
  Send,
  Calendar,
  IndianRupee,
  MapPin,
  Phone,
  User,
  Briefcase,
  CreditCard
} from 'lucide-react'
import { useRouter } from 'next/navigation'

interface Application {
  id: number
  application_id: string
  user_id: number
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
  user_details?: {
    id: number
    full_name: string
    email: string
    phone: string
    aadhaar: string
    role: string
  }
}

interface DashboardStats {
  total_applications: number
  pending_applications: number
  under_review: number
  documents_pending: number
  approved_applications: number
  rejected_applications: number
  total_users: number
  recent_applications: Application[]
}

export function AdminDashboard() {
  const router = useRouter()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null)
  const [isHydrated, setIsHydrated] = useState(false)
  const [actionDialog, setActionDialog] = useState<{
    open: boolean
    type: 'approve' | 'reject' | 'documents' | 'status'
    application: Application | null
  }>({
    open: false,
    type: 'approve',
    application: null
  })
  const [actionForm, setActionForm] = useState({
    status: '',
    admin_notes: '',
    documents_required: ''
  })
  const [filters, setFilters] = useState({
    status: 'all',
    loan_type: 'all',
    search: ''
  })
  const [currentUser, setCurrentUser] = useState<any>(null)

  useEffect(() => {
    // Mark as hydrated first
    setIsHydrated(true)
    
    // Check admin authentication only on client side
    if (typeof window === 'undefined') return
    
    const token = localStorage.getItem('admin_token')
    const user = localStorage.getItem('admin_user')
    
    if (!token || !user) {
      router.push('/staff-login')
      return
    }

    try {
      const userData = JSON.parse(user)
      if (userData.role !== 'admin') {
        router.push('/staff-login')
        return
      }

      setCurrentUser(userData)
      fetchDashboardStats()
      fetchApplications()
    } catch (e) {
      console.error('Error parsing user data:', e)
      router.push('/staff-login')
    }
  }, [router])

  const getAuthHeaders = (): HeadersInit => {
    if (typeof window === 'undefined') {
      return {
        'Content-Type': 'application/json'
      }
    }
    
    const token = localStorage.getItem('admin_token')
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/admin/dashboard-stats', {
        headers: getAuthHeaders()
      })
      
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      } else {
        setError('Failed to fetch dashboard statistics')
      }
    } catch (err) {
      setError('Network error fetching statistics')
    }
  }

  const fetchApplications = async () => {
    try {
      const queryParams = new URLSearchParams()
      if (filters.status && filters.status !== 'all') queryParams.append('status', filters.status)
      if (filters.loan_type && filters.loan_type !== 'all') queryParams.append('loan_type', filters.loan_type)
      
      const response = await fetch(`http://localhost:5001/api/admin/applications?${queryParams}`, {
        headers: getAuthHeaders()
      })
      
      if (response.ok) {
        const data = await response.json()
        setApplications(data.applications || [])
      } else {
        setError('Failed to fetch applications')
      }
    } catch (err) {
      setError('Network error fetching applications')
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async () => {
    if (!actionDialog.application) return

    try {
      let endpoint = ''
      let payload = {}

      switch (actionDialog.type) {
        case 'approve':
        case 'reject':
          endpoint = `http://localhost:5001/api/admin/applications/${actionDialog.application.id}/approve`
          payload = {
            status: actionDialog.type === 'approve' ? 'approved' : 'rejected',
            admin_notes: actionForm.admin_notes
          }
          break
        case 'documents':
          endpoint = `http://localhost:5001/api/admin/applications/${actionDialog.application.id}/request-documents`
          payload = {
            documents_required: actionForm.documents_required,
            admin_notes: actionForm.admin_notes
          }
          break
        case 'status':
          endpoint = `http://localhost:5001/api/admin/applications/${actionDialog.application.id}/update-status`
          payload = {
            status: actionForm.status,
            admin_notes: actionForm.admin_notes
          }
          break
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(payload)
      })

      if (response.ok) {
        // Refresh applications and stats
        await fetchApplications()
        await fetchDashboardStats()
        
        // Close dialog and reset form
        setActionDialog({ open: false, type: 'approve', application: null })
        setActionForm({ status: '', admin_notes: '', documents_required: '' })
      } else {
        const data = await response.json()
        setError(data.message || 'Action failed')
      }
    } catch (err) {
      setError('Network error performing action')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    router.push('/staff-login')
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
    // Use a consistent, hydration-safe date format
    if (!isHydrated) {
      return dateString // Return raw string during SSR
    }
    
    try {
      return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (e) {
      return dateString // Fallback to original string if parsing fails
    }
  }

  const filteredApplications = applications.filter(app => {
    if (filters.search) {
      const searchLower = filters.search.toLowerCase()
      return (
        app.application_id.toLowerCase().includes(searchLower) ||
        app.personal.name.toLowerCase().includes(searchLower) ||
        app.user_details?.email.toLowerCase().includes(searchLower)
      )
    }
    return true
  })

  // Prevent hydration mismatch by not rendering until hydrated
  if (!isHydrated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (loading && !stats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading admin dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Enhanced Header */}
      <header className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 shadow-xl border-b border-blue-300/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center gap-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-3 shadow-lg">
                <Shield className="h-10 w-10 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white tracking-tight">Admin Dashboard</h1>
                <p className="text-blue-100 text-sm font-medium">Bank of India - Loan Management System</p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              {currentUser && (
                <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-xl px-4 py-2">
                  <div className="h-8 w-8 bg-white/20 rounded-full flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                  <div className="text-right">
                    <p className="text-white font-medium text-sm">{currentUser.full_name}</p>
                    <p className="text-blue-100 text-xs">Administrator</p>
                  </div>
                </div>
              )}
              <Button 
                onClick={handleLogout}
                className="bg-white/10 hover:bg-white/20 text-white border border-white/20 backdrop-blur-sm"
                size="sm"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Enhanced Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-700">Total Applications</p>
                  <p className="text-3xl font-bold text-blue-900">{stats?.total_applications || 0}</p>
                </div>
                <div className="h-12 w-12 bg-blue-500 rounded-xl flex items-center justify-center">
                  <FileText className="h-6 w-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-green-700">Approved</p>
                  <p className="text-3xl font-bold text-green-900">{stats?.approved_applications || 0}</p>
                </div>
                <div className="h-12 w-12 bg-green-500 rounded-xl flex items-center justify-center">
                  <CheckCircle className="h-6 w-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-orange-700">Pending Review</p>
                  <p className="text-3xl font-bold text-orange-900">{stats?.under_review || 0}</p>
                </div>
                <div className="h-12 w-12 bg-orange-500 rounded-xl flex items-center justify-center">
                  <Clock className="h-6 w-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-700">Total Users</p>
                  <p className="text-3xl font-bold text-purple-900">{stats?.total_users || 0}</p>
                </div>
                <div className="h-12 w-12 bg-purple-500 rounded-xl flex items-center justify-center">
                  <Users className="h-6 w-6 text-white" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Enhanced Filters Section */}
        <Card className="mb-8 bg-white/80 backdrop-blur-sm border border-gray-200/50 shadow-lg">
          <CardHeader className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200/50">
            <div className="flex items-center gap-3">
              <Filter className="h-5 w-5 text-gray-600" />
              <CardTitle className="text-lg font-semibold text-gray-800">Application Filters</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="p-6">
            <div className="flex flex-wrap gap-4">
              <div className="flex-1 min-w-[200px]">
                <Label htmlFor="search" className="text-sm font-medium text-gray-700 mb-2 block">Search</Label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <Input
                    id="search"
                    type="text"
                    placeholder="Search by ID, name, or email..."
                    value={filters.search}
                    onChange={(e) => setFilters({...filters, search: e.target.value})}
                    className="pl-10 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="min-w-[150px]">
                <Label htmlFor="status-filter" className="text-sm font-medium text-gray-700 mb-2 block">Status</Label>
                <Select value={filters.status} onValueChange={(value) => setFilters({...filters, status: value})}>
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="All Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="under_review">Under Review</SelectItem>
                    <SelectItem value="documents_pending">Documents Pending</SelectItem>
                    <SelectItem value="approved">Approved</SelectItem>
                    <SelectItem value="rejected">Rejected</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="min-w-[150px]">
                <Label htmlFor="loan-type-filter" className="text-sm font-medium text-gray-700 mb-2 block">Loan Type</Label>
                <Select value={filters.loan_type} onValueChange={(value) => setFilters({...filters, loan_type: value})}>
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="All Types" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="personal">Personal Loan</SelectItem>
                    <SelectItem value="home">Home Loan</SelectItem>
                    <SelectItem value="education">Education Loan</SelectItem>
                    <SelectItem value="business">Business Loan</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Enhanced Applications List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredApplications.map((app) => (
            <Card key={app.id} className="bg-white/90 backdrop-blur-sm border border-gray-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02]">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg font-semibold text-gray-800">{app.personal.name}</CardTitle>
                    <CardDescription className="text-sm text-gray-600">{app.application_id}</CardDescription>
                  </div>
                  <Badge className={`${getStatusColor(app.status)} shadow-sm font-medium`}>
                    {app.status.replace('_', ' ')}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="flex items-center gap-2">
                    <CreditCard className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-600">{app.loan.type}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <IndianRupee className="h-4 w-4 text-gray-500" />
                    <span className="font-medium text-gray-800">{formatCurrency(app.loan.amount)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-600">{app.personal.location}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-600">{app.personal.contact}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Briefcase className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-600">{app.employment.status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-600">{formatDate(app.submitted_at)}</span>
                  </div>
                </div>
                
                <Separator />
                
                <div className="flex gap-2">
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setSelectedApplication(app)}
                    className="flex-1 bg-blue-50 border-blue-200 text-blue-700 hover:bg-blue-100"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    View
                  </Button>
                  
                  {app.status === 'pending' || app.status === 'under_review' ? (
                    <>
                      <Button 
                        size="sm"
                        onClick={() => setActionDialog({ open: true, type: 'approve', application: app })}
                        className="bg-green-600 hover:bg-green-700 text-white flex-1"
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Approve
                      </Button>
                      <Button 
                        size="sm" 
                        variant="destructive"
                        onClick={() => setActionDialog({ open: true, type: 'reject', application: app })}
                        className="flex-1"
                      >
                        <XCircle className="h-4 w-4 mr-1" />
                        Reject
                      </Button>
                    </>
                  ) : (
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => setActionDialog({ open: true, type: 'documents', application: app })}
                      className="flex-1 bg-yellow-50 border-yellow-200 text-yellow-700 hover:bg-yellow-100"
                    >
                      <MessageSquare className="h-4 w-4 mr-1" />
                      Message
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredApplications.length === 0 && (
          <Card className="bg-white/80 backdrop-blur-sm">
            <CardContent className="text-center py-12">
              <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">No applications found</h3>
              <p className="text-gray-500">Try adjusting your filters to see more results.</p>
            </CardContent>
          </Card>
        )}

        {/* Enhanced Action Dialog */}
        <Dialog open={actionDialog.open} onOpenChange={(open) => setActionDialog({...actionDialog, open})}>
          <DialogContent className="max-w-2xl bg-white/95 backdrop-blur-sm">
            <DialogHeader className={`rounded-lg p-4 mb-4 ${
              actionDialog.type === 'approve' ? 'bg-gradient-to-r from-green-500 to-green-600' :
              actionDialog.type === 'reject' ? 'bg-gradient-to-r from-red-500 to-red-600' :
              'bg-gradient-to-r from-blue-500 to-blue-600'
            }`}>
              <DialogTitle className="text-white text-lg font-semibold flex items-center gap-2">
                {actionDialog.type === 'approve' && <CheckCircle className="h-5 w-5" />}
                {actionDialog.type === 'reject' && <XCircle className="h-5 w-5" />}
                {actionDialog.type === 'documents' && <MessageSquare className="h-5 w-5" />}
                {actionDialog.type === 'status' && <AlertTriangle className="h-5 w-5" />}
                {actionDialog.type === 'approve' && 'Approve Application'}
                {actionDialog.type === 'reject' && 'Reject Application'}
                {actionDialog.type === 'documents' && 'Send Document Request'}
                {actionDialog.type === 'status' && 'Update Application Status'}
              </DialogTitle>
              <DialogDescription className="text-blue-100">
                {actionDialog.application && (
                  <div className="mt-2 bg-white/10 rounded-lg p-3">
                    <p className="font-medium">{actionDialog.application.personal.name}</p>
                    <p className="text-sm opacity-90">{actionDialog.application.application_id}</p>
                  </div>
                )}
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4">
              {actionDialog.type === 'status' && (
                <div>
                  <Label htmlFor="status">New Status</Label>
                  <Select value={actionForm.status} onValueChange={(value) => setActionForm({...actionForm, status: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="under_review">Under Review</SelectItem>
                      <SelectItem value="documents_pending">Documents Pending</SelectItem>
                      <SelectItem value="approved">Approved</SelectItem>
                      <SelectItem value="rejected">Rejected</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              )}

              {actionDialog.type === 'documents' && (
                <div>
                  <Label htmlFor="documents">Required Documents</Label>
                  <Textarea
                    id="documents"
                    placeholder="List the documents required from the applicant..."
                    value={actionForm.documents_required}
                    onChange={(e) => setActionForm({...actionForm, documents_required: e.target.value})}
                    className="min-h-[100px]"
                  />
                </div>
              )}

              <div>
                <Label htmlFor="admin-notes">Admin Notes</Label>
                <Textarea
                  id="admin-notes"
                  placeholder="Add any notes or comments for this action..."
                  value={actionForm.admin_notes}
                  onChange={(e) => setActionForm({...actionForm, admin_notes: e.target.value})}
                  className="min-h-[100px]"
                />
              </div>
            </div>

            <DialogFooter className="gap-2 mt-6">
              <Button 
                variant="outline" 
                onClick={() => setActionDialog({ open: false, type: 'approve', application: null })}
                className="px-6 hover:bg-gray-100 border-gray-300"
              >
                Cancel
              </Button>
              <Button 
                onClick={handleAction}
                className={`px-6 flex items-center gap-2 font-semibold ${actionDialog.type === 'approve' ? 'bg-green-600 hover:bg-green-700' : actionDialog.type === 'reject' ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'}`}
              >
                <Send className="h-4 w-4" />
                {actionDialog.type === 'approve' && 'Approve Application'}
                {actionDialog.type === 'reject' && 'Reject Application'}
                {actionDialog.type === 'documents' && 'Send Document Request'}
                {actionDialog.type === 'status' && 'Update Status'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}