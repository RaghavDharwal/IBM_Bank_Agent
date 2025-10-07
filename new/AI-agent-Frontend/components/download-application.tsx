import React from 'react'
import { Button } from './ui/button'
import { Download, FileText } from 'lucide-react'

interface ApplicationData {
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
}

interface DownloadApplicationProps {
  application: ApplicationData
  variant?: 'default' | 'outline' | 'secondary'
  size?: 'sm' | 'default' | 'lg'
}

export function DownloadApplication({ application, variant = 'outline', size = 'sm' }: DownloadApplicationProps) {
  
  const generatePDF = () => {
    // Create HTML content for PDF
    const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Loan Application - ${application.application_id}</title>
      <style>
        body { 
          font-family: Arial, sans-serif; 
          line-height: 1.6; 
          margin: 20px;
          color: #333;
        }
        .header { 
          text-align: center; 
          border-bottom: 2px solid #1e40af; 
          padding-bottom: 20px; 
          margin-bottom: 30px;
        }
        .header h1 { 
          color: #1e40af; 
          margin: 0;
          font-size: 28px;
        }
        .header h2 { 
          color: #666; 
          margin: 5px 0 0 0;
          font-size: 16px;
          font-weight: normal;
        }
        .section { 
          margin-bottom: 25px; 
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 20px;
        }
        .section-title { 
          font-size: 18px; 
          font-weight: bold; 
          color: #1e40af; 
          margin-bottom: 15px;
          border-bottom: 1px solid #e5e7eb;
          padding-bottom: 8px;
        }
        .field { 
          display: flex; 
          margin-bottom: 10px; 
        }
        .field-label { 
          font-weight: bold; 
          width: 150px; 
          color: #374151;
        }
        .field-value { 
          flex: 1;
          color: #1f2937;
        }
        .status { 
          padding: 8px 16px; 
          border-radius: 20px; 
          font-weight: bold;
          text-align: center;
          margin: 10px 0;
        }
        .status.pending { background-color: #fef3c7; color: #92400e; }
        .status.approved { background-color: #d1fae5; color: #065f46; }
        .status.rejected { background-color: #fee2e2; color: #991b1b; }
        .status.under_review { background-color: #dbeafe; color: #1e40af; }
        .status.documents_pending { background-color: #fef3c7; color: #92400e; }
        .footer { 
          text-align: center; 
          margin-top: 40px; 
          font-size: 12px; 
          color: #6b7280;
          border-top: 1px solid #e5e7eb;
          padding-top: 20px;
        }
        .amount { 
          font-size: 20px; 
          font-weight: bold; 
          color: #059669; 
        }
        @media print {
          body { margin: 0; }
          .section { break-inside: avoid; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>🏛️ Bank of India</h1>
        <h2>Ministry of Finance - Loan Application</h2>
      </div>

      <div class="section">
        <div class="section-title">Application Details</div>
        <div class="field">
          <span class="field-label">Application ID:</span>
          <span class="field-value">${application.application_id}</span>
        </div>
        <div class="field">
          <span class="field-label">Submitted Date:</span>
          <span class="field-value">${new Date(application.submitted_at).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          })}</span>
        </div>
        <div class="field">
          <span class="field-label">Status:</span>
          <div class="status ${application.status.replace('_', ' ')}">${application.status.replace('_', ' ').toUpperCase()}</div>
        </div>
      </div>

      <div class="section">
        <div class="section-title">Personal Information</div>
        <div class="field">
          <span class="field-label">Full Name:</span>
          <span class="field-value">${application.personal.name}</span>
        </div>
        <div class="field">
          <span class="field-label">Age:</span>
          <span class="field-value">${application.personal.age} years</span>
        </div>
        <div class="field">
          <span class="field-label">Gender:</span>
          <span class="field-value">${application.personal.gender.charAt(0).toUpperCase() + application.personal.gender.slice(1)}</span>
        </div>
        <div class="field">
          <span class="field-label">Location:</span>
          <span class="field-value">${application.personal.location}</span>
        </div>
        <div class="field">
          <span class="field-label">Contact:</span>
          <span class="field-value">${application.personal.contact}</span>
        </div>
      </div>

      <div class="section">
        <div class="section-title">Employment Information</div>
        <div class="field">
          <span class="field-label">Employment Status:</span>
          <span class="field-value">${application.employment.status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
        </div>
        <div class="field">
          <span class="field-label">Monthly Income:</span>
          <span class="field-value">₹${application.employment.income.toLocaleString('en-IN')}</span>
        </div>
        <div class="field">
          <span class="field-label">Credit Score:</span>
          <span class="field-value">${application.employment.credit_score}</span>
        </div>
      </div>

      <div class="section">
        <div class="section-title">Loan Information</div>
        <div class="field">
          <span class="field-label">Loan Type:</span>
          <span class="field-value">${application.loan.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
        </div>
        <div class="field">
          <span class="field-label">Loan Amount:</span>
          <span class="field-value amount">₹${application.loan.amount.toLocaleString('en-IN')}</span>
        </div>
        <div class="field">
          <span class="field-label">Loan Tenure:</span>
          <span class="field-value">${application.loan.tenure}</span>
        </div>
      </div>

      ${application.admin_notes ? `
      <div class="section">
        <div class="section-title">Admin Notes</div>
        <div class="field-value">${application.admin_notes}</div>
      </div>
      ` : ''}

      ${application.documents_required ? `
      <div class="section">
        <div class="section-title">Documents Required</div>
        <div class="field-value">${application.documents_required}</div>
      </div>
      ` : ''}

      <div class="footer">
        <p>This is a computer-generated document. No signature is required.</p>
        <p>Bank of India | Ministry of Finance | Government of India</p>
        <p>Generated on: ${new Date().toLocaleDateString('en-IN', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })}</p>
      </div>
    </body>
    </html>
    `

    // Create a new window and print
    const printWindow = window.open('', '_blank', 'width=800,height=600')
    if (printWindow) {
      printWindow.document.write(htmlContent)
      printWindow.document.close()
      
      // Wait for content to load then trigger print
      printWindow.onload = () => {
        printWindow.print()
        // Close the window after printing (optional)
        setTimeout(() => {
          printWindow.close()
        }, 1000)
      }
    }
  }

  const downloadAsHTML = () => {
    const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Loan Application - ${application.application_id}</title>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; color: #333; }
        .header { text-align: center; border-bottom: 2px solid #1e40af; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { color: #1e40af; margin: 0; font-size: 28px; }
        .section { margin-bottom: 25px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; }
        .section-title { font-size: 18px; font-weight: bold; color: #1e40af; margin-bottom: 15px; }
        .field { display: flex; margin-bottom: 10px; }
        .field-label { font-weight: bold; width: 150px; color: #374151; }
        .field-value { flex: 1; color: #1f2937; }
        .status { padding: 8px 16px; border-radius: 20px; font-weight: bold; text-align: center; }
        .amount { font-size: 20px; font-weight: bold; color: #059669; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>🏛️ Bank of India - Loan Application</h1>
      </div>
      <div class="section">
        <div class="section-title">Application Details</div>
        <div class="field"><span class="field-label">Application ID:</span><span class="field-value">${application.application_id}</span></div>
        <div class="field"><span class="field-label">Status:</span><span class="field-value status">${application.status.toUpperCase()}</span></div>
      </div>
      <div class="section">
        <div class="section-title">Personal Information</div>
        <div class="field"><span class="field-label">Name:</span><span class="field-value">${application.personal.name}</span></div>
        <div class="field"><span class="field-label">Age:</span><span class="field-value">${application.personal.age}</span></div>
        <div class="field"><span class="field-label">Gender:</span><span class="field-value">${application.personal.gender}</span></div>
        <div class="field"><span class="field-label">Location:</span><span class="field-value">${application.personal.location}</span></div>
        <div class="field"><span class="field-label">Contact:</span><span class="field-value">${application.personal.contact}</span></div>
      </div>
      <div class="section">
        <div class="section-title">Employment Information</div>
        <div class="field"><span class="field-label">Status:</span><span class="field-value">${application.employment.status}</span></div>
        <div class="field"><span class="field-label">Income:</span><span class="field-value">₹${application.employment.income.toLocaleString()}</span></div>
        <div class="field"><span class="field-label">Credit Score:</span><span class="field-value">${application.employment.credit_score}</span></div>
      </div>
      <div class="section">
        <div class="section-title">Loan Information</div>
        <div class="field"><span class="field-label">Type:</span><span class="field-value">${application.loan.type}</span></div>
        <div class="field"><span class="field-label">Amount:</span><span class="field-value amount">₹${application.loan.amount.toLocaleString()}</span></div>
        <div class="field"><span class="field-label">Tenure:</span><span class="field-value">${application.loan.tenure}</span></div>
      </div>
    </body>
    </html>
    `

    const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `loan-application-${application.application_id}.html`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  return (
    <div className="flex gap-2">
      <Button
        variant={variant}
        size={size}
        onClick={generatePDF}
        className="flex items-center gap-2"
      >
        <Download className="h-4 w-4" />
        Download PDF
      </Button>
      <Button
        variant="outline"
        size={size}
        onClick={downloadAsHTML}
        className="flex items-center gap-2"
      >
        <FileText className="h-4 w-4" />
        HTML Copy
      </Button>
    </div>
  )
}
