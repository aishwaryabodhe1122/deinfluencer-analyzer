'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import AuthService, { User } from '../../services/auth';

interface AnalysisRecord {
  id: number;
  influencer_username: string;
  platform: string;
  overall_score: number;
  engagement_quality: number;
  content_authenticity: number;
  sponsored_ratio: number;
  follower_authenticity: number;
  consistency_score: number;
  analyzed_at: string;
  insights: string[];
  recommendations: string[];
}

export default function AnalysisHistoryPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([]);
  const [filteredAnalyses, setFilteredAnalyses] = useState<AnalysisRecord[]>([]);
  const [selectedPlatform, setSelectedPlatform] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'date' | 'score'>('date');
  const [showPlatformFilter, setShowPlatformFilter] = useState(false);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    const currentUser = AuthService.getUser();
    if (!currentUser) {
      router.push('/landing');
      return;
    }
    
    setUser(currentUser);
    loadAnalysisHistory();
    setLoading(false);
  }, [router]);

  useEffect(() => {
    filterAndSortAnalyses();
  }, [analyses, selectedPlatform, sortBy, searchTerm]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowPlatformFilter(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const loadAnalysisHistory = async () => {
    try {
      // Load real analysis history from backend
      const historyData = await AuthService.getAnalysisHistory({
        limit: 50,
        offset: 0
      });
      
      setAnalyses(historyData);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load analysis history');
    }
  };

  const filterAndSortAnalyses = async () => {
    try {
      // Use backend filtering when possible for better performance
      const filters: any = {
        limit: 50,
        offset: 0
      };
      
      if (selectedPlatform !== 'all') {
        filters.platform = selectedPlatform;
      }
      
      if (searchTerm) {
        filters.search = searchTerm;
      }
      
      if (sortBy) {
        filters.sort_by = sortBy;
      }
      
      const historyData = await AuthService.getAnalysisHistory(filters);
      setFilteredAnalyses(historyData);
    } catch (err: any) {
      // Fallback to client-side filtering if backend filtering fails
      let filtered = analyses;

      // Filter by platform
      if (selectedPlatform !== 'all') {
        filtered = filtered.filter(analysis => analysis.platform === selectedPlatform);
      }

      // Filter by search term
      if (searchTerm) {
        filtered = filtered.filter(analysis => 
          analysis.influencer_username.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      // Sort
      filtered = filtered.sort((a, b) => {
        if (sortBy === 'date') {
          return new Date(b.analyzed_at).getTime() - new Date(a.analyzed_at).getTime();
        } else {
          return b.overall_score - a.overall_score;
        }
      });

      setFilteredAnalyses(filtered);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8.5) return 'text-success';
    if (score >= 7.0) return 'text-warning';
    return 'text-danger';
  };

  const getScoreBadgeClass = (score: number) => {
    if (score >= 8.5) return 'bg-success';
    if (score >= 7.0) return 'bg-warning';
    return 'bg-danger';
  };

  const getPlatformIcon = (platform: string) => {
    const icons: { [key: string]: string } = {
      instagram: 'fab fa-instagram',
      youtube: 'fab fa-youtube',
      twitter: 'fab fa-x-twitter',
      facebook: 'fab fa-meta',
      linkedin: 'fab fa-linkedin',
      tiktok: 'fab fa-tiktok'
    };
    return icons[platform] || 'fas fa-globe';
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading analysis history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100 d-flex flex-column">
      <Navbar />
      
      <main className="flex-grow-1" style={{ backgroundColor: '#1a1d29', minHeight: '100vh' }}>
        <div className="container-fluid py-4">
          <div className="row">
            <div className="col-12">
              <div className="d-flex align-items-center justify-content-between mb-4">
                <div>
                  <h2 className="mb-1" style={{ color: '#f5f1e8' }}>
                    <i className="fas fa-history text-warning me-2"></i>
                    Analysis History
                  </h2>
                  <p className="mb-0" style={{ color: '#a0a3b1' }}>View your past influencer authenticity analyses</p>
                </div>
                <div className="badge bg-warning fs-6 px-3 py-2" style={{ color: '#1a1d29' }}>
                  {filteredAnalyses.length} Total Analyses
                </div>
              </div> {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              {/* Filters and Search */}
              <div className="card mb-4" style={{ backgroundColor: '#2a2d3a', border: '1px solid #d4af37' }}>
                <div className="card-body">
                  <div className="row g-3">
                    <div className="col-md-4">
                      <label htmlFor="search" className="form-label" style={{ color: '#f5f1e8' }}>Search Influencer</label>
                      <div className="input-group">
                        <span className="input-group-text" style={{ backgroundColor: '#3a3d4a', border: '1px solid #d4af37', color: '#f5f1e8' }}>
                          <i className="fas fa-search"></i>
                        </span>
                        <input
                          type="text"
                          className="form-control"
                          id="search"
                          placeholder="Search by username..."
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          style={{ backgroundColor: '#3a3d4a', border: '1px solid #d4af37', color: '#f5f1e8' }}
                        />
                      </div>
                    </div>
                    <div className="col-md-4">
                      <label htmlFor="platform" className="form-label" style={{ color: '#f5f1e8' }}>Platform</label>
                      <div className="custom-dropdown" style={{ position: 'relative' }} ref={dropdownRef}>
                         <button 
                          type="button"
                          className="btn form-select"
                          style={{
                            backgroundColor: '#2a2d3a',
                            border: '1px solid #d4af37',
                            color: '#f5f1e8',
                            fontSize: '14px',
                            padding: '8px 12px',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            minHeight: '38px',
                            width: '100%',
                            textAlign: 'left',
                            zIndex: 1001
                          }}
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('History dropdown clicked, current state:', showPlatformFilter);
                            setShowPlatformFilter(prev => !prev);
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <i 
                              className={selectedPlatform === 'all' ? 'fas fa-globe' : `fab ${
                                selectedPlatform === 'instagram' ? 'fa-instagram' :
                                selectedPlatform === 'twitter' ? 'fa-twitter' :
                                selectedPlatform === 'tiktok' ? 'fa-tiktok' :
                                selectedPlatform === 'youtube' ? 'fa-youtube' :
                                selectedPlatform === 'facebook' ? 'fa-meta' :
                                selectedPlatform === 'linkedin' ? 'fa-linkedin' : 'fa-globe'
                              }`}
                              style={{ color: '#6c757d', fontSize: '14px' }}
                            ></i>
                            <span>
                              {selectedPlatform === 'all' ? 'All Platforms' :
                               selectedPlatform === 'instagram' ? 'Instagram' :
                               selectedPlatform === 'twitter' ? 'X (Twitter)' :
                               selectedPlatform === 'tiktok' ? 'TikTok' :
                               selectedPlatform === 'youtube' ? 'YouTube' :
                               selectedPlatform === 'facebook' ? 'Meta' :
                               selectedPlatform === 'linkedin' ? 'LinkedIn' : 'All Platforms'}
                            </span>
                          </div>
                          <i 
                            className={`fas fa-chevron-${showPlatformFilter ? 'up' : 'down'}`} 
                            style={{ color: '#6c757d', fontSize: '10px' }}
                          ></i>
                        </button>
                        
                        {showPlatformFilter && (
                          <div 
                            className="dropdown-menu show"
                            style={{
                              position: 'absolute',
                              top: '100%',
                              left: 0,
                              right: 0,
                              backgroundColor: '#2a2d3a',
                              border: '1px solid #d4af37',
                              borderTop: 'none',
                              borderRadius: '0 0 6px 6px',
                              zIndex: 1002,
                              maxHeight: '250px',
                              overflowY: 'auto',
                              boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
                              display: 'block',
                              minHeight: '200px'
                            }}
                          >
                            {[
                              { value: 'all', label: 'All Platforms', icon: 'fas fa-globe' },
                              { value: 'instagram', label: 'Instagram', icon: 'fab fa-instagram' },
                              { value: 'youtube', label: 'YouTube', icon: 'fab fa-youtube' },
                              { value: 'twitter', label: 'X (Twitter)', icon: 'fab fa-twitter' },
                              { value: 'facebook', label: 'Meta', icon: 'fab fa-meta' },
                              { value: 'linkedin', label: 'LinkedIn', icon: 'fab fa-linkedin' },
                              { value: 'tiktok', label: 'TikTok', icon: 'fab fa-tiktok' }
                            ].map((option, index) => {console.log('Rendering option:', option); return (
                              <button
                                key={option.value}
                                type="button"
                                className="dropdown-item"
                                style={{
                                  padding: '10px 12px',
                                  cursor: 'pointer',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '8px',
                                  color: '#f5f1e8',
                                  backgroundColor: selectedPlatform === option.value ? '#d4af37' : 'transparent',
                                  borderBottom: '1px solid #3a3d4a',
                                  border: 'none',
                                  width: '100%',
                                  textAlign: 'left'
                                }}
                                onClick={(e) => {
                                  e.preventDefault();
                                  e.stopPropagation();
                                  console.log('History option clicked:', option.value);
                                  setSelectedPlatform(option.value);
                                  setShowPlatformFilter(false);
                                }}
                                onMouseEnter={(e) => {
                                  if (selectedPlatform !== option.value) {
                                    e.currentTarget.style.backgroundColor = '#3a3d4a';
                                  }
                                }}
                                onMouseLeave={(e) => {
                                  if (selectedPlatform !== option.value) {
                                    e.currentTarget.style.backgroundColor = 'transparent';
                                  }
                                }}
                              >
                                <i className={option.icon} style={{ color: '#d4af37', fontSize: '14px' }}></i>
                                <span style={{ color: '#f5f1e8' }}>{option.label}</span>
                              </button>
                            )})}
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="col-md-4">
                      <label htmlFor="sort" className="form-label">Sort By</label>
                      <select
                        className="form-select"
                        id="sort"
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value as 'date' | 'score')}
                      >
                        <option value="date">Most Recent</option>
                        <option value="score">Highest Score</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Analysis Results */}
              {filteredAnalyses.length === 0 ? (
                <div className="card">
                  <div className="card-body text-center py-5">
                    <i className="fas fa-search fa-3x text-muted mb-3"></i>
                    <h5>No analyses found</h5>
                    <p className="text-muted">
                      {searchTerm || selectedPlatform !== 'all' 
                        ? 'Try adjusting your filters or search term.'
                        : 'Start analyzing influencers to see your history here.'}
                    </p>
                    <a href="/dashboard" className="btn btn-primary">
                      <i className="fas fa-plus me-2"></i>
                      Analyze Influencer
                    </a>
                  </div>
                </div>
              ) : (
                <div className="row">
                  {filteredAnalyses.map(analysis => (
                    <div key={analysis.id} className="col-md-6 col-lg-4 mb-4">
                      <div className="card h-100">
                        <div className="card-header d-flex align-items-center justify-content-between">
                          <div className="d-flex align-items-center">
                            <i className={`${getPlatformIcon(analysis.platform)} me-2`}></i>
                            <strong>@{analysis.influencer_username}</strong>
                          </div>
                          <span className={`badge ${getScoreBadgeClass(analysis.overall_score)}`}>
                            {analysis.overall_score.toFixed(1)}
                          </span>
                        </div>
                        <div className="card-body">
                          <div className="row g-2 mb-3">
                            <div className="col-6">
                              <small className="text-muted">Engagement</small>
                              <div className={`fw-medium ${getScoreColor(analysis.engagement_quality)}`}>
                                {analysis.engagement_quality.toFixed(1)}/10
                              </div>
                            </div>
                            <div className="col-6">
                              <small className="text-muted">Content</small>
                              <div className={`fw-medium ${getScoreColor(analysis.content_authenticity)}`}>
                                {analysis.content_authenticity.toFixed(1)}/10
                              </div>
                            </div>
                            <div className="col-6">
                              <small className="text-muted">Followers</small>
                              <div className={`fw-medium ${getScoreColor(analysis.follower_authenticity)}`}>
                                {analysis.follower_authenticity.toFixed(1)}/10
                              </div>
                            </div>
                            <div className="col-6">
                              <small className="text-muted">Consistency</small>
                              <div className={`fw-medium ${getScoreColor(analysis.consistency_score)}`}>
                                {analysis.consistency_score.toFixed(1)}/10
                              </div>
                            </div>
                          </div>

                          <div className="mb-3">
                            <small className="text-muted d-block mb-1">Key Insights</small>
                            <ul className="list-unstyled mb-0">
                              {analysis.insights.slice(0, 2).map((insight, index) => (
                                <li key={index} className="small mb-1">
                                  <i className="fas fa-check-circle text-success me-1"></i>
                                  {insight}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                        <div className="card-footer">
                          <div className="d-flex align-items-center justify-content-between">
                            <small className="text-muted">
                              {analysis.analyzed_at ? 
                                new Date(analysis.analyzed_at).toLocaleDateString() : 
                                'Recent Analysis'
                              }
                            </small>
                            <button 
                              className="btn btn-outline-warning btn-sm"
                              onClick={() => {
                                // Create a simple modal or alert with analysis details
                                alert(`Analysis Details for @${analysis.influencer_username}\n\nOverall Score: ${analysis.overall_score.toFixed(1)}/10\nPlatform: ${analysis.platform}\n\nDetailed Scores:\n- Engagement Quality: ${analysis.engagement_quality.toFixed(1)}/10\n- Content Authenticity: ${analysis.content_authenticity.toFixed(1)}/10\n- Follower Authenticity: ${analysis.follower_authenticity.toFixed(1)}/10\n- Consistency Score: ${analysis.consistency_score.toFixed(1)}/10\n\nKey Insights:\n${analysis.insights.join('\n- ')}\n\nRecommendations:\n${analysis.recommendations.join('\n- ')}`);
                              }}
                            >
                              <i className="fas fa-eye me-1"></i>
                              View Details
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
