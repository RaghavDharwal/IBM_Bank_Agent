"use client"

import { Button } from "@/components/ui/button"
import { Shield, Phone, Mail, LogOut, User } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"

export function DashboardHeader() {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
    // Check if user is logged in
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    if (token && userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.push('/')
  }

  if (!isClient) {
    return null // Prevent hydration mismatch
  }
  return (
    <header className="bg-primary text-primary-foreground shadow-lg">
      {/* Top Government Bar */}
      <div className="bg-accent text-accent-foreground py-2">
        <div className="container mx-auto px-4 flex justify-between items-center text-sm">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Phone className="h-3 w-3" />
              Helpline: 1800-XXX-XXXX
            </span>
            <span className="flex items-center gap-1">
              <Mail className="h-3 w-3" />
              support@bank.in
            </span>
          </div>
          <div className="text-xs">Last Updated: {isClient ? new Date().toLocaleDateString("en-IN") : "Loading..."}</div>
        </div>
      </div>

      {/* Main Header */}
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <Shield className="h-12 w-12 text-accent" />
              <div>
                <h1 className="text-2xl font-black font-serif">Bank of India</h1>
                <p className="text-sm opacity-90">Ministry of Finance - Loan Portal</p>
              </div>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <Link href="/" className="hover:text-accent transition-colors font-medium">
              Home
            </Link>
            <a href="#schemes" className="hover:text-accent transition-colors font-medium">
              Loan Schemes
            </a>
            <a href="#eligibility" className="hover:text-accent transition-colors font-medium">
              Eligibility
            </a>
            <a href="#faq" className="hover:text-accent transition-colors font-medium">
              FAQ
            </a>
            <a href="#contact" className="hover:text-accent transition-colors font-medium">
              Contact
            </a>
            <Link href="/staff-login" className="hover:text-accent transition-colors font-medium flex items-center gap-1">
              <Shield className="h-4 w-4" />
              Staff Login
            </Link>
          </nav>

          {/* Auth Buttons */}
          <div className="flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <div className="hidden sm:flex items-center gap-2 text-sm">
                  <User className="h-4 w-4" />
                  <span>Welcome, {user.full_name}</span>
                </div>
                <Button 
                  variant="secondary" 
                  size="sm" 
                  onClick={handleLogout}
                  className="flex items-center gap-2"
                >
                  <LogOut className="h-4 w-4" />
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link href="/login">
                  <Button variant="secondary" size="sm" className="font-semibold">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="outline" size="sm" className="font-semibold">
                    Register
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Banner */}
      <div className="bg-secondary text-secondary-foreground py-2">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center gap-8 text-sm font-medium">
            <span className="text-accent">🏛️ Official Bank Portal</span>
            <span>•</span>
            <span>Secure & Verified</span>
            <span>•</span>
            <span>Digital India Initiative</span>
          </div>
        </div>
      </div>
    </header>
  )
}
