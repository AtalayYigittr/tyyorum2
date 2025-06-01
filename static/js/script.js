let products = [];

function addProduct() {
    const name = document.getElementById('productName').value;
    const url = document.getElementById('productUrl').value;
    
    if (!name || !url) {
        showAlert('error', 'Lütfen ürün adı ve URL giriniz!');
        return;
    }
    
    if (!url.includes('trendyol.com')) {
        showAlert('error', 'Lütfen geçerli bir Trendyol ürün linki giriniz!');
        return;
    }
    
    // Check if URL contains a product ID
    if (!url.match(/p-\d+|\/\d+\/yorumlar|\/\d+\/?$/)) {
        showAlert('error', 'Geçersiz ürün URL\'si. Lütfen ürün sayfasından veya yorum sayfasından alınan URL\'yi kullanın.');
        return;
    }
    
    if (products.length >= 10) {
        showAlert('error', 'Maksimum 10 ürün ekleyebilirsiniz!');
        return;
    }
    
    products.push({ name, url });
    updateProductList();
    showAlert('success', 'Ürün başarıyla eklendi!');
    
    // Clear inputs
    document.getElementById('productName').value = '';
    document.getElementById('productUrl').value = '';
}

function removeProduct(index) {
    products.splice(index, 1);
    updateProductList();
    showAlert('info', 'Ürün kaldırıldı');
}

function updateProductList() {
    const productList = document.getElementById('productList');
    productList.innerHTML = products.map((product, index) => `
        <div class="product-item">
            <div>
                <strong>${escapeHtml(product.name)}</strong>
                <small class="text-muted">${escapeHtml(product.url)}</small>
            </div>
            <button class="btn btn-outline-danger btn-sm" onclick="removeProduct(${index})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const alertContainer = document.getElementById('alertContainer');
    alertContainer.appendChild(alertDiv);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => alertDiv.remove(), 150);
    }, 3000);
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatSentiment(sentiment) {
    const value = parseFloat(sentiment);
    if (value > 0.3) return '<span class="text-success">Olumlu</span>';
    if (value < -0.3) return '<span class="text-danger">Olumsuz</span>';
    return '<span class="text-warning">Nötr</span>';
}

function displayReviews(reviews) {
    return reviews.map(review => `
        <div class="review-item ${review.sentiment > 0 ? 'positive' : review.sentiment < 0 ? 'negative' : 'neutral'}">
            <div class="review-rating">
                ${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}
            </div>
            <div class="review-text">${escapeHtml(review.text)}</div>
            <div class="review-sentiment">
                Duygu Analizi: ${formatSentiment(review.sentiment)}
            </div>
        </div>
    `).join('');
}

function displayTopics(topics) {
    return topics.map(([topic, count]) => `
        <span class="badge bg-secondary me-1">
            ${escapeHtml(topic)} (${count})
        </span>
    `).join('');
}

function analyzeProducts() {
    if (products.length === 0) {
        showAlert('error', 'Lütfen en az bir ürün ekleyin!');
        return;
    }
    
    document.getElementById('results').style.display = 'block';
    document.getElementById('analysisResults').innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Yükleniyor...</span>
            </div>
            <p class="mt-2">Ürünler analiz ediliyor...</p>
        </div>
    `;
    
    fetch('/compare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ products })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display sentiment comparison chart
        Plotly.newPlot('sentimentChart', JSON.parse(data.visualizations.sentiment_comparison));
        
        // Display detailed results
        const resultsHtml = data.results.map(result => {
            if (result.error) {
                return `
                    <div class="analysis-item error">
                        <h4>${escapeHtml(result.name)}</h4>
                        <div class="alert alert-danger">
                            Hata: ${escapeHtml(result.error)}
                        </div>
                    </div>
                `;
            }
            
            return `
                <div class="analysis-item">
                    <h4>${escapeHtml(result.name)}</h4>
                    <div class="sentiment-stats">
                        <div class="sentiment-score ${result.avg_sentiment > 0 ? 'positive' : result.avg_sentiment < 0 ? 'negative' : 'neutral'}">
                            Genel Duygu Analizi: ${formatSentiment(result.avg_sentiment)}
                        </div>
                        <div class="review-counts">
                            <span class="badge bg-success">Olumlu: ${result.positive_count}</span>
                            <span class="badge bg-danger">Olumsuz: ${result.negative_count}</span>
                            <span class="badge bg-warning text-dark">Nötr: ${result.neutral_count}</span>
                            <span class="badge bg-info">Toplam: ${result.total_reviews}</span>
                        </div>
                    </div>
                    
                    <div class="topics-section mt-3">
                        <h5>En Çok Bahsedilen Konular:</h5>
                        <div class="topics-list">
                            ${displayTopics(result.top_topics)}
                        </div>
                    </div>
                    
                    <div class="reviews-section mt-3">
                        <h5>Örnek Yorumlar:</h5>
                        <div class="reviews-list">
                            ${displayReviews(result.reviews)}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        document.getElementById('analysisResults').innerHTML = resultsHtml;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('analysisResults').innerHTML = `
            <div class="alert alert-danger">
                <h5>Analiz sırasında bir hata oluştu:</h5>
                <p>${error.message}</p>
                ${error.details ? `
                    <hr>
                    <h6>Hata Detayları:</h6>
                    <ul>
                        ${error.details.map(detail => `<li>${detail}</li>`).join('')}
                    </ul>
                ` : ''}
                <hr>
                <p class="mb-0">Lütfen şunları kontrol edin:</p>
                <ul class="mb-0">
                    <li>Ürün URL'lerinin doğru olduğundan emin olun</li>
                    <li>Ürünlerin yorum sayfalarına erişilebildiğinden emin olun</li>
                    <li>Ürünlerin en az bir yorumu olduğundan emin olun</li>
                </ul>
            </div>
        `;
    });
}
