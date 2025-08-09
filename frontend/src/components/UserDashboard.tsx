'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface AnalysisHistoryItem {
  id: number;
  influencer_username: string;
  platform: string;
  overall_score: number;
  created_at: string;
}

interface WatchlistItem {
  id: number;
  influencer_username: string;
  platform: string;
  added_at: string;
}

export default function UserDashboard() {
  const { user, token } = useAuth();
  const [analysisHistory, setAnalysisHistory] = useState<AnalysisHistoryItem[]>([]);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && token) {
      fetchUserData();
    }
  }, [user, token]);

  const fetchUserData = async () => {
    try {
      const headers = {
        'Authorization': `Bearer ${token}`,
      };

      // Fetch analysis history
      const historyResponse = await fetch('http://localhost:8000/api/user/history?limit=5', {
        headers,
      });
      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setAnalysisHistory(historyData);
      }

      // Fetch watchlist
      const watchlistResponse = await fetch('http://localhost:8000/api/user/watchlist', {
        headers,
      });
      if (watchlistResponse.ok) {
        const watchlistData = await watchlistResponse.json();
        setWatchlist(watchlistData);
      }
    } catch (error) {
      console.error('Failed to fetch user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFromWatchlist = async (watchlistId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/user/watchlist/${watchlistId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setWatchlist(prev => prev.filter(item => item.id !== watchlistId));
      }
    } catch (error) {
      console.error('Failed to remove from watchlist:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getScoreClass = (score: number) => {
    if (score >= 8.5) return 'text-success';
    if (score >= 7.0) return 'text-info';
    if (score >= 5.0) return 'text-warning';
    return 'text-danger';
  };

  if (!user) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <h2>Please sign in to view your dashboard</h2>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <div className="loading-spinner mx-auto"></div>
          <p className="mt-3">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="row">
        <div className="col-12 mb-4">
          <h1>Welcome back, {user.full_name || user.username}! 👋</h1>
          <p className="text-muted">Here's your influencer analysis activity</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-5">
        <div className="col-md-4 mb-3">
          <div className="card metric-card">
            <div className="card-body text-center">
              <h3 className="text-primary">{user.analysis_count || 0}</h3>
              <p className="text-muted mb-0">Analyses Performed</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card metric-card">
            <div className="card-body text-center">
              <h3 className="text-primary">{user.watchlist_count || 0}</h3>
              <p className="text-muted mb-0">Influencers Watched</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-3">
          <div className="card metric-card">
            <div className="card-body text-center">
              <h3 className="text-primary">{user.is_verified ? '✓' : '○'}</h3>
              <p className="text-muted mb-0">Account Status</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Recent Analysis History */}
        <div className="col-lg-8 mb-4">
          <div className="card metric-card">
            <div className="card-header bg-transparent">
              <h5 className="mb-0">📈 Recent Analysis History</h5>
            </div>
            <div className="card-body">
              {analysisHistory.length > 0 ? (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Influencer</th>
                        <th>Platform</th>
                        <th>Score</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysisHistory.map((analysis) => (
                        <tr key={analysis.id}>
                          <td>
                            <strong>@{analysis.influencer_username}</strong>
                          </td>
                          <td>
                            <span className="badge bg-secondary text-capitalize">
                              {analysis.platform}
                            </span>
                          </td>
                          <td>
                            <span className={`fw-bold ${getScoreClass(analysis.overall_score)}`}>
                              {analysis.overall_score}/10
                            </span>
                          </td>
                          <td className="text-muted">
                            {formatDate(analysis.created_at)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-muted text-center py-4">
                  No analysis history yet. Start analyzing influencers to see your history here!
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Watchlist */}
        <div className="col-lg-4 mb-4">
          <div className="card metric-card">
            <div className="card-header bg-transparent">
              <h5 className="mb-0">⭐ Your Watchlist</h5>
            </div>
            <div className="card-body">
              {watchlist.length > 0 ? (
                <div className="list-group list-group-flush">
                  {watchlist.map((item) => (
                    <div key={item.id} className="list-group-item d-flex justify-content-between align-items-center">
                      <div>
                        <strong>@{item.influencer_username}</strong>
                        <br />
                        <small className="text-muted text-capitalize">{item.platform}</small>
                      </div>
                      <button
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => removeFromWatchlist(item.id)}
                        title="Remove from watchlist"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted text-center py-4">
                  Your watchlist is empty. Add influencers to track their authenticity scores!
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
