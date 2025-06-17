// Firebase configuration -- replace with your own project credentials
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

// Handle sign in form submission
if (document.getElementById('login-form')) {
    document.getElementById('login-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        auth.signInWithEmailAndPassword(email, password)
            .then(() => {
                window.location.href = 'dashboard.html';
            })
            .catch(err => {
                document.getElementById('login-error').textContent = err.message;
            });
    });
}

// Redirect to login if not authenticated for protected pages
function requireAuth() {
    auth.onAuthStateChanged(user => {
        if (!user) {
            window.location.href = 'login.html';
        }
    });
}

// Sign out helper
function signOut() {
    auth.signOut().then(() => {
        window.location.href = 'login.html';
    });
}
