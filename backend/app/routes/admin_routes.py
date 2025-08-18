# backend/app/routes/admin_routes.py

from flask import Blueprint, request, jsonify, session, redirect, render_template_string, send_from_directory, current_app
import os
import csv 

# Import all the necessary functions from our other modules
from ..utils.csv_handler import (
    verify_staff_credentials, get_all_loan_applications, get_application_documents,
    get_application_history, update_application_status, add_application_history,
    create_objection
)
from ..utils.helpers import calculate_analytics, format_currency
from ..services.notification_service import send_objection_notification

admin_bp = Blueprint('admin_bp', __name__)


# --- Admin Account and Session Routes ---

@admin_bp.route('/staff-login', methods=['POST'])
def staff_login_route():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'})

        auth_result = verify_staff_credentials(username, password)

        if auth_result['success']:
            session['staff_user'] = auth_result['user']
            session['logged_in'] = True
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'error': auth_result['error']})

    except Exception as e:
        return jsonify({'success': False, 'error': f'Login error: {str(e)}'})

@admin_bp.route('/logout')
def logout_route():
    session.clear()
    return redirect('/')


# --- Admin Dashboard and Application Management ---

@admin_bp.route('/admin-dashboard')
def admin_dashboard_route():
    if not session.get('logged_in'):
        return redirect('/staff.html') # Redirect to staff login page

    applications = get_all_loan_applications()
    analytics_data = calculate_analytics(applications)
    
