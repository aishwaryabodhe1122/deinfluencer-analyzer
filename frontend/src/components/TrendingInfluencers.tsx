'use client';

import { useState, useEffect } from 'react';

interface TrendingInfluencer {
  username: string;
  platform: string;
  authenticity_score: number;
  follower_count: number;
  trend_direction: 'up' | 'down' | 'stable';
}

export default function TrendingInfluencers() {
  const [trending, setTrending] = useState<TrendingInfluencer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrendingInfluencers();
  }, []);

  const fetchTrendingInfluencers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/trending');
      const data = await response.json();
      setTrending(data.trending || []);
    } catch (error) {
      console.error('Failed to fetch trending influencers:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score: number) => {
    if (score >= 8.5) return 'text-success';
    if (score >= 7.0) return 'text-info';
    if (score >= 5.0) return 'text-warning';
    return 'text-danger';
  };

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up': return '📈';
      case 'down': return '📉';
      default: return '➡️';
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  if (loading) {
    return (
      <section className="py-5 bg-light">
        <div className="container">
          <div className="text-center">
            <div className="loading-spinner mx-auto"></div>
            <p className="mt-3 text-muted">Loading trending influencers...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-5 bg-light">
      <div className="container">
        <div className="row">
          <div className="col-12 text-center mb-5">
            <h2 className="display-5 fw-bold">🔥 Trending Authentic Influencers</h2>
            <p className="lead text-muted">
              Discover influencers with high authenticity scores who are currently trending
            </p>
          </div>
        </div>
        
        <div className="row">
          {trending.map((influencer, index) => (
            <div key={index} className="col-md-6 col-lg-4 mb-4">
              <div className="card metric-card h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <div>
                      <h5 className="card-title mb-1">@{influencer.username}</h5>
                      <small className="text-muted text-capitalize">{influencer.platform}</small>
                    </div>
                    <span className="fs-4">{getTrendIcon(influencer.trend_direction)}</span>
                  </div>
                  
                  <div className="mb-3">
                    <div className="d-flex justify-content-between align-items-center">
                      <span className="text-muted">Authenticity Score</span>
                      <span className={`fw-bold ${getScoreClass(influencer.authenticity_score)}`}>
                        {influencer.authenticity_score}/10
                      </span>
                    </div>
                    <div className="progress mt-2">
                      <div 
                        className="progress-bar bg-primary" 
                        style={{ width: `${influencer.authenticity_score * 10}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="d-flex justify-content-between align-items-center">
                    <span className="text-muted">Followers</span>
                    <span className="fw-semibold">{formatNumber(influencer.follower_count)}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {trending.length === 0 && (
          <div className="text-center">
            <p className="text-muted">No trending influencers available at the moment.</p>
          </div>
        )}
      </div>
    </section>
  );
}
