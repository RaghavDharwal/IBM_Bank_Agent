let currentUser = null;

// Immediately clear staff sessions when page loads (before checking auth)
document.addEventListener("DOMContentLoaded", function () {
  // Clear staff sessions aggressively on page load
  clearStaffSession();
  // Wait a moment then check auth status
  setTimeout(checkAuthStatus, 500);
});

// Also clear on page visibility change (when user returns to tab)
document.addEventListener("visibilitychange", function () {
  if (!document.hidden) {
    clearStaffSession();
    setTimeout(checkAuthStatus, 200);
  }
});

function switchAuthTab(tab) {
  // Update tab buttons
  document
    .querySelectorAll(".auth-tab")
    .forEach((t) => t.classList.remove("active"));
  event.target.classList.add("active");

  // Update forms
  document
    .querySelectorAll(".auth-form")
    .forEach((f) => f.classList.remove("active"));
  document.getElementById(tab + "Form").classList.add("active");
}

function showAlert(message, type, container = "auth") {
  const alertId =
    container +
    (type === "error" ? "Error" : type === "success" ? "Success" : "Info");
  const alert = document.getElementById(alertId);
  alert.textContent = message;
  alert.style.display = "block";

  setTimeout(() => {
    alert.style.display = "none";
  }, 5000);
}

function checkAuthStatus() {
  // Automatically clear any staff session when accessing user interface
  clearStaffSession();

  // Check user session with server
  fetch("/user-auth-status", {
    credentials: "include", // Include cookies for session management
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.logged_in) {
        currentUser = { email: data.email };
        showUserLoggedIn();
        // Hide any auth warnings since we've cleared conflicts
        hideAuthWarning();
      } else {
        // Clear local storage if server session is invalid
        localStorage.removeItem("currentUser");
        hideAuthWarning();
      }
    })
    .catch(() => {
      // Fallback to localStorage for demo
      const savedUser = localStorage.getItem("currentUser");
      if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showUserLoggedIn();
      }
      hideAuthWarning();
    });
}

function checkConflictingSessions() {
  // Check if staff is logged in
  fetch("/admin-dashboard")
    .then((response) => {
      if (response.ok) {
        showAuthWarning(
          "⚠️ Staff session detected. You are currently logged in as admin staff."
        );
      }
    })
    .catch(() => {});
}

function showAuthWarning(message) {
  document.getElementById("statusText").textContent = message;
  document.getElementById("authStatusBar").classList.add("show");
}

function clearAllSessions() {
  // Clear all sessions and localStorage
  localStorage.clear();
  fetch("/clear-all-sessions", {
    method: "POST",
    credentials: "include",
  })
    .then(() => {
      location.reload();
    })
    .catch(() => location.reload());
}

function clearStaffSession() {
  // Clear staff session when user logs in - more aggressive approach
  Promise.all([
    fetch("/clear-staff-session", {
      method: "POST",
      credentials: "include",
    }).catch(() => {}),
    fetch("/admin-logout", {
      method: "POST",
      credentials: "include",
    }).catch(() => {}),
    fetch("/logout", {
      method: "POST",
      credentials: "include",
    }).catch(() => {}),
  ]).then(() => {
    // Force clear any staff-related localStorage
    Object.keys(localStorage).forEach((key) => {
      if (key.includes("staff") || key.includes("admin")) {
        localStorage.removeItem(key);
      }
    });
  });
}

function hideAuthWarning() {
  document.getElementById("authStatusBar").classList.remove("show");
}

function showUserLoggedIn() {
  document.getElementById("authContainer").style.display = "none";
  document.getElementById("userStatus").classList.add("show");
  document.getElementById("userEmail").textContent = currentUser.email;
  document.getElementById("loanApplicationSection").style.display = "block";

  // Load user data when logged in
  loadDrafts();
  loadHistory();
}

function switchAppTab(tabName) {
  // Remove active class from all tabs
  document
    .querySelectorAll(".app-tab")
    .forEach((tab) => tab.classList.remove("active"));
  document
    .querySelectorAll(".tab-content")
    .forEach((content) => content.classList.remove("active"));

  // Add active class to selected tab
  event.target.classList.add("active");
  document.getElementById(tabName + "Tab").classList.add("active");

  // Load data for specific tabs
  if (tabName === "drafts") {
    loadDrafts();
  } else if (tabName === "history") {
    loadHistory();
  }
}

function loadDrafts() {
  const draftsContainer = document.getElementById("draftsContainer");
  const drafts = JSON.parse(localStorage.getItem("applicationDrafts") || "[]");
  const userDrafts = drafts.filter(
    (draft) => draft.userEmail === currentUser.email
  );

  if (userDrafts.length === 0) {
    draftsContainer.innerHTML = `
                    <div class="empty-state">
                        <div style="text-align: center; padding: 3rem; color: #6c757d;">
                            <div style="font-size: 4rem; margin-bottom: 1rem;">💾</div>
                            <h4>No Drafts Found</h4>
                            <p>Pre-approved applications will appear here for document upload.</p>
                            <button onclick="switchAppTab('newApplication')" class="btn-primary" style="margin-top: 1rem; width: auto; padding: 0.8rem 2rem;">
                                Create New Application
                            </button>
                        </div>
                    </div>
                `;
    return;
  }

  let draftsHTML = "";
  userDrafts.forEach((draft) => {
    const statusClass = getStatusClass(draft.status);
    const formattedDate = new Date(draft.savedAt).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

    draftsHTML += `
                    <div class="application-card">
                        <div class="application-header">
                            <div class="application-id">📋 ${
                              draft.applicationId
                            }</div>
                            <div class="status-badge ${statusClass}">${draft.status.replace(
      "_",
      " "
    )}</div>
                        </div>
                        
                        <div class="application-details">
                            <div class="detail-item">
                                <div class="detail-label">Loan Type</div>
                                <div class="detail-value">${
                                  draft.formData["loan-type"]
                                }</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Amount</div>
                                <div class="detail-value">₹${parseInt(
                                  draft.formData["loan-amount"]
                                ).toLocaleString()}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Saved On</div>
                                <div class="detail-value">${formattedDate}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Status</div>
                                <div class="detail-value">${
                                  draft.status === "APPROVED"
                                    ? "Ready for Documents"
                                    : "Conditional Approval"
                                }</div>
                            </div>
                        </div>
                        
                        <div class="application-actions">
                            <button onclick="uploadDocumentsForDraft('${
                              draft.applicationId
                            }', '${
      draft.requiredDocuments
    }')" class="btn-small btn-upload">
                                📎 Upload Documents
                            </button>
                            <button onclick="viewDraftDetails('${
                              draft.applicationId
                            }')" class="btn-small btn-view">
                                👁️ View Details
                            </button>
                        </div>
                    </div>
                `;
  });

  draftsContainer.innerHTML = draftsHTML;
}

function loadHistory() {
  const historyContainer = document.getElementById("historyContainer");

  // Get applications from server
  fetch("/user-applications", {
    credentials: "include", // Include cookies for session management
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.applications.length > 0) {
        let historyHTML = "";
        data.applications.forEach((app) => {
          const statusClass = getStatusClass(
            app.status || app.eligibility_status
          );
          const formattedDate = new Date(app.created_at).toLocaleDateString(
            "en-US",
            {
              year: "numeric",
              month: "short",
              day: "numeric",
            }
          );

          historyHTML += `
                                <div class="application-card">
                                    <div class="application-header">
                                        <div class="application-id">📋 ${
                                          app.application_id
                                        }</div>
                                        <div class="status-badge ${statusClass}">${(
            app.status || app.eligibility_status
          ).replace("_", " ")}</div>
                                    </div>
                                    
                                    <div class="application-details">
                                        <div class="detail-item">
                                            <div class="detail-label">Loan Type</div>
                                            <div class="detail-value">${
                                              app.loan_type
                                            }</div>
                                        </div>
                                        <div class="detail-item">
                                            <div class="detail-label">Amount</div>
                                            <div class="detail-value">₹${parseInt(
                                              app.loan_amount
                                            ).toLocaleString()}</div>
                                        </div>
                                        <div class="detail-item">
                                            <div class="detail-label">Applied On</div>
                                            <div class="detail-value">${formattedDate}</div>
                                        </div>
                                        <div class="detail-item">
                                            <div class="detail-label">Current Status</div>
                                            <div class="detail-value">${getStatusText(
                                              app.status ||
                                                app.eligibility_status
                                            )}</div>
                                        </div>
                                    </div>
                                    
                                    <div class="application-actions">
                                        <button onclick="viewApplicationDetails('${
                                          app.application_id
                                        }')" class="btn-small btn-view">
                                            👁️ View Details
                                        </button>
                                        ${
                                          (app.status === "APPROVED" ||
                                            app.status ===
                                              "CONDITIONALLY_APPROVED" ||
                                            app.eligibility_status ===
                                              "APPROVED" ||
                                            app.eligibility_status ===
                                              "CONDITIONALLY_APPROVED") &&
                                          app.status !== "OBJECTION_RAISED"
                                            ? `<button onclick="uploadDocumentsForApplication('${app.application_id}')" class="btn-small btn-upload">📎 Upload Documents</button>`
                                            : ""
                                        }
                                    </div>
                                </div>
                            `;
        });

        historyContainer.innerHTML = historyHTML;
      } else {
        historyContainer.innerHTML = `
                            <div class="empty-state">
                                <div style="text-align: center; padding: 3rem; color: #6c757d;">
                                    <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
                                    <h4>No Applications Found</h4>
                                    <p>Your submitted loan applications will appear here.</p>
                                    <button onclick="switchAppTab('newApplication')" class="btn-primary" style="margin-top: 1rem; width: auto; padding: 0.8rem 2rem;">
                                        Apply for Your First Loan
                                    </button>
                                </div>
                            </div>
                        `;
      }
    })
    .catch((error) => {
      console.error("Error loading history:", error);
      historyContainer.innerHTML = `
                        <div class="empty-state">
                            <div style="text-align: center; padding: 3rem; color: #dc2626;">
                                <div style="font-size: 4rem; margin-bottom: 1rem;">⚠️</div>
                                <h4>Error Loading History</h4>
                                <p>Unable to fetch your application history. Please try again.</p>
                                <button onclick="loadHistory()" class="btn-primary" style="margin-top: 1rem; width: auto; padding: 0.8rem 2rem;">
                                    Retry
                                </button>
                            </div>
                        </div>
                    `;
    });
}

function getStatusClass(status) {
  switch (status?.toLowerCase()) {
    case "approved":
      return "status-approved";
    case "conditionally_approved":
      return "status-conditional";
    case "rejected":
      return "status-rejected";
    case "objection_raised":
      return "status-objection";
    default:
      return "status-pending";
  }
}

function getStatusText(status) {
  switch (status?.toLowerCase()) {
    case "approved":
      return "Approved - Upload Documents";
    case "conditionally_approved":
      return "Conditional Approval";
    case "rejected":
      return "Not Approved";
    case "pending":
      return "Under Review";
    case "objection_raised":
      return "Action Required - See Drafts";
    default:
      return "Processing";
  }
}

function uploadDocumentsForDraft(applicationId, requiredDocs) {
  // Switch to new application tab and show upload section
  switchAppTab("newApplication");
  setTimeout(() => {
    showDocumentUploadSection(applicationId, requiredDocs);
    document
      .getElementById("newApplicationTab")
      .scrollIntoView({ behavior: "smooth" });
  }, 100);
}

function uploadDocumentsForApplication(applicationId) {
  // Get application details and show upload section
  fetch(`/application-details/${applicationId}`, {
    credentials: "include", // Include cookies for session management
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const requiredDocs =
          data.application.required_documents ||
          "Identity Proof, Income Proof, Address Proof";
        uploadDocumentsForDraft(applicationId, requiredDocs);
      }
    })
    .catch((error) => {
      console.error("Error getting application details:", error);
      showAlert("Error loading application details", "error", "application");
    });
}

function viewDraftDetails(applicationId) {
  const drafts = JSON.parse(localStorage.getItem("applicationDrafts") || "[]");
  const draft = drafts.find((d) => d.applicationId === applicationId);

  if (draft) {
    alert(`Application Details for ${applicationId}:
                
Loan Type: ${draft.formData["loan-type"]}
Amount: ₹${parseInt(draft.formData["loan-amount"]).toLocaleString()}
Status: ${draft.status}
Required Documents: ${draft.requiredDocuments}
Saved: ${new Date(draft.savedAt).toLocaleString()}`);
  }
}

function viewApplicationDetails(applicationId) {
  // Fetch and display application details
  fetch(`/application-details/${applicationId}`, {
    credentials: "include", // Include cookies for session management
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const app = data.application;
        alert(`Application Details for ${applicationId}:
                        
Applicant: ${app.full_name}
Loan Type: ${app.loan_type}
Amount: ₹${parseInt(app.loan_amount).toLocaleString()}
Status: ${app.eligibility_status}
Applied: ${new Date(app.created_at).toLocaleString()}
Required Documents: ${app.required_documents || "N/A"}`);
      }
    })
    .catch((error) => {
      console.error("Error loading application details:", error);
      showAlert("Error loading application details", "error", "application");
    });
}

function logout() {
  currentUser = null;
  localStorage.removeItem("currentUser");
  document.getElementById("authContainer").style.display = "block";
  document.getElementById("userStatus").classList.remove("show");
  document.getElementById("loanApplicationSection").style.display = "none";
}

// Login Form Handler
document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
      const response = await fetch("/user-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // Include cookies for session management
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        // Clear staff session when user logs in
        clearStaffSession();

        currentUser = { email: email };
        localStorage.setItem("currentUser", JSON.stringify(currentUser));
        showAlert("Login successful!", "success");
        setTimeout(showUserLoggedIn, 1000);
      } else {
        showAlert(data.error || "Login failed", "error");
      }
    } catch (error) {
      showAlert("Network error. Please try again.", "error");
    }
  });

// Register Form Handler
document
  .getElementById("registerForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const fullName = document.getElementById("regFullName").value;
    const email = document.getElementById("regEmail").value;
    const phone = document.getElementById("regPhone").value;
    const password = document.getElementById("regPassword").value;

    try {
      const response = await fetch("/user-register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // Include cookies for session management
        body: JSON.stringify({ fullName, email, phone, password }),
      });

      const data = await response.json();

      if (data.success) {
        // Clear staff session when user registers
        clearStaffSession();

        currentUser = { email: email };
        localStorage.setItem("currentUser", JSON.stringify(currentUser));
        showAlert("Registration successful!", "success");
        setTimeout(showUserLoggedIn, 1000);
      } else {
        showAlert(data.error || "Registration failed", "error");
      }
    } catch (error) {
      showAlert("Network error. Please try again.", "error");
    }
  });

// Loan Application Form Handler
document
  .getElementById("loanApplicationForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = document.getElementById("submitApplicationBtn");
    submitBtn.disabled = true;
    submitBtn.textContent = "🔄 Processing Application with Watson AI...";

    const formData = {
      "full-name": document.getElementById("fullName").value,
      "date-of-birth": document.getElementById("dateOfBirth").value,
      gender: document.getElementById("gender").value,
      "marital-status": document.getElementById("maritalStatus").value,
      nationality: document.getElementById("nationality").value,
      "contact-number": document.getElementById("contactNumber").value,
      "employment-type": document.getElementById("employmentType").value,
      "employer-name": document.getElementById("employerName").value,
      "annual-income": document.getElementById("annualIncome").value,
      "existing-loans":
        document.getElementById("existingLoans").value || "None",
      "loan-type": document.getElementById("loanType").value,
      "loan-amount": document.getElementById("loanAmount").value,
      "loan-tenure": document.getElementById("loanTenure").value,
      "loan-purpose": document.getElementById("loanPurpose").value,
      "preferred-emi": document.getElementById("preferredEmi").value || "",
      "cibil-score": document.getElementById("cibilScore").value,
    };

    try {
      const response = await fetch("/apply-comprehensive-loan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // Include cookies for session management
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        const applicationId = data.application_id;
        const eligibilityStatus = data.eligibility_status;

        // Show success message with status
        let statusMessage = "";
        let alertType = "success";

        if (eligibilityStatus === "APPROVED") {
          statusMessage = `🎉 Congratulations! Your application ${applicationId} is PRE-APPROVED! 
                        
Next Steps:
• Check your email for document requirements
• Upload required documents below
• Wait for final verification`;

          // Show document upload section for approved applications
          showDocumentUploadSection(applicationId, data.required_documents);
        } else if (eligibilityStatus === "CONDITIONALLY_APPROVED") {
          statusMessage = `⚠️ Your application ${applicationId} is CONDITIONALLY APPROVED! 
                        
Assessment: ${data.eligibility_reason}

Required Documents: ${data.required_documents}

Please check your email for detailed instructions.`;
          alertType = "info";

          // Show document upload section for conditionally approved applications
          showDocumentUploadSection(applicationId, data.required_documents);
        } else {
          statusMessage = `📋 Application ${applicationId} submitted for review.
                        
Assessment: ${data.eligibility_reason}

Please check your email for next steps and recommendations.`;
          alertType = "info";
        }

        showAlert(statusMessage, alertType, "application");

        // Save application draft for approved/conditionally approved
        if (
          eligibilityStatus === "APPROVED" ||
          eligibilityStatus === "CONDITIONALLY_APPROVED"
        ) {
          saveApplicationDraft(
            applicationId,
            formData,
            eligibilityStatus,
            data.required_documents
          );
        }

        // Reset form
        document.getElementById("loanApplicationForm").reset();
      } else {
        showAlert(
          data.error || "Application submission failed",
          "error",
          "application"
        );
      }
    } catch (error) {
      showAlert("Network error. Please try again.", "error", "application");
      console.error("Application error:", error);
    }

    submitBtn.disabled = false;
    submitBtn.textContent = "🚀 Submit Application for AI Pre-Approval";
  });

// Save application draft to localStorage
function saveApplicationDraft(applicationId, formData, status, requiredDocs) {
  const draft = {
    applicationId: applicationId,
    formData: formData,
    status: status,
    requiredDocuments: requiredDocs,
    savedAt: new Date().toISOString(),
    userEmail: currentUser.email,
  };

  let drafts = JSON.parse(localStorage.getItem("applicationDrafts") || "[]");
  drafts.push(draft);
  localStorage.setItem("applicationDrafts", JSON.stringify(drafts));
}

// Show document upload section for approved applications
function showDocumentUploadSection(applicationId, requiredDocs) {
  // Create document type mapping
  const docTypeMapping = {
    "Identity Proof": ["Aadhaar Card", "PAN Card", "Passport Size Photos"],
    "Income Proof": [
      "Bank Statements (6 months)",
      "Salary Slips (3 months)",
      "Form 16",
      "ITR (2 years)",
    ],
    "Address Proof": [
      "Aadhaar Card",
      "Bank Statements (6 months)",
      "Property Documents",
    ],
    "PAN Card": ["PAN Card"],
    "Aadhaar Card": ["Aadhaar Card"],
    Salary: ["Salary Slips (3 months)", "Employment Certificate", "Form 16"],
    "Employment Certificate": ["Employment Certificate"],
    "Bank Statements": ["Bank Statements (6 months)"],
    "Form 16": ["Form 16"],
    "Business Registration": ["Business Registration"],
    ITR: ["ITR (2 years)"],
    "Property Documents": ["Property Documents"],
  };

  // Generate options based on required documents
  let docOptions = '<option value="">Select Document Type</option>';
  const requiredDocsList = requiredDocs.split(", ").map((doc) => doc.trim());
  const allAllowedDocs = new Set();

  requiredDocsList.forEach((requiredDoc) => {
    if (docTypeMapping[requiredDoc]) {
      docTypeMapping[requiredDoc].forEach((docType) => {
        allAllowedDocs.add(docType);
      });
    } else {
      // If exact match not found, try partial matching
      Object.keys(docTypeMapping).forEach((key) => {
        if (
          requiredDoc.toLowerCase().includes(key.toLowerCase()) ||
          key.toLowerCase().includes(requiredDoc.toLowerCase())
        ) {
          docTypeMapping[key].forEach((docType) => {
            allAllowedDocs.add(docType);
          });
        }
      });
    }
  });

  // Convert set to sorted array and create options
  Array.from(allAllowedDocs)
    .sort()
    .forEach((docType) => {
      docOptions += `<option value="${docType}">${docType}</option>`;
    });

  // Add "Other" option at the end
  docOptions += '<option value="Other">Other</option>';

  const uploadSection = document.createElement("div");
  uploadSection.id = "documentUploadSection";
  uploadSection.innerHTML = `
                <div class="form-section" style="background: #f0f9ff; border: 2px solid #0ea5e9; border-radius: 12px; margin-top: 2rem;">
                    <h3 class="section-title" style="color: #0c4a6e;">📄 Document Upload - Application ${applicationId}</h3>
                    
                    <div class="alert alert-info" style="display: block; margin-bottom: 1rem;">
                        <strong>Required Documents:</strong><br>
                        ${requiredDocs
                          .split(", ")
                          .map((doc) => `• ${doc}`)
                          .join("<br>")}
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="documentType">Document Type</label>
                            <select id="documentType" required>
                                ${docOptions}
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="documentFile">Upload Document</label>
                            <input type="file" id="documentFile" accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" required>
                            <small style="color: #6c757d; font-size: 0.9rem;">
                                Supported formats: PDF, JPG, PNG, DOC, DOCX (Max 5MB)
                            </small>
                        </div>
                    </div>
                    
                    <button type="button" onclick="uploadDocument('${applicationId}')" class="btn-primary" id="uploadDocBtn">
                        📎 Upload Document
                    </button>
                    
                    <div class="alert alert-success" id="uploadSuccess" style="display: none; margin-top: 1rem;"></div>
                    <div class="alert alert-error" id="uploadError" style="display: none; margin-top: 1rem;"></div>
                </div>
            `;

  // Insert after the loan application form
  const loanSection = document.getElementById("loanApplicationSection");
  loanSection.appendChild(uploadSection);
}