# Enhanced HTML template for admin dashboard with tabs
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title data-translate="admin-dashboard">Admin Dashboard</title>
        <meta charset="UTF-8">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="scripts/language.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8fafc; }
            .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .tabs { display: flex; background: white; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .tab { padding: 15px 25px; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s; }
            .tab:hover { background: #f1f5f9; }
            .tab.active { border-bottom-color: #2563eb; background: #eff6ff; color: #2563eb; font-weight: 600; }
            .tab-content { display: none; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .tab-content.active { display: block; }
            .section { margin: 20px 0; }
            .section h2 { color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-top: 0; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #e2e8f0; padding: 12px; text-align: left; }
            th { background: #f8fafc; font-weight: 600; }
            .status-pending { background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 4px; }
            .status-approved { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; }
            .status-rejected { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; }
            .logout-btn { background: #dc2626; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .logout-btn:hover { background: #b91c1c; }
            .source-tag { font-size: 0.8em; padding: 2px 6px; border-radius: 3px; }
            .source-basic { background: #e0f2fe; color: #0277bd; }
            .source-comprehensive { background: #f3e5f5; color: #7b1fa2; }
            .action-btn { padding: 6px 12px; margin: 2px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
            .view-btn { background: #3b82f6; color: white; }
            .view-btn:hover { background: #2563eb; }
            .approve-btn { background: #10b981; color: white; }
            .approve-btn:hover { background: #059669; }
            .reject-btn { background: #ef4444; color: white; }
            .reject-btn:hover { background: #dc2626; }
            .charts-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
            .chart-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #2563eb; }
            .stat-label { color: #64748b; margin-top: 5px; }
            .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); }
            .modal-content { background: white; margin: 5% auto; padding: 20px; border-radius: 8px; width: 80%; max-width: 600px; max-height: 80vh; overflow-y: auto; }
            .modal-close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
            .modal-close:hover { color: black; }
            
            /* Filter Styles */
            .filter-container { background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e2e8f0; }
            .filter-container h3 { margin-top: 0; color: #1e293b; }
            .filter-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; align-items: end; }
            .filter-group { display: flex; flex-direction: column; }
            .filter-group label { font-weight: 600; color: #374151; margin-bottom: 5px; font-size: 0.9em; }
            .filter-group select, .filter-group input { padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 14px; }
            .filter-group select:focus, .filter-group input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
            .filter-btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; }
            .clear-btn { background: #6b7280; color: white; margin-right: 8px; }
            .clear-btn:hover { background: #4b5563; }
            .export-btn { background: #059669; color: white; }
            .export-btn:hover { background: #047857; }
            .filter-results { margin-top: 15px; font-weight: 600; color: #374151; padding: 10px; background: white; border-radius: 4px; border: 1px solid #e2e8f0; }
            .row-hidden { display: none !important; }
        </style>
    </head>
    <body>
        <div class="header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 data-translate="admin-dashboard">🏦 Banking Admin Dashboard</h1>
                    <p>Welcome, """ + session['staff_user']['username'] + """</p>
                </div>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <div class="language-selector">
                        <div class="language-dropdown">
                            <button class="language-btn" id="languageBtn" style="background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; padding: 8px 12px; border-radius: 4px; cursor: pointer;">
                                <span class="language-flag" id="currentFlag">🇺🇸</span>
                                <span class="language-text" id="currentLang">English</span>
                                <span class="dropdown-arrow">▼</span>
                            </button>
                            <div class="language-menu" id="languageMenu" style="position: absolute; top: 100%; right: 0; background: white; border: 1px solid #e2e8f0; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 1000; min-width: 120px; display: none;">
                                <div class="language-option" onclick="changeLanguage('en')" style="padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; color: #1f2937;">
                                    <span class="flag">🇺🇸</span>
                                    <span>English</span>
                                </div>
                                <div class="language-option" onclick="changeLanguage('hi')" style="padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; color: #1f2937;">
                                    <span class="flag">🇮🇳</span>
                                    <span>हिंदी</span>
                                </div>
                                <div class="language-option" onclick="changeLanguage('ta')" style="padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; color: #1f2937;">
                                    <span class="flag">🇮🇳</span>
                                    <span>தமிழ்</span>
                                </div>
                                <div class="language-option" onclick="changeLanguage('te')" style="padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; color: #1f2937;">
                                    <span class="flag">🇮🇳</span>
                                    <span>తెలుగు</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="logout-btn" onclick="location.href='/logout'" data-translate="logout">Logout</button>
                </div>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('applications')" data-translate="loan-applications">📋 Loan Applications</div>
            <div class="tab" onclick="showTab('analytics')" data-translate="analytics">📊 Analytics</div>
        </div>
        
        <div id="applications" class="tab-content active">
            <div class="section">
                <h2>📋 Loan Applications (""" + str(len(applications)) + """)</h2>
                
                <!-- Filter Controls -->
                <div class="filter-container">
                    <h3>🔍 Filter Applications</h3>
                    <div class="filter-row">
                        <div class="filter-group">
                            <label for="statusFilter">Status:</label>
                            <select id="statusFilter" onchange="applyFilters()">
                                <option value="">All Statuses</option>
                                <option value="pending">Pending</option>
                                <option value="approved">Approved</option>
                                <option value="eligibility_assessed">Assessed</option>
                                <option value="rejected">Rejected</option>
                                <option value="objection_raised">Objected</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label for="typeFilter">Loan Type:</label>
                            <select id="typeFilter" onchange="applyFilters()">
                                <option value="">All Types</option>
                                <option value="personal">Personal Loan</option>
                                <option value="home">Home Loan</option>
                                <option value="car">Car Loan</option>
                                <option value="business">Business Loan</option>
                                <option value="education">Education Loan</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label for="sourceFilter">Source:</label>
                            <select id="sourceFilter" onchange="applyFilters()">
                                <option value="">All Sources</option>
                                <option value="basic">Basic</option>
                                <option value="comprehensive">Comprehensive</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label for="amountFilter">Amount Range:</label>
                            <select id="amountFilter" onchange="applyFilters()">
                                <option value="">All Amounts</option>
                                <option value="0-50000">$0 - $50,000</option>
                                <option value="50000-100000">$50,000 - $100,000</option>
                                <option value="100000-250000">$100,000 - $250,000</option>
                                <option value="250000-500000">$250,000 - $500,000</option>
                                <option value="500000+">$500,000+</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label for="dateFilter">Date Range:</label>
                            <select id="dateFilter" onchange="applyFilters()">
                                <option value="">All Dates</option>
                                <option value="today">Today</option>
                                <option value="week">This Week</option>
                                <option value="month">This Month</option>
                                <option value="quarter">This Quarter</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label for="searchFilter">Search:</label>
                            <input type="text" id="searchFilter" placeholder="Search by ID, name, or email..." onkeyup="applyFilters()">
                        </div>
                        
                        <div class="filter-group">
                            <button class="filter-btn clear-btn" onclick="clearFilters()">Clear All</button>
                            <button class="filter-btn export-btn" onclick="exportFilteredData()">Export Filtered</button>
                        </div>
                    </div>
                    
                    <div class="filter-results">
                        <span id="filterResults">Showing all """ + str(len(applications)) + """ applications</span>
                    </div>
                </div>
                
                <table id="applicationsTable">
                    <thead>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Loan Type</th>
                            <th>Amount</th>
                            <th>Status</th>
                            <th>Type</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for app in applications:
        # Handle different status values
        status = app.get('status', 'pending')
        status_class = 'status-pending'
        if status.lower() in ['approved', 'eligibility_assessed']:
            status_class = 'status-approved'
        elif status.lower() == 'rejected':
            status_class = 'status-rejected'
        
        # Handle different source types
        source = app.get('source', 'unknown')
        source_class = f'source-{source}'
        
        # Get the display name - handle empty or missing names
        name = f"{app.get('first_name', '')} {app.get('last_name', '')}".strip()
        if not name or name == ' ':
            full_name = app.get('full_name', '')
            if full_name and full_name.strip():
                name = full_name.strip()
            else:
                # Extract name from email if no name provided
                email_user = app.get('email', app.get('user_email', '')).split('@')[0]
                name = email_user.replace('.', ' ').title() if email_user else 'N/A'
        
        # Get email
        email = app.get('email', app.get('user_email', 'N/A'))
        
        # Get loan type - handle missing loan type
        loan_type = app.get('loan_type', app.get('loanType', ''))
        if not loan_type or loan_type.strip() == '':
            loan_type = 'Not Specified'
        
        # Format amount - handle missing or empty amounts
        amount = app.get('loan_amount', app.get('loanAmount', ''))
        if amount and str(amount).strip() and str(amount).strip() != 'N/A':
            try:
                amount_val = float(str(amount).replace(',', ''))
                amount = f"${amount_val:,.0f}"
            except (ValueError, TypeError):
                amount = f"${amount}"
        else:
            amount = 'Not Specified'
        
        dashboard_html += f"""
                    <tr>
                        <td>{app.get('application_id', 'N/A')}</td>
                        <td>{name}</td>
                        <td>{email}</td>
                        <td>{loan_type}</td>
                        <td>{amount}</td>
                        <td><span class="{status_class}">{status}</span></td>
                        <td><span class="source-tag {source_class}">{source}</span></td>
                        <td>{app.get('created_at', 'N/A')[:10]}</td>
                        <td>
                            <button class="action-btn view-btn" onclick="viewApplication('{app.get('application_id', 'N/A')}')">View</button>
                            <button class="action-btn approve-btn" onclick="approveApplication('{app.get('application_id', 'N/A')}')">Approve</button>
                            <button class="action-btn reject-btn" onclick="rejectApplication('{app.get('application_id', 'N/A')}')">Reject</button>
                        </td>
                    </tr>
        """
    
    dashboard_html += """
                </tbody>
            </table>
        </div>
    </div>
    
    <div id="analytics" class="tab-content">
        <div class="section">
            <h2>� Analytics Dashboard</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">""" + str(analytics_data['total_applications']) + """</div>
                    <div class="stat-label">Total Applications</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">""" + str(analytics_data['approved_count']) + """</div>
                    <div class="stat-label">Approved</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">""" + str(analytics_data['pending_count']) + """</div>
                    <div class="stat-label">Pending</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">""" + analytics_data['avg_amount'] + """</div>
                    <div class="stat-label">Average Loan Amount</div>
                </div>
            </div>
            
            <div class="charts-container">
                <div class="chart-box">
                    <h3>Application Status Distribution</h3>
                    <canvas id="statusChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-box">
                    <h3>Loan Types Distribution</h3>
                    <canvas id="loanTypeChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Application Details Modal -->
    <div id="applicationModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modalContent">
                <!-- Application details will be loaded here -->
            </div>
        </div>
    </div>
    
    <script>
        // Tab switching functionality
        function showTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
            
            // Initialize charts if analytics tab is shown
            if (tabName === 'analytics') {
                initCharts();
            }
        }
        
        // Initialize charts
        function initCharts() {
            // Status Chart
            const statusCtx = document.getElementById('statusChart').getContext('2d');
            new Chart(statusCtx, {
                type: 'pie',
                data: {
                    labels: ['Approved', 'Pending', 'Rejected'],
                    datasets: [{
                        data: [""" + str(analytics_data['approved_count']) + """, """ + str(analytics_data['pending_count']) + """, """ + str(analytics_data['rejected_count']) + """],
                        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            
            // Loan Type Chart
            const loanTypeCtx = document.getElementById('loanTypeChart').getContext('2d');
            new Chart(loanTypeCtx, {
                type: 'doughnut',
                data: {
                    labels: """ + str(list(analytics_data['loan_types'].keys())) + """,
                    datasets: [{
                        data: """ + str(list(analytics_data['loan_types'].values())) + """,
                        backgroundColor: ['#3b82f6', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        // Application actions
        function viewApplication(appId) {
            fetch(`/view-application/${appId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('modalContent').innerHTML = data.html;
                        document.getElementById('applicationModal').style.display = 'block';
                    } else {
                        alert('Error loading application details: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error: ' + error);
                });
        }
        
        function approveApplication(appId) {
            if (confirm('Are you sure you want to approve this application?')) {
                fetch(`/approve-application/${appId}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Application approved successfully!');
                            location.reload();
                        } else {
                            alert('Error approving application: ' + data.error);
                        }
                    })
                    .catch(error => {
                        alert('Error: ' + error);
                    });
            }
        }
        
        function rejectApplication(appId) {
            if (confirm('Are you sure you want to reject this application?')) {
                fetch(`/reject-application/${appId}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Application rejected successfully!');
                            location.reload();
                        } else {
                            alert('Error rejecting application: ' + data.error);
                        }
                    })
                    .catch(error => {
                        alert('Error: ' + error);
                    });
            }
        }
        
        function closeModal() {
            document.getElementById('applicationModal').style.display = 'none';
        }
        
        // Modal tab switching
        function showModalTab(tabName, element) {
            // Hide all tab contents
            document.querySelectorAll('.modal-tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.modal-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            element.classList.add('active');
        }
        
        // View document
        function viewDocument(filePath, extension) {
            const isImage = ['jpg', 'jpeg', 'png', 'gif'].includes(extension.toLowerCase());
            const url = `/view-document/${filePath}`;
            
            if (isImage) {
                // Show image in a new modal
                const imageModal = document.createElement('div');
                imageModal.style.cssText = `
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.8); z-index: 2000; display: flex; 
                    justify-content: center; align-items: center;
                `;
                imageModal.innerHTML = `
                    <div style="max-width: 90%; max-height: 90%; position: relative;">
                        <img src="${url}" style="max-width: 100%; max-height: 100%; border-radius: 8px;" />
                        <button onclick="this.parentElement.parentElement.remove()" 
                                style="position: absolute; top: 10px; right: 10px; background: white; 
                                       border: none; border-radius: 50%; width: 30px; height: 30px; 
                                       cursor: pointer; font-size: 18px;">×</button>
                    </div>
                `;
                document.body.appendChild(imageModal);
            } else {
                // Open PDF or other documents in new tab
                window.open(url, '_blank');
            }
        }
        
        // Quick approve/reject functions
        function quickApprove(appId) {
            approveApplication(appId);
        }
        
        function quickReject(appId) {
            rejectApplication(appId);
        }
        
        // Show objection form
        function showObjectionForm(appId) {
            const form = document.createElement('div');
            form.style.cssText = `
                position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                background: rgba(0,0,0,0.5); z-index: 2000; display: flex; 
                justify-content: center; align-items: center;
            `;
            form.innerHTML = `
                <div style="background: white; padding: 30px; border-radius: 12px; max-width: 500px; width: 90%;">
                    <h3 style="margin: 0 0 20px 0; color: #dc2626;">Raise Objection</h3>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 600;">Reason for Objection:</label>
                        <textarea id="objectionReason" rows="4" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; resize: vertical;"
                                  placeholder="Please provide a detailed reason for the objection..."></textarea>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 600;">Requested Documents (comma-separated):</label>
                        <input type="text" id="requestedDocs" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"
                               placeholder="e.g., Updated Income Certificate, Bank Statements, ID Proof">
                    </div>
                    <div style="text-align: right;">
                        <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                                style="padding: 10px 20px; border: 1px solid #ddd; background: white; border-radius: 4px; margin-right: 10px; cursor: pointer;">Cancel</button>
                        <button onclick="submitObjection('${appId}', this)" 
                                style="padding: 10px 20px; background: #dc2626; color: white; border: none; border-radius: 4px; cursor: pointer;">Submit Objection</button>
                    </div>
                </div>
            `;
            document.body.appendChild(form);
        }
        
        // Submit objection
        function submitObjection(appId, button) {
            const reason = document.getElementById('objectionReason').value.trim();
            const requestedDocs = document.getElementById('requestedDocs').value.trim();
            
            if (!reason) {
                alert('Please provide a reason for the objection.');
                return;
            }
            
            button.disabled = true;
            button.textContent = 'Submitting...';
            
            fetch(`/create-objection/${appId}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    reason: reason,
                    requested_documents: requestedDocs
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Objection submitted successfully! User will be notified via email.');
                    button.parentElement.parentElement.parentElement.remove();
                    closeModal();
                    location.reload();
                } else {
                    alert('Error submitting objection: ' + data.error);
                    button.disabled = false;
                    button.textContent = 'Submit Objection';
                }
            })
            .catch(error => {
                alert('Error: ' + error);
                button.disabled = false;
                button.textContent = 'Submit Objection';
            });
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('applicationModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
        
        // Filter functionality
        let originalRows = [];
        
        // Initialize filters when page loads
        document.addEventListener('DOMContentLoaded', function() {
            const table = document.getElementById('applicationsTable');
            const tbody = table.querySelector('tbody');
            originalRows = Array.from(tbody.querySelectorAll('tr'));
        });
        
        function applyFilters() {
            const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
            const typeFilter = document.getElementById('typeFilter').value.toLowerCase();
            const sourceFilter = document.getElementById('sourceFilter').value.toLowerCase();
            const amountFilter = document.getElementById('amountFilter').value;
            const dateFilter = document.getElementById('dateFilter').value;
            const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
            
            let visibleCount = 0;
            
            originalRows.forEach(row => {
                let showRow = true;
                const cells = row.cells;
                
                // Status filter
                if (statusFilter && !cells[5].textContent.toLowerCase().includes(statusFilter)) {
                    showRow = false;
                }
                
                // Loan type filter
                if (typeFilter && !cells[3].textContent.toLowerCase().includes(typeFilter)) {
                    showRow = false;
                }
                
                // Source filter
                if (sourceFilter && !cells[6].textContent.toLowerCase().includes(sourceFilter)) {
                    showRow = false;
                }
                
                // Amount filter
                if (amountFilter && !filterByAmount(cells[4].textContent, amountFilter)) {
                    showRow = false;
                }
                
                // Date filter
                if (dateFilter && !filterByDate(cells[7].textContent, dateFilter)) {
                    showRow = false;
                }
                
                // Search filter (ID, name, and email)
                if (searchFilter) {
                    const id = cells[0].textContent.toLowerCase();
                    const name = cells[1].textContent.toLowerCase();
                    const email = cells[2].textContent.toLowerCase();
                    if (!id.includes(searchFilter) && !name.includes(searchFilter) && !email.includes(searchFilter)) {
                        showRow = false;
                    }
                }
                
                if (showRow) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // Update results count
            document.getElementById('filterResults').textContent = `Showing ${visibleCount} of ${originalRows.length} applications`;
        }
        
        function filterByAmount(amountText, range) {
            const amount = parseFloat(amountText.replace(/[$,]/g, ''));
            if (isNaN(amount)) return true; // Include if amount cannot be parsed
            
            switch(range) {
                case '0-50000': return amount <= 50000;
                case '50000-100000': return amount > 50000 && amount <= 100000;
                case '100000-250000': return amount > 100000 && amount <= 250000;
                case '250000-500000': return amount > 250000 && amount <= 500000;
                case '500000+': return amount > 500000;
                default: return true;
            }
        }
        
        function filterByDate(dateText, range) {
            const rowDate = new Date(dateText);
            const today = new Date();
            const diffTime = today - rowDate;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            switch(range) {
                case 'today': return diffDays <= 1;
                case 'week': return diffDays <= 7;
                case 'month': return diffDays <= 30;
                case 'quarter': return diffDays <= 90;
                default: return true;
            }
        }
        
        function clearFilters() {
            document.getElementById('statusFilter').value = '';
            document.getElementById('typeFilter').value = '';
            document.getElementById('sourceFilter').value = '';
            document.getElementById('amountFilter').value = '';
            document.getElementById('dateFilter').value = '';
            document.getElementById('searchFilter').value = '';
            
            // Show all rows
            originalRows.forEach(row => {
                row.style.display = '';
            });
            
            // Update results count
            document.getElementById('filterResults').textContent = `Showing all ${originalRows.length} applications`;
        }
        
        function exportFilteredData() {
            const visibleRows = originalRows.filter(row => row.style.display !== 'none');
            
            if (visibleRows.length === 0) {
                alert('No data to export');
                return;
            }
            
            // Create CSV content
            let csv = 'ID,Name,Email,Loan Type,Amount,Status,Source,Date\\n';
            
            visibleRows.forEach(row => {
                const cells = row.cells;
                const rowData = [
                    cells[0].textContent, // ID
                    cells[1].textContent, // Name
                    cells[2].textContent, // Email
                    cells[3].textContent, // Loan Type
                    cells[4].textContent, // Amount
                    cells[5].textContent.trim(), // Status (remove extra spaces)
                    cells[6].textContent.trim(), // Source
                    cells[7].textContent  // Date
                ];
                csv += rowData.map(field => `"${field.replace(/"/g, '""')}"`).join(',') + '\\n';
            });
            
            // Download CSV
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `filtered_applications_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
    </script>
    </body>
    </html>
    """
    
    # This is a truncated example. Paste your full HTML string here.
    return render_template_string(dashboard_html, applications=applications, analytics_data=analytics_data, session=session)


@admin_bp.route('/view-application/<app_id>')
def view_application_route(app_id):
    """View detailed application information with documents"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        # Get application details from both CSV files
        application = None
        
        # First check comprehensive loans
        try:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('application_id') == app_id:
                        application = row
                        break
        except FileNotFoundError:
            pass
        
        # If not found, check basic loan applications
        if not application:
            try:
                with open(current_app.config['LOAN_APPLICATIONS_CSV'], 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row.get('application_id') == app_id:
                            application = row
                            break
            except FileNotFoundError:
                pass
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'})
        
        # Get uploaded documents for this application
        documents = get_application_documents(app_id)
        
        # Get application history
        history = get_application_history(app_id)
        
        # Generate detailed HTML for modal
        html = f"""
        <div style="max-height: 80vh; overflow-y: auto;">
            <h2>Application Details - {app_id}</h2>
            
            <!-- Tab Navigation -->
            <div style="display: flex; border-bottom: 1px solid #ddd; margin-bottom: 20px;">
                <button class="modal-tab active" onclick="showModalTab('details', this)">Application Details</button>
                <button class="modal-tab" onclick="showModalTab('documents', this)">Documents ({len(documents)})</button>
                <button class="modal-tab" onclick="showModalTab('history', this)">History</button>
            </div>
            
            <!-- Application Details Tab -->
            <div id="details" class="modal-tab-content active">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h3>Personal Information</h3>
                        <p><strong>Name:</strong> {application.get('full_name', 'N/A')}</p>
                        <p><strong>Email:</strong> {application.get('user_email', application.get('email', 'N/A'))}</p>
                        <p><strong>Date of Birth:</strong> {application.get('date_of_birth', 'N/A')}</p>
                        <p><strong>Gender:</strong> {application.get('gender', 'N/A')}</p>
                        <p><strong>Marital Status:</strong> {application.get('marital_status', 'N/A')}</p>
                        <p><strong>Nationality:</strong> {application.get('nationality', 'N/A')}</p>
                        <p><strong>Contact:</strong> {application.get('contact_number', 'N/A')}</p>
                    </div>
                    <div>
                        <h3>Employment Information</h3>
                        <p><strong>Employment Type:</strong> {application.get('employment_type', 'N/A')}</p>
                        <p><strong>Employer:</strong> {application.get('employer_name', 'N/A')}</p>
                        <p><strong>Annual Income:</strong> {format_currency(application.get('annual_income', 'N/A'))}</p>
                        <p><strong>Existing Loans:</strong> {application.get('existing_loans', 'N/A')}</p>
                    </div>
                </div>
                <div style="margin-top: 20px;">
                    <h3>Loan Information</h3>
                    <p><strong>Loan Type:</strong> {application.get('loan_type', 'N/A')}</p>
                    <p><strong>Loan Amount:</strong> {format_currency(application.get('loan_amount', 'N/A'))}</p>
                    <p><strong>Loan Tenure:</strong> {application.get('loan_tenure', 'N/A')} years</p>
                    <p><strong>Loan Purpose:</strong> {application.get('loan_purpose', 'N/A')}</p>
                    <p><strong>Preferred EMI:</strong> {format_currency(application.get('preferred_emi', 'N/A'))}</p>
                    <p><strong>CIBIL Score:</strong> {application.get('cibil_score', 'N/A')}</p>
                </div>
                <div style="margin-top: 20px;">
                    <h3>Application Status</h3>
                    <p><strong>Status:</strong> {application.get('status', 'N/A')}</p>
                    <p><strong>Eligibility Status:</strong> {application.get('eligibility_status', 'N/A')}</p>
                    <p><strong>Eligibility Reason:</strong> {application.get('eligibility_reason', 'N/A')}</p>
                    <p><strong>Required Documents:</strong> {application.get('required_documents', 'N/A')}</p>
                    <p><strong>Uploaded Documents:</strong> {application.get('uploaded_documents', 'N/A')}</p>
                    <p><strong>Created At:</strong> {application.get('created_at', 'N/A')}</p>
                    <p><strong>Updated At:</strong> {application.get('updated_at', 'N/A')}</p>
                </div>
            </div>
            
            <!-- Documents Tab -->
            <div id="documents" class="modal-tab-content">
                <h3>Uploaded Documents</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">"""
        
        for doc in documents:
            file_extension = doc.get('file_name', '').split('.')[-1].lower()
            is_image = file_extension in ['jpg', 'jpeg', 'png', 'gif']
            
            html += f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; background: #f9f9f9;">
                        <h4>{doc.get('document_type', 'Unknown')}</h4>
                        <p><strong>File:</strong> {doc.get('file_name', 'N/A')}</p>
                        <p><strong>Status:</strong> <span style="color: {'green' if doc.get('verified') == 'approved' else 'orange' if doc.get('verified') == 'pending' else 'red'}">{doc.get('verified', 'pending').title()}</span></p>
                        <p><strong>Uploaded:</strong> {doc.get('uploaded_at', 'N/A')[:16].replace('T', ' ')}</p>
                        <div style="margin-top: 10px;">
                            <button class="action-btn view-btn" onclick="viewDocument('{doc.get('file_path', '')}', '{file_extension}')">View Document</button>
                        </div>
                    </div>"""
        
        if not documents:
            html += """
                    <p style="text-align: center; color: #666; font-style: italic;">No documents uploaded yet.</p>"""
        
        html += """
                </div>
            </div>
            
            <!-- History Tab -->
            <div id="history" class="modal-tab-content">
                <h3>Application History</h3>
                <div style="border-left: 3px solid #2563eb; margin-left: 10px;">"""
        
        for hist in history:
            status_color = '#10b981' if hist.get('action_type') == 'APPROVED' else '#ef4444' if hist.get('action_type') == 'REJECTED' else '#f59e0b'
            html += f"""
                    <div style="margin-left: 20px; margin-bottom: 20px; position: relative;">
                        <div style="position: absolute; left: -30px; width: 20px; height: 20px; border-radius: 50%; background: {status_color}; border: 3px solid white;"></div>
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: {status_color};">{hist.get('action_type', 'N/A')}</h4>
                            <p style="margin: 5px 0; color: #666;"><strong>By:</strong> {hist.get('action_by', 'N/A')}</p>
                            <p style="margin: 5px 0;">{hist.get('action_reason', 'No reason provided')}</p>
                            <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #888;">{hist.get('created_at', 'N/A')[:16].replace('T', ' ')}</p>
                        </div>
                    </div>"""
        
        if not history:
            html += """
                    <p style="text-align: center; color: #666; font-style: italic; margin-left: 20px;">No history available.</p>"""
        
        html += """
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center;">"""
        
        html += f"""
                <button class="action-btn approve-btn" onclick="quickApprove('{app_id}')">Quick Approve</button>
                <button class="action-btn reject-btn" onclick="quickReject('{app_id}')">Quick Reject</button>
                <button class="action-btn" style="background: #f59e0b;" onclick="showObjectionForm('{app_id}')">Raise Objection</button>
            </div>
        </div>"""
        
        return jsonify({'success': True, 'html': html})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/approve-application/<app_id>', methods=['POST'])
def approve_application_route(app_id):
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    user_email = request.json.get('user_email', '') # Get email from request if available
    updated = update_application_status(app_id, 'APPROVED', 'Application approved by admin')
    if updated:
        add_application_history(app_id, user_email, 'APPROVED', session['staff_user']['username'], 'Application approved by admin')
        # You would also trigger an approval email from the notification_service here
        return jsonify({'success': True, 'message': 'Application approved'})
    return jsonify({'success': False, 'error': 'Application not found'})


@admin_bp.route('/reject-application/<app_id>', methods=['POST'])
def reject_application_route(app_id):
    """Reject a loan application"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        updated = update_application_status(app_id, 'REJECTED', 'Application rejected by admin')
        if updated:
            # Add to history
            add_application_history(app_id, '', 'REJECTED', session['staff_user']['username'], 'Application rejected by admin')
            return jsonify({'success': True, 'message': 'Application rejected successfully'})
        else:
            return jsonify({'success': False, 'error': 'Application not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@admin_bp.route('/create-objection/<app_id>', methods=['POST'])
def create_objection_route(app_id):
    """Create objection for an application"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        data = request.json
        reason = data.get('reason', '')
        requested_docs = data.get('requested_documents', '')
        
        if not reason:
            return jsonify({'success': False, 'error': 'Reason is required'})
        
        # Get application details for email
        application = None
        try:
            with open(current_app.config['COMPREHENSIVE_LOANS_CSV'], 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('application_id') == app_id:
                        application = row
                        break
        except FileNotFoundError:
            pass
        
        if not application:
            return jsonify({'success': False, 'error': 'Application not found'})
        
        user_email = application.get('user_email', application.get('email', ''))
        objection_id = create_objection(app_id, user_email, reason, requested_docs, session['staff_user']['username'])
        
        if objection_id:
            # Send notification email to user
            send_objection_notification(user_email, app_id, reason, requested_docs)
            return jsonify({'success': True, 'message': 'Objection created successfully', 'objection_id': objection_id})
        else:
            return jsonify({'success': False, 'error': 'Failed to create objection'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


# @admin_bp.route('/view-document/<path:filename>')
# def view_document_route(filename):
#     if not session.get('logged_in'):
#         return jsonify({'success': False, 'error': 'Not authenticated'})
    
#     # This assumes the 'data/uploads' directory is inside the 'backend' folder
#     # You might need to adjust the path depending on your final structure
#     upload_folder = os.path.join(os.getcwd(), 'data', 'uploads')
#     return send_from_directory(upload_folder, filename)

@admin_bp.route('/view-document/<path:filepath>')
def view_document_route(filepath):
    """
    Securely serves an uploaded document from the data/uploads directory.
    The 'filepath' can include subdirectories, e.g., 'APP_ID/filename.pdf'.
    """
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    # current_app.root_path gives us the path to the 'backend' folder
    # This is more reliable than os.getcwd()
    uploads_directory = os.path.join(current_app.root_path, 'data', 'uploads')
    
    try:
        # send_from_directory is a secure way to send files.
        # It prevents users from accessing files outside the 'uploads_directory'.
        return send_from_directory(uploads_directory, filepath, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500