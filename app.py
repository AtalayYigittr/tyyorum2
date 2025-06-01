from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import logging
import time
from collections import Counter
from textblob import TextBlob
import plotly.express as px

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendyolSentimentAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': 'https://www.trendyol.com',
            'Referer': 'https://www.trendyol.com/'
        })
        self.stopwords = set([
            'bir', 've', 'bu', 'için', 'ile', 'çok', 'da', 'de', 'en', 'ki',
            'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'şu', 'ama', 'fakat',
            'ise', 'yani', 'nasıl', 'neden', 'ne', 'kim', 'nerede', 'gibi', 'kadar'
        ])
    
    def get_product_reviews(self, product_url, max_pages=5):
        try:
            # Extract product ID from URL
            # Support both formats: p-{id} and /productID/yorumlar
            # Remove any query parameters from URL first
            clean_url = product_url.split('?')[0]
            product_id = re.search(r'p-(\d+)|/(\d+)/yorumlar|/(\d+)/?$', clean_url)
            if not product_id:
                raise ValueError("Geçersiz ürün URL'si. URL'nin sonunda ürün ID'si olmalıdır.")
            # Get the first non-None group (either from p-{id} or /{id}/yorumlar format)
            product_id = next(g for g in product_id.groups() if g is not None)
            logger.info(f"Extracted product ID: {product_id} from URL: {product_url}")
            
            reviews = []
            base_url = "https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review"
            
            for page in range(1, max_pages + 1):
                try:
                    url = f"{base_url}/{product_id}?page={page}&pageSize=30&sort=0"
                    response = self.session.get(url)
                    if response.status_code == 429:  # Rate limit
                        time.sleep(5)  # Wait for 5 seconds
                        response = self.session.get(url)
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data.get('result', {}).get('productReviews', []):
                        break
                        
                    reviews_data = data.get('result', {}).get('productReviews', [])
                    if not reviews_data:
                        logger.warning(f"No reviews found in response for product {product_id} on page {page}")
                        continue
                        
                    for review in reviews_data:
                        comment = review.get('comment', '').strip()
                        if not comment:  # Skip empty reviews
                            continue
                            
                        reviews.append({
                            'text': comment,
                            'rating': review.get('rate', 0),
                            'date': review.get('lastModifiedDate', ''),
                            'helpful': review.get('voteCount', 0)
                        })
                    
                    if page < max_pages:
                        time.sleep(1)  # Polite delay between requests
                    
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error fetching page {page} for product {product_id}: {str(e)}")
                    continue
            
            return reviews
            
        except Exception as e:
            logger.error(f"Error getting reviews: {str(e)}")
            return []

    def analyze_sentiment(self, text):
        try:
            # Using TextBlob for sentiment analysis with Turkish text
            blob = TextBlob(text)
            # Simple rule-based sentiment boosting for Turkish text
            positive_words = ['güzel', 'harika', 'mükemmel', 'iyi', 'başarılı', 'kaliteli']
            negative_words = ['kötü', 'berbat', 'rezalet', 'korkunç', 'başarısız', 'kalitesiz', 'etmez']
            
            base_polarity = blob.sentiment.polarity
            
            # Adjust polarity based on Turkish keywords
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            adjusted_polarity = base_polarity + (0.1 * (positive_count - negative_count))
            return max(min(adjusted_polarity, 1.0), -1.0)  # Clamp between -1 and 1
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return 0

    def extract_topics(self, reviews):
        try:
            # Extract words and their frequencies
            words = []
            for review in reviews:
                # Split text into words and clean them
                text = review['text'].lower()
                text = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', '', text)  # Keep Turkish characters
                words.extend([
                    word for word in text.split()
                    if word not in self.stopwords and len(word) > 2
                ])
            
            # Get most common topics
            return Counter(words).most_common(5)
        except Exception as e:
            logger.error(f"Error extracting topics: {str(e)}")
            return []

    def analyze_product(self, product_url):
        try:
            reviews = self.get_product_reviews(product_url)
            if not reviews:
                raise ValueError("Bu ürün için yorum bulunamadı. Lütfen URL'yi kontrol edin ve ürünün yorumları olduğundan emin olun.")
            
            if len(reviews) == 0:
                raise ValueError("Bu ürün için yorum bulunamadı.")

            logger.info(f"Found {len(reviews)} reviews for analysis")
            sentiments = []
            for review in reviews:
                sentiment = self.analyze_sentiment(review['text'])
                sentiments.append(sentiment)

            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            topics = self.extract_topics(reviews)

            return {
                'avg_sentiment': avg_sentiment,
                'total_reviews': len(reviews),
                'top_topics': topics,
                'positive_count': sum(1 for s in sentiments if s > 0),
                'negative_count': sum(1 for s in sentiments if s < 0),
                'neutral_count': sum(1 for s in sentiments if s == 0),
                'reviews': [{
                    'text': r['text'],
                    'rating': r['rating'],
                    'sentiment': s
                } for r, s in zip(reviews[:5], sentiments[:5])]  # Include first 5 reviews
            }
        except Exception as e:
            logger.error(f"Error analyzing product: {str(e)}")
            raise

analyzer = TrendyolSentimentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'urls' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        results = {}
        for url in data['urls'][:10]:
            try:
                result = analyzer.analyze_product(url)
                if result:
                    results[url] = result
            except Exception as e:
                logger.error(f"Error analyzing URL {url}: {str(e)}")
                results[url] = {'error': str(e)}
        
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.get_json()
        if not data or 'products' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        results = []
        for product in data['products'][:10]:
            try:
                result = analyzer.analyze_product(product['url'])
                if result:
                    result['name'] = product['name']
                    results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing product {product['name']}: {str(e)}")
                results.append({
                    'name': product['name'],
                    'error': str(e)
                })

        # Check if we have any successful analyses
        successful_results = [r for r in results if 'error' not in r]
        if not successful_results:
            error_messages = [r.get('error', 'Bilinmeyen hata') for r in results if 'error' in r]
            return jsonify({
                'error': 'Hiçbir ürün analiz edilemedi',
                'details': error_messages
            }), 500

        # Create comparison visualizations
        sentiment_df = pd.DataFrame([{
            'Product': r['name'],
            'Sentiment': r.get('avg_sentiment', 0),
            'Reviews': r.get('total_reviews', 0)
        } for r in results if 'error' not in r])
        
        sentiment_fig = px.bar(sentiment_df, x='Product', y='Sentiment',
                              title='Ürün Yorumları Duygu Analizi Karşılaştırması',
                              labels={'Product': 'Ürün', 'Sentiment': 'Duygu Puanı'},
                              text='Reviews',  # Show review count on bars
                              hover_data=['Reviews'])
        
        sentiment_fig.update_traces(texttemplate='%{text} yorum', textposition='outside')
        
        return jsonify({
            'results': results,
            'visualizations': {
                'sentiment_comparison': sentiment_fig.to_json()
            }
        })
    except Exception as e:
        logger.error(f"Error in compare endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