// Upload document function
async function uploadDocument(applicationId) {
  const documentType = document.getElementById("documentType").value;
  const documentFile = document.getElementById("documentFile").files[0];

  if (!documentType || !documentFile) {
    document.getElementById("uploadError").textContent =
      "Please select document type and file";
    document.getElementById("uploadError").style.display = "block";
    return;
  }

  // Check file size (5MB limit)
  if (documentFile.size > 5 * 1024 * 1024) {
    document.getElementById("uploadError").textContent =
      "File size must be less than 5MB";
    document.getElementById("uploadError").style.display = "block";
    return;
  }

  const uploadBtn = document.getElementById("uploadDocBtn");
  uploadBtn.disabled = true;
  uploadBtn.textContent = "📤 Uploading...";

  const formData = new FormData();
  formData.append("application_id", applicationId);
  formData.append("document_type", documentType);
  formData.append("document", documentFile);

  try {
    const response = await fetch("/upload-documents", {
      method: "POST",
      credentials: "include", // Include cookies for session management
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      document.getElementById(
        "uploadSuccess"
      ).textContent = `✅ ${documentType} uploaded successfully! Admin has been notified.`;
      document.getElementById("uploadSuccess").style.display = "block";
      document.getElementById("uploadError").style.display = "none";

      // Reset upload form
      document.getElementById("documentType").value = "";
      document.getElementById("documentFile").value = "";

      // Send email notification to admin
      notifyAdminOfDocumentUpload(
        applicationId,
        documentType,
        currentUser.email
      );
    } else {
      document.getElementById("uploadError").textContent =
        data.error || "Upload failed";
      document.getElementById("uploadError").style.display = "block";
    }
  } catch (error) {
    document.getElementById("uploadError").textContent =
      "Network error during upload";
    document.getElementById("uploadError").style.display = "block";
    console.error("Upload error:", error);
  }

  uploadBtn.disabled = false;
  uploadBtn.textContent = "📎 Upload Document";
}

// Notify admin of document upload
async function notifyAdminOfDocumentUpload(
  applicationId,
  documentType,
  userEmail
) {
  try {
    await fetch("/notify-admin-document-upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Include cookies for session management
      body: JSON.stringify({
        application_id: applicationId,
        document_type: documentType,
        user_email: userEmail,
      }),
    });
  } catch (error) {
    console.error("Admin notification error:", error);
  }
}
