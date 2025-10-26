document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    // Check if already logged in
    if (isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        emailError.textContent = '';
        passwordError.textContent = '';

        const email = emailInput.value.trim();
        const password = passwordInput.value;

        if (!email) {
            emailError.textContent = 'Please enter your email or username';
            emailInput.focus();
            return;
        }

        if (!password) {
            passwordError.textContent = 'Please enter your password';
            passwordInput.focus();
            return;
        }

        const submitButton = loginForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Signing in...';

        try {
            await login(email, password);

            window.location.href = 'index.html';
        } catch (error) {
            // Parse error message from backend
            let errorMessage = error.message || 'Login failed. Please check your credentials.';

            // Check if it's a JSON error response
            try {
                const errorData = JSON.parse(errorMessage);
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    // Handle Pydantic validation errors
                    errorData.detail.forEach(err => {
                        passwordError.textContent = err.msg || err.ctx?.reason || 'Invalid input';
                    });
                } else if (typeof errorData.detail === 'string') {
                    // Handle simple error messages
                    passwordError.textContent = errorData.detail;
                } else {
                    passwordError.textContent = 'Login failed. Please check your credentials.';
                }
            } catch (parseError) {
                // Not JSON, use the error message as-is
                passwordError.textContent = errorMessage;
            }

            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
});

