// document.addEventListener('DOMContentLoaded', function() {
//     // --- ELEMENT REFERENCES ---
//     const loanForm = document.getElementById('loanApplicationForm');
//     const formContainer = document.getElementById('form-container');
//     const responseContainer = document.getElementById('response-container');
//     const emiSlider = document.getElementById('preferred-emi');
//     const emiValue = document.getElementById('emi-value');

//     // --- CONFIGURATION ---
//     const BACKEND_URL = 'http://127.0.0.1:5000/ask';

//     // --- EVENT LISTENERS ---
//     if (loanForm) {
//         loanForm.addEventListener('submit', handleFormSubmit);
//     }

//     if (emiSlider) {
//         emiSlider.addEventListener('input', () => {
//             const value = parseInt(emiSlider.value).toLocaleString('en-IN');
//             emiValue.textContent = value;
//         });
//     }

//     /**
//      * Main function to handle the form submission.
//      * @param {Event} event - The form submission event.
//      */
//     async function handleFormSubmit(event) {
//         event.preventDefault(); // Prevent default page reload
        
//         // Basic validation
//         if (!validateForm()) {
//             alert('Please fill out all required fields marked with *');
//             return;
//         }

//         const submitButton = document.getElementById('submit-btn');
//         submitButton.disabled = true;
//         submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

//         // Collect all data from the form
//         const formData = collectFormData();
        
//         try {
//             // Send data to the backend
//             const response = await fetch(BACKEND_URL, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify(formData)
//             });

//             if (!response.ok) {
//                 throw new Error(`Server error: ${response.statusText}`);
//             }

//             const data = await response.json();
            
//             // Display the AI's response
//             displayAIResponse(data.response, data.is_eligible);

//         } catch (error) {
//             console.error('Error submitting application:', error);
//             displayAIResponse(`An error occurred while contacting the server: ${error.message}`, false);
//         } finally {
//             // Re-enable the button in case of an error where the view doesn't change
//             submitButton.disabled = false;
//             submitButton.innerHTML = '<i class="fas fa-paper-plane"></i> Check Eligibility';
//         }
//     }

//     /**
//      * Collects all data from form fields into a structured object.
//      * @returns {object} The structured form data.
//      */
//     function collectFormData() {
//         const getCheckedValues = (name) => Array.from(document.querySelectorAll(`input[name="${name}"]:checked`)).map(cb => cb.value);
        
//         return {
//             personalDetails: {
//                 name: document.getElementById('name').value,
//                 dob: document.getElementById('dob').value,
//                 gender: document.querySelector('input[name="gender"]:checked')?.value || '',
//                 maritalStatus: document.getElementById('marital-status').value,
//                 nationality: document.getElementById('nationality').value,
//                 contact: document.getElementById('contact').value,
//                 email: document.getElementById('email').value
//             },
//             employment: {
//                 type: document.querySelector('input[name="employment"]:checked')?.value || '',
//                 employer: document.getElementById('employer').value,
//                 income: document.getElementById('income').value,
//                 existingLoans: document.getElementById('existing-loans').value
//             },
//             loanDetails: {
//                 types: getCheckedValues('loan-type'),
//                 amount: document.getElementById('loan-amount').value,
//                 tenure: document.getElementById('tenure').value,
//                 purpose: document.getElementById('purpose').value,
//                 preferredEMI: document.getElementById('preferred-emi').value,
//                 cibilScore: document.getElementById('cibil-score').value
//             }
//         };
//     }

//     /**
//      * Displays the AI's response by hiding the form and showing the response container.
//      * @param {string} aiResponse - The text response from the AI.
//      * @param {boolean} isEligible - A boolean indicating eligibility.
//      */
//     function displayAIResponse(aiResponse, isEligible) {
//         formContainer.style.display = 'none'; // Hide the form
        
//         const eligibilityStatus = isEligible ? 'Potentially Eligible' : 'Likely Ineligible';
//         const eligibilityClass = isEligible ? 'eligible' : 'not-eligible';

//         responseContainer.innerHTML = `
//             <div class="response-header">
//                 <h2>Loan Eligibility Assessment</h2>
//                 <div class="status-badge ${eligibilityClass}">
//                     ${isEligible ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-times-circle"></i>'} ${eligibilityStatus}
//                 </div>
//             </div>
//             <div class="ai-response">
//                 <h3>AI Analysis Result:</h3>
//                 <div class="response-text">${aiResponse.replace(/\n/g, '<br>')}</div>
//             </div>
//             <div class="action-buttons">
//                 <button onclick="location.reload()" class="btn-secondary">
//                     <i class="fas fa-redo"></i> Apply Again
//                 </button>
//             </div>
//         `;

//         responseContainer.style.display = 'block'; // Show the response
//     }

//     /**
//      * Simple validation to check required fields.
//      * @returns {boolean} True if the form is valid, false otherwise.
//      */
//     function validateForm() {
//         let isValid = true;
//         const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
//         requiredFields.forEach(field => {
//             if (!field.value.trim()) {
//                 field.classList.add('error');
//                 isValid = false;
//             } else {
//                 field.classList.remove('error');
//             }
//         });
//         return isValid;
//     }
// });
