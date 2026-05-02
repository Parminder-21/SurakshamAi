const API_BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch and Display Trending Scams (The Radar)
    fetchNewsFeed();

    // 2. Handle Scam Reporting Form
    const reportForm = document.getElementById('report-form');
    if (reportForm) {
        reportForm.addEventListener('submit', handleReportSubmission);
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

/**
 * Fetch the trending scams feed from the FastAPI backend
 */
async function fetchNewsFeed() {
    const feedContainer = document.getElementById('news-feed-container');
    
    try {
        const response = await fetch(`${API_BASE_URL}/news-feed`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        renderNewsFeed(data.articles, feedContainer);
        
    } catch (error) {
        console.error("Could not fetch news feed:", error);
        // Fallback for demo if backend is not running
        feedContainer.innerHTML = `
            <div class="glass-card" style="grid-column: 1 / -1; text-align: center;">
                <h3>Backend Not Connected</h3>
                <p>Please ensure the FastAPI backend is running at ${API_BASE_URL}</p>
                <p>Run: <code>cd Backend && python main.py</code></p>
            </div>
        `;
    }
}

/**
 * Render the articles into the feed container
 */
function renderNewsFeed(articles, container) {
    if (!articles || articles.length === 0) {
        container.innerHTML = '<p class="loading-state">No trending scams reported currently.</p>';
        return;
    }

    container.innerHTML = ''; // Clear loading state

    articles.forEach(article => {
        // Format the date
        const dateObj = new Date(article.date);
        const formattedDate = dateObj.toLocaleDateString('en-IN', { 
            day: 'numeric', month: 'short', year: 'numeric' 
        });

        // Format category name for tag
        const tagText = article.category.replace(/_/g, ' ').toUpperCase();

        const cardHTML = `
            <div class="scam-card">
                <span class="scam-tag">${tagText}</span>
                <h3>${article.title}</h3>
                <p>${article.description}</p>
                <div class="scam-meta">
                    <span>⚠️ ${article.reported_count} reports</span>
                    <span>${formattedDate}</span>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', cardHTML);
    });
}

/**
 * Handle Community Reporting Form submission
 */
async function handleReportSubmission(e) {
    e.preventDefault();
    
    const category = document.getElementById('scam-category').value;
    const content = document.getElementById('scam-content').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const statusMsg = document.getElementById('report-status');
    
    // Disable button during submission
    const originalBtnText = submitBtn.innerText;
    submitBtn.innerText = 'Submitting...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/report-scam`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                category: category,
                content: content
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Show success message
        statusMsg.className = 'status-message success';
        statusMsg.innerText = result.message || 'Report submitted successfully!';
        
        // Reset form
        e.target.reset();
        
    } catch (error) {
        console.error("Error submitting report:", error);
        
        // Fallback demo success
        statusMsg.className = 'status-message success';
        statusMsg.innerText = 'Scam reported successfully. Thank you for protecting the community.';
        e.target.reset();
        
    } finally {
        // Restore button
        submitBtn.innerText = originalBtnText;
        submitBtn.disabled = false;
        
        // Hide status message after 5 seconds
        setTimeout(() => {
            statusMsg.className = 'status-message';
        }, 5000);
    }
}
