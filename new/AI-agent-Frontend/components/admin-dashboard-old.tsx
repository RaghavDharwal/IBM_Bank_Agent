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
                <div className="text-right">
                  <p className="text-sm font-semibold text-white">{currentUser.full_name}</p>
                  <p className="text-xs text-blue-200 flex items-center gap-1">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    Administrator
                  </p>
                </div>
              )}
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleLogout}
                className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 hover:text-white transition-all duration-200"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <Tabs defaultValue="dashboard" className="space-y-8">
          <TabsList className="bg-white/70 backdrop-blur-sm shadow-lg border border-white/20 p-1 rounded-xl">
            <TabsTrigger 
              value="dashboard" 
              className="px-6 py-3 rounded-lg font-medium transition-all duration-200 data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=active]:shadow-lg"
            >
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-current"></div>
                Dashboard
              </div>
            </TabsTrigger>
            <TabsTrigger 
              value="applications" 
              className="px-6 py-3 rounded-lg font-medium transition-all duration-200 data-[state=active]:bg-blue-600 data-[state=active]:text-white data-[state=active]:shadow-lg"
            >
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                All Applications
              </div>
            </TabsTrigger>
            <TabsTrigger 
              value="pending" 
              className="px-6 py-3 rounded-lg font-medium transition-all duration-200 data-[state=active]:bg-amber-600 data-[state=active]:text-white data-[state=active]:shadow-lg"
            >
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                Pending Review
                {stats && (stats.pending_applications + stats.under_review) > 0 && (
                  <span className="bg-amber-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center">
                    {stats.pending_applications + stats.under_review}
                  </span>
                )}
              </div>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-6">
            {/* Enhanced Stats Cards */}
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Total Applications Card */}
                <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                    <CardTitle className="text-sm font-semibold text-blue-800">Total Applications</CardTitle>
                    <div className="bg-blue-500 p-2 rounded-xl shadow-md">
                      <FileText className="h-5 w-5 text-white" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-blue-900">{stats.total_applications}</div>
                    <p className="text-xs text-blue-700 mt-1 flex items-center gap-1">
                      <span className="w-1 h-1 bg-blue-500 rounded-full"></span>
                      All loan applications
                    </p>
                  </CardContent>
                </Card>

                {/* Pending Review Card */}
                <Card className="bg-gradient-to-br from-amber-50 to-orange-100 border-amber-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                    <CardTitle className="text-sm font-semibold text-amber-800">Pending Review</CardTitle>
                    <div className="bg-amber-500 p-2 rounded-xl shadow-md animate-pulse">
                      <Clock className="h-5 w-5 text-white" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-amber-900">{stats.pending_applications + stats.under_review}</div>
                    <p className="text-xs text-amber-700 mt-1 flex items-center gap-1">
                      <span className="w-1 h-1 bg-amber-500 rounded-full animate-ping"></span>
                      Needs attention
                    </p>
                  </CardContent>
                </Card>

                {/* Approved Card */}
                <Card className="bg-gradient-to-br from-emerald-50 to-green-100 border-emerald-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                    <CardTitle className="text-sm font-semibold text-emerald-800">Approved</CardTitle>
                    <div className="bg-emerald-500 p-2 rounded-xl shadow-md">
                      <CheckCircle className="h-5 w-5 text-white" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-emerald-900">{stats.approved_applications}</div>
                    <p className="text-xs text-emerald-700 mt-1 flex items-center gap-1">
                      <span className="w-1 h-1 bg-emerald-500 rounded-full"></span>
                      Successfully processed
                    </p>
                  </CardContent>
                </Card>

                {/* Total Users Card */}
                <Card className="bg-gradient-to-br from-purple-50 to-indigo-100 border-purple-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                    <CardTitle className="text-sm font-semibold text-purple-800">Total Users</CardTitle>
                    <div className="bg-purple-500 p-2 rounded-xl shadow-md">
                      <Users className="h-5 w-5 text-white" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-purple-900">{stats.total_users}</div>
                    <p className="text-xs text-purple-700 mt-1 flex items-center gap-1">
                      <span className="w-1 h-1 bg-purple-500 rounded-full"></span>
                      Registered users
                    </p>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Enhanced Recent Applications */}
            <Card className="bg-white/80 backdrop-blur-sm shadow-xl border border-white/20">
              <CardHeader className="bg-gradient-to-r from-slate-50 to-blue-50 rounded-t-lg border-b border-slate-200/50">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-xl font-bold text-slate-800 flex items-center gap-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      Recent Applications
                    </CardTitle>
                    <CardDescription className="text-slate-600 mt-1">Latest loan applications requiring attention</CardDescription>
                  </div>
                  <div className="bg-blue-500 p-2 rounded-xl shadow-md">
                    <FileText className="h-5 w-5 text-white" />
                  </div>
                </div>
              </CardHeader>
              <CardContent className="p-6">
                {stats?.recent_applications && stats.recent_applications.length > 0 ? (
                  <div className="space-y-4">
                    {stats.recent_applications.slice(0, 5).map((app, index) => (
                      <div 
                        key={app.id} 
                        className="group flex items-center justify-between p-5 bg-gradient-to-r from-white to-slate-50 border border-slate-200/50 rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 hover:scale-[1.02] hover:border-blue-300/50"
                      >
                        <div className="flex items-center gap-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-lg">
                            {app.personal.name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <p className="font-semibold text-slate-800 group-hover:text-blue-700 transition-colors">{app.personal.name}</p>
                            <p className="text-sm text-slate-500 flex items-center gap-1">
                              <span className="w-1 h-1 bg-slate-400 rounded-full"></span>
                              ID: {app.application_id}
                            </p>
                            <p className="text-xs text-slate-400 mt-1">{formatDate(app.submitted_at)}</p>
                          </div>
                          <Badge className={`${getStatusColor(app.status)} shadow-sm font-medium`}>
                            {app.status.replace('_', ' ').toUpperCase()}
                          </Badge>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-lg text-slate-800">{formatCurrency(app.loan.amount)}</p>
                          <p className="text-sm text-slate-500 capitalize font-medium">{app.loan.type.replace('_', ' ')}</p>
                          <div className="flex items-center gap-2 mt-2">
                            <Button 
                              size="sm" 
                              variant="outline"
                              className="h-8 px-3 text-xs border-blue-200 text-blue-700 hover:bg-blue-50 hover:border-blue-300"
                              onClick={() => setSelectedApplication(app)}
                            >
                              <Eye className="h-3 w-3 mr-1" />
                              View
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  </div>
                ) : (
                  <p className="text-gray-600 text-center py-4">No recent applications</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="applications" className="space-y-6">
            {/* Enhanced Filters */}
            <Card className="bg-gradient-to-r from-blue-50 via-white to-indigo-50 border-blue-200/30 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-t-lg">
                <CardTitle className="flex items-center gap-3 text-xl font-bold">
                  <div className="bg-white/20 p-2 rounded-lg">
                    <Filter className="h-5 w-5" />
                  </div>
                  Filter Applications
                </CardTitle>
                <CardDescription className="text-blue-100 mt-2">
                  Search and filter applications by various criteria
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="search" className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                      <Search className="h-4 w-4 text-blue-500" />
                      Search
                    </Label>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                      <Input
                        id="search"
                        placeholder="Search by name, ID, email..."
                        value={filters.search}
                        onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                        className="pl-10 border-slate-300 focus:border-blue-500 focus:ring-blue-500/20 rounded-lg bg-white/80 backdrop-blur-sm"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="status-filter" className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                      <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                      Status
                    </Label>
                    <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
                      <SelectTrigger className="border-slate-300 focus:border-blue-500 focus:ring-blue-500/20 rounded-lg bg-white/80 backdrop-blur-sm">
                        <SelectValue placeholder="All statuses" />
                      </SelectTrigger>
                      <SelectContent className="bg-white/95 backdrop-blur-md border-slate-200 shadow-xl">
                        <SelectItem value="all" className="focus:bg-blue-50">All statuses</SelectItem>
                        <SelectItem value="pending" className="focus:bg-amber-50">Pending</SelectItem>
                        <SelectItem value="under_review" className="focus:bg-blue-50">Under Review</SelectItem>
                        <SelectItem value="documents_pending" className="focus:bg-orange-50">Documents Pending</SelectItem>
                        <SelectItem value="approved" className="focus:bg-green-50">Approved</SelectItem>
                        <SelectItem value="rejected" className="focus:bg-red-50">Rejected</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="loan-type-filter" className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                      <CreditCard className="h-4 w-4 text-green-500" />
                      Loan Type
                    </Label>
                    <Select value={filters.loan_type} onValueChange={(value) => setFilters(prev => ({ ...prev, loan_type: value }))}>
                      <SelectTrigger className="border-slate-300 focus:border-blue-500 focus:ring-blue-500/20 rounded-lg bg-white/80 backdrop-blur-sm">
                        <SelectValue placeholder="All types" />
                      </SelectTrigger>
                      <SelectContent className="bg-white/95 backdrop-blur-md border-slate-200 shadow-xl">
                        <SelectItem value="all" className="focus:bg-blue-50">All types</SelectItem>
                        <SelectItem value="home" className="focus:bg-blue-50">Home Loan</SelectItem>
                        <SelectItem value="personal" className="focus:bg-green-50">Personal Loan</SelectItem>
                        <SelectItem value="business" className="focus:bg-purple-50">Business Loan</SelectItem>
                        <SelectItem value="education" className="focus:bg-orange-50">Education Loan</SelectItem>
                        <SelectItem value="vehicle" className="focus:bg-red-50">Vehicle Loan</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="flex items-end">
                    <Button 
                      onClick={fetchApplications} 
                      className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 rounded-lg font-medium py-3"
                    >
                      <Filter className="h-4 w-4 mr-2" />
                      Apply Filters
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Applications List */}
            <div className="space-y-4">
              {filteredApplications.map((application) => (
                <Card key={application.id} className="border-l-4 border-l-blue-500">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-lg flex items-center gap-2">
                          <FileText className="h-5 w-5 text-blue-600" />
                          {application.personal.name} - #{application.application_id}
                        </CardTitle>
                        <CardDescription className="flex items-center gap-4 mt-1">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {formatDate(application.submitted_at)}
                          </span>
                          {application.user_details && (
                            <span className="flex items-center gap-1">
                              <User className="h-3 w-3" />
                              {application.user_details.email}
                            </span>
                          )}
                        </CardDescription>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <Badge className={getStatusColor(application.status)}>
                          {application.status.replace('_', ' ').toUpperCase()}
                        </Badge>
                        <div className="flex gap-2">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm">
                                <Eye className="h-4 w-4 mr-1" />
                                View
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
                              <DialogHeader>
                                <DialogTitle>Application Details - {application.application_id}</DialogTitle>
                                <DialogDescription>
                                  Complete application information and user details
                                </DialogDescription>
                              </DialogHeader>
                              
                              <div className="space-y-6">
                                {/* Personal Info */}
                                <div>
                                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                    <User className="h-4 w-4" />
                                    Personal Information
                                  </h4>
                                  <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div><span className="font-medium">Name:</span> {application.personal.name}</div>
                                    <div><span className="font-medium">Age:</span> {application.personal.age} years</div>
                                    <div><span className="font-medium">Gender:</span> {application.personal.gender}</div>
                                    <div><span className="font-medium">Location:</span> {application.personal.location}</div>
                                    <div><span className="font-medium">Contact:</span> {application.personal.contact}</div>
                                  </div>
                                </div>

                                <Separator />

                                {/* Employment Info */}
                                <div>
                                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                    <Briefcase className="h-4 w-4" />
                                    Employment Information
                                  </h4>
                                  <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div><span className="font-medium">Status:</span> {application.employment.status.replace('_', ' ')}</div>
                                    <div><span className="font-medium">Monthly Income:</span> {formatCurrency(application.employment.income)}</div>
                                    <div><span className="font-medium">Credit Score:</span> {application.employment.credit_score}</div>
                                  </div>
                                </div>

                                <Separator />

                                {/* Loan Info */}
                                <div>
                                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                    <IndianRupee className="h-4 w-4" />
                                    Loan Information
                                  </h4>
                                  <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div><span className="font-medium">Type:</span> {application.loan.type.replace('_', ' ')}</div>
                                    <div><span className="font-medium">Amount:</span> <span className="text-lg font-bold text-green-600">{formatCurrency(application.loan.amount)}</span></div>
                                    <div><span className="font-medium">Tenure:</span> {application.loan.tenure}</div>
                                  </div>
                                </div>

                                {application.admin_notes && (
                                  <>
                                    <Separator />
                                    <div>
                                      <h4 className="font-semibold text-gray-900 mb-2">Admin Notes</h4>
                                      <p className="text-sm bg-gray-50 p-3 rounded">{application.admin_notes}</p>
                                    </div>
                                  </>
                                )}

                                {application.documents_required && (
                                  <>
                                    <Separator />
                                    <div>
                                      <h4 className="font-semibold text-gray-900 mb-2">Documents Required</h4>
                                      <pre className="text-sm bg-yellow-50 p-3 rounded whitespace-pre-wrap">{application.documents_required}</pre>
                                    </div>
                                  </>
                                )}
                              </div>
                            </DialogContent>
                          </Dialog>

                          {application.status === 'pending' || application.status === 'under_review' ? (
                            <>
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => {
                                  setActionDialog({ open: true, type: 'documents', application })
                                  setActionForm({ status: '', admin_notes: '', documents_required: '' })
                                }}
                              >
                                <MessageSquare className="h-4 w-4 mr-1" />
                                Request Docs
                              </Button>
                              
                              <Button 
                                variant="default" 
                                size="sm"
                                onClick={() => {
                                  setActionDialog({ open: true, type: 'approve', application })
                                  setActionForm({ status: '', admin_notes: '', documents_required: '' })
                                }}
                              >
                                <CheckCircle className="h-4 w-4 mr-1" />
                                Approve
                              </Button>
                              
                              <Button 
                                variant="destructive" 
                                size="sm"
                                onClick={() => {
                                  setActionDialog({ open: true, type: 'reject', application })
                                  setActionForm({ status: '', admin_notes: '', documents_required: '' })
                                }}
                              >
                                <XCircle className="h-4 w-4 mr-1" />
                                Reject
                              </Button>
                            </>
                          ) : (
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => {
                                setActionDialog({ open: true, type: 'status', application })
                                setActionForm({ status: application.status, admin_notes: application.admin_notes || '', documents_required: '' })
                              }}
                            >
                              Update Status
                            </Button>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-blue-50 p-3 rounded-lg">
                        <p className="text-sm text-blue-600 font-medium">Loan Details</p>
                        <p className="text-blue-900 font-semibold">{formatCurrency(application.loan.amount)}</p>
                        <p className="text-blue-700 text-sm capitalize">{application.loan.type.replace('_', ' ')} - {application.loan.tenure}</p>
                      </div>
                      
                      <div className="bg-green-50 p-3 rounded-lg">
                        <p className="text-sm text-green-600 font-medium">Income & Credit</p>
                        <p className="text-green-900 font-semibold">{formatCurrency(application.employment.income)}/month</p>
                        <p className="text-green-700 text-sm">Credit Score: {application.employment.credit_score}</p>
                      </div>
                      
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="text-sm text-gray-600 font-medium">Contact</p>
                        <p className="text-gray-900 font-semibold">{application.personal.contact}</p>
                        <p className="text-gray-700 text-sm">{application.personal.location}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}

              {filteredApplications.length === 0 && !loading && (
                <Card>
                  <CardContent className="text-center py-12">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">No Applications Found</h3>
                    <p className="text-gray-600">No applications match your current filters.</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          <TabsContent value="pending">
            <Card>
              <CardHeader>
                <CardTitle>Applications Pending Review</CardTitle>
                <CardDescription>Applications that require immediate attention</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {applications
                    .filter(app => app.status === 'pending' || app.status === 'under_review')
                    .map((application) => (
                      <div key={application.id} className="flex items-center justify-between p-4 border rounded-lg bg-yellow-50 border-yellow-200">
                        <div className="flex items-center gap-4">
                          <div>
                            <p className="font-medium">{application.personal.name}</p>
                            <p className="text-sm text-gray-600">ID: {application.application_id}</p>
                            <p className="text-sm text-gray-600">Submitted: {formatDate(application.submitted_at)}</p>
                          </div>
                          <Badge className={getStatusColor(application.status)}>
                            {application.status.replace('_', ' ').toUpperCase()}
                          </Badge>
                        </div>
                        <div className="text-right">
                          <p className="font-medium">{formatCurrency(application.loan.amount)}</p>
                          <p className="text-sm text-gray-600 capitalize">{application.loan.type.replace('_', ' ')}</p>
                          <div className="flex gap-2 mt-2">
                            <Button 
                              size="sm" 
                              onClick={() => {
                                setActionDialog({ open: true, type: 'approve', application })
                                setActionForm({ status: '', admin_notes: '', documents_required: '' })
                              }}
                            >
                              Approve
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline"
                              onClick={() => {
                                setActionDialog({ open: true, type: 'documents', application })
                                setActionForm({ status: '', admin_notes: '', documents_required: '' })
                              }}
                            >
                              Request Docs
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}

                  {applications.filter(app => app.status === 'pending' || app.status === 'under_review').length === 0 && (
                    <div className="text-center py-8">
                      <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">All Caught Up!</h3>
                      <p className="text-gray-600">No applications are currently pending review.</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Enhanced Action Dialog */}
        <Dialog open={actionDialog.open} onOpenChange={(open) => setActionDialog(prev => ({ ...prev, open }))}>
          <DialogContent className="sm:max-w-[500px] p-0 overflow-hidden">
            {/* Modern Header with Gradient */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 text-white">
              <DialogHeader>
                <DialogTitle className="text-xl font-semibold flex items-center gap-2">
                  {actionDialog.type === 'approve' && (
                    <>
                      <CheckCircle className="h-5 w-5" />
                      Approve Application
                    </>
                  )}
                  {actionDialog.type === 'reject' && (
                    <>
                      <XCircle className="h-5 w-5" />
                      Reject Application
                    </>
                  )}
                  {actionDialog.type === 'documents' && (
                    <>
                      <FileText className="h-5 w-5" />
                      Request Documents
                    </>
                  )}
                  {actionDialog.type === 'status' && (
                    <>
                      <Clock className="h-5 w-5" />
                      Update Application Status
                    </>
                  )}
                </DialogTitle>
                <DialogDescription className="text-blue-100 mt-1">
                  {actionDialog.application && (
                    <div className="flex items-center gap-2">
                      <User className="h-4 w-4" />
                      <span>Application #{actionDialog.application.application_id} - {actionDialog.application.personal.name}</span>
                    </div>
                  )}
                </DialogDescription>
              </DialogHeader>
            </div>

            {/* Enhanced Content Area */}
            <div className="p-6 space-y-6">
              {/* Application Summary Card */}
              {actionDialog.application && (
                <div className="bg-gradient-to-r from-gray-50 to-blue-50 p-4 rounded-lg border">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600 font-medium">Loan Amount:</span>
                      <p className="font-bold text-blue-700">{formatCurrency(actionDialog.application.loan.amount)}</p>
                    </div>
                    <div>
                      <span className="text-gray-600 font-medium">Loan Type:</span>
                      <p className="font-semibold capitalize">{actionDialog.application.loan.type.replace('_', ' ')}</p>
                    </div>
                    <div>
                      <span className="text-gray-600 font-medium">Current Status:</span>
                      <Badge className={getStatusColor(actionDialog.application.status)} variant="secondary">
                        {actionDialog.application.status.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </div>
                    <div>
                      <span className="text-gray-600 font-medium">Submitted:</span>
                      <p className="font-medium">{formatDate(actionDialog.application.submitted_at)}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Form Fields */}
              <div className="space-y-4">
                {actionDialog.type === 'status' && (
                  <div className="space-y-2">
                    <Label htmlFor="status" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4" />
                      New Status
                    </Label>
                    <Select value={actionForm.status} onValueChange={(value) => setActionForm(prev => ({ ...prev, status: value }))}>
                      <SelectTrigger className="h-11 border-2 border-gray-200 hover:border-blue-300 transition-colors">
                        <SelectValue placeholder="Select new status" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pending">
                          <div className="flex items-center gap-2">
                            <Clock className="h-4 w-4 text-yellow-500" />
                            Pending
                          </div>
                        </SelectItem>
                        <SelectItem value="under_review">
                          <div className="flex items-center gap-2">
                            <Eye className="h-4 w-4 text-blue-500" />
                            Under Review
                          </div>
                        </SelectItem>
                        <SelectItem value="documents_pending">
                          <div className="flex items-center gap-2">
                            <FileText className="h-4 w-4 text-orange-500" />
                            Documents Pending
                          </div>
                        </SelectItem>
                        <SelectItem value="approved">
                          <div className="flex items-center gap-2">
                            <CheckCircle className="h-4 w-4 text-green-500" />
                            Approved
                          </div>
                        </SelectItem>
                        <SelectItem value="rejected">
                          <div className="flex items-center gap-2">
                            <XCircle className="h-4 w-4 text-red-500" />
                            Rejected
                          </div>
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}

                {actionDialog.type === 'documents' && (
                  <div className="space-y-2">
                    <Label htmlFor="documents" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      Documents Required
                    </Label>
                    <Textarea
                      id="documents"
                      placeholder="List the documents that need to be submitted (e.g., Income proof, Bank statements, Identity verification...)"
                      value={actionForm.documents_required}
                      onChange={(e) => setActionForm(prev => ({ ...prev, documents_required: e.target.value }))}
                      rows={4}
                      className="border-2 border-gray-200 hover:border-blue-300 focus:border-blue-500 transition-colors resize-none"
                    />
                  </div>
                )}

                <div className="space-y-2">
                  <Label htmlFor="notes" className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <MessageSquare className="h-4 w-4" />
                    Admin Notes
                  </Label>
                  <Textarea
                    id="notes"
                    placeholder="Add your comments, feedback, or notes about this decision..."
                    value={actionForm.admin_notes}
                    onChange={(e) => setActionForm(prev => ({ ...prev, admin_notes: e.target.value }))}
                    rows={3}
                    className="border-2 border-gray-200 hover:border-blue-300 focus:border-blue-500 transition-colors resize-none"
                  />
                </div>
              </div>
            </div>

            {/* Enhanced Footer */}
            <div className="bg-gray-50 px-6 py-4 flex justify-end gap-3 border-t">
              <Button 
                variant="outline" 
                onClick={() => setActionDialog(prev => ({ ...prev, open: false }))}
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
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
