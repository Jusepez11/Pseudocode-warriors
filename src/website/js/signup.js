document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm');
    const termsCheckbox = document.getElementById('terms');
    const pwBar = document.getElementById('pwBar');

    const usernameError = document.getElementById('usernameError');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
    const confirmError = document.getElementById('confirmError');

    // Check if already logged in
    if (isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }

    // Password strength indicator (visual only, not validation)
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        let strength = 0;

        if (password.length >= 6) strength += 25;
        if (password.length >= 10) strength += 25;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
        if (/\d/.test(password)) strength += 25;

        pwBar.style.width = `${strength}%`;
        pwBar.style.background = strength < 50 ? '#ef4444' : strength < 75 ? '#f59e0b' : '#10b981';
    });

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        usernameError.textContent = '';
        emailError.textContent = '';
        passwordError.textContent = '';
        confirmError.textContent = '';

        const username = usernameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const confirm = confirmInput.value;
        const termsAccepted = termsCheckbox.checked;

        let hasError = false;

        if (!username) {
            usernameError.textContent = 'Please enter your full name';
            hasError = true;
        }

        if (!email) {
            emailError.textContent = 'Please enter your email';
            hasError = true;
        }

        if (!password) {
            passwordError.textContent = 'Please enter a password';
            hasError = true;
        }

        if (!confirm) {
            confirmError.textContent = 'Please confirm your password';
            hasError = true;
        } else if (password !== confirm) {
            confirmError.textContent = 'Passwords do not match';
            hasError = true;
        }

        if (!termsAccepted) {
            alert('Please accept the Terms and Privacy Policy');
            hasError = true;
        }

        if (hasError) return;

        const submitButton = signupForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Creating account...';

        try {
            await register(username, email, password);
            await login(username, password);

            window.location.href = 'index.html';
        } catch (error) {
            // Parse error message from backend
            let errorMessage = error.message || 'Registration failed. Please try again.';

            // Check if it's a Pydantic validation error with detail array
            try {
                const errorData = JSON.parse(errorMessage);
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    // Handle Pydantic validation errors
                    errorData.detail.forEach(err => {
                        const field = err.loc && err.loc.length > 1 ? err.loc[1] : null;
                        const message = err.msg || err.ctx?.reason || 'Invalid input';

                        if (field === 'username') {
                            usernameError.textContent = message;
                        } else if (field === 'email') {
                            emailError.textContent = message;
                        } else if (field === 'password') {
                            passwordError.textContent = message;
                        } else {
                            passwordError.textContent = message;
                        }
                    });
                } else if (typeof errorData.detail === 'string') {
                    // Handle simple error messages
                    errorMessage = errorData.detail;
                    if (errorMessage.includes('Username')) {
                        usernameError.textContent = errorMessage;
                    } else if (errorMessage.includes('Email')) {
                        emailError.textContent = errorMessage;
                    } else {
                        passwordError.textContent = errorMessage;
                    }
                } else {
                    passwordError.textContent = 'Registration failed. Please try again.';
                }
            } catch (parseError) {
                // Not JSON, use the error message as-is
                if (errorMessage.includes('Username')) {
                    usernameError.textContent = errorMessage;
                } else if (errorMessage.includes('Email')) {
                    emailError.textContent = errorMessage;
                } else {
                    passwordError.textContent = errorMessage;
                }
            }

            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
});