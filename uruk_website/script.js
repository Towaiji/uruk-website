// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add button hover effects
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'scale(1.1)';
    });
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'scale(1)';
    });
});

// dynamically load header.html on each file
document.addEventListener("DOMContentLoaded", () => {
  const headerPlaceholder = document.getElementById("main-header");
  if (headerPlaceholder) {
    fetch("header.html")
      .then(response => response.text())
      .then(data => {
        headerPlaceholder.innerHTML = data;

        // AFTER header is inserted, set active link based on current page
        const currentPath = window.location.pathname.split("/").pop(); // e.g. about.html
        const navLinks = document.querySelectorAll(".nav-bar ul li a");

        navLinks.forEach(link => {
          const href = link.getAttribute("href");
          if (href === currentPath) {
            link.classList.add("active");
          } else {
            link.classList.remove("active");
          }
        });
      })
      .catch(err => {
        console.error("Failed to load header:", err);
      });
  }
});

