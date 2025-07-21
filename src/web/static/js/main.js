// ServiceNow Document Generator - Main JavaScript

// Global variables
let currentPreviewData = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFormValidation();
    initializeAjaxSetup();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Setup AJAX defaults
function initializeAjaxSetup() {
    // Add CSRF token to all requests if needed
    // Setup default error handling
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        showNotification('予期しないエラーが発生しました', 'error');
    });
}

// Utility functions
function showNotification(message, type = 'info', duration = 5000) {
    const alertTypes = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };
    
    const alertClass = alertTypes[type] || 'alert-info';
    const alertId = 'alert-' + Date.now();
    
    const alertHtml = `
        <div id="${alertId}" class="alert ${alertClass} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 1050; min-width: 300px;" role="alert">
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto remove after duration
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, duration);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// API functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Template functions
async function loadTemplatePreview(documentType) {
    if (!documentType) {
        showNotification('ドキュメントタイプを選択してください', 'warning');
        return null;
    }
    
    try {
        const data = await apiRequest(`/api/templates/${encodeURIComponent(documentType)}/preview`);
        return data;
    } catch (error) {
        showNotification(`プレビューの取得に失敗しました: ${error.message}`, 'error');
        throw error;
    }
}

async function generateDocument(documentRequest) {
    try {
        const data = await apiRequest('/api/generate', {
            method: 'POST',
            body: JSON.stringify(documentRequest)
        });
        return data;
    } catch (error) {
        showNotification(`ドキュメント生成に失敗しました: ${error.message}`, 'error');
        throw error;
    }
}

// Download functions
function downloadFile(filename) {
    window.open(`/api/download/${encodeURIComponent(filename)}`, '_blank');
}

function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Form helpers
function getFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

function resetForm(formElement) {
    formElement.reset();
    formElement.classList.remove('was-validated');
}

// Loading states
function showLoading(element, text = 'Loading...') {
    const originalContent = element.innerHTML;
    element.dataset.originalContent = originalContent;
    element.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        ${text}
    `;
    element.disabled = true;
}

function hideLoading(element) {
    if (element.dataset.originalContent) {
        element.innerHTML = element.dataset.originalContent;
        delete element.dataset.originalContent;
    }
    element.disabled = false;
}

// Modal helpers
function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
    return modal;
}

function hideModal(modalId) {
    const modalElement = document.getElementById(modalId);
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide();
    }
}

// Local storage helpers
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.warn('Failed to save to localStorage:', error);
    }
}

function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : defaultValue;
    } catch (error) {
        console.warn('Failed to load from localStorage:', error);
        return defaultValue;
    }
}

// Form auto-save
function enableAutoSave(formElement, key) {
    const inputs = formElement.querySelectorAll('input, select, textarea');
    
    // Load saved data
    const savedData = loadFromLocalStorage(key, {});
    inputs.forEach(input => {
        if (savedData[input.name]) {
            input.value = savedData[input.name];
        }
    });
    
    // Save on change
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const formData = getFormData(formElement);
            saveToLocalStorage(key, formData);
        });
    });
    
    // Clear on submit
    formElement.addEventListener('submit', () => {
        localStorage.removeItem(key);
    });
}

// Export functions for global use
window.DocumentGenerator = {
    loadTemplatePreview,
    generateDocument,
    downloadFile,
    downloadBlob,
    showNotification,
    showLoading,
    hideLoading,
    showModal,
    hideModal,
    enableAutoSave,
    getFormData,
    resetForm
};