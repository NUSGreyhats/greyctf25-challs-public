const output = document.getElementById('output');
const authSection = document.getElementById('authSection');
const appSection = document.getElementById('appSection');

// Check if toilet technician is logged in on page load
window.addEventListener('load', checkAuthStatus);

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/user');
        if (response.ok) {
            const user = await response.json();
            showApp(user);
        } else {
            showAuth();
        }
    } catch (error) {
        showAuth();
    }
}

function showAuth() {
    authSection.style.display = 'block';
    appSection.style.display = 'none';
}

function showApp(user) {
    authSection.style.display = 'none';
    appSection.style.display = 'block';
    
    document.getElementById('currentUser').textContent = `Welcome, Toilet Technician ${user.username}`;
    document.getElementById('username').value = user.username;
    document.getElementById('email').value = user.email;
    document.getElementById('toiletExperience').value = user.toiletExperience || '';
    document.getElementById('dateUpdated').value = new Date().toISOString();
    document.getElementById('smell').value = user.smell || '';
    document.getElementById('temperature').value = user.temperature || '';
}

// Login form
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        
        const result = await response.json();
        
        if (result.success) {
            checkAuthStatus();
            showMessage('Dispenser access granted! 🧻', 'success');
        } else {
            showMessage(result.error, 'error');
        }
    } catch (error) {
        showMessage('Dispenser access failed', 'error');
    }
});

// Register form
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        
        const result = await response.json();
        
        if (result.success) {
            checkAuthStatus();
            showMessage('New toilet technician registered successfully! 🚽', 'success');
        } else {
            showMessage(result.error, 'error');
        }
    } catch (error) {
        showMessage('Toilet technician registration failed', 'error');
    }
});

// Profile form
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/update-profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, // Add JSON header
            body: JSON.stringify(Object.fromEntries(formData)) // Convert to JSON
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('Dispenser configuration updated successfully! 🧻✨', 'success');
            await refreshProfile();
        } else {
            showMessage('Dispenser update failed', 'error');
        }
    } catch (error) {
        showMessage('Toilet network error', 'error');
    }
});

async function refreshProfile() {
    try {
        const response = await fetch('/api/user');
        if (response.ok) {
            const user = await response.json();
            document.getElementById('username').value = user.username;
            document.getElementById('email').value = user.email;
            document.getElementById('toiletExperience').value = user.toiletExperience || '';
            document.getElementById('smell').value = user.smell || '';
            document.getElementById('temperature').value = user.temperature || '';
            document.getElementById('currentUser').textContent = `Welcome, Toilet Technician ${user.username}`;
        }
    } catch (error) {
        console.log('Failed to refresh toilet profile');
    }
}

async function logout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        showAuth();
        showMessage('Exited dispenser safely 🚪', 'success');
    } catch (error) {
        showMessage('Failed to exit dispenser', 'error');
    }
}

async function checkAdmin() {
    try {
        const response = await fetch('/admin/dashboard');
        
        if (response.ok) {
            const result = await response.json();
            showMessage(`Supreme toilet technician access granted! 🚽👑<br><div class="flag">${result.flag}</div>`, 'success');
        } else {
            const error = await response.json();
            showMessage(error.error || 'Toilet access denied', 'error');
        }
    } catch (error) {
        showMessage('Toilet network error', 'error');
    }
}

function showMessage(message, type) {
    output.innerHTML = `<div class="${type}">${message}</div>`;
}