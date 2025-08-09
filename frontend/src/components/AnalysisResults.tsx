'use client';

import { AnalysisData } from '@/app/page';

interface AnalysisResultsProps {
  data: AnalysisData;
}

export default function AnalysisResults({ data }: AnalysisResultsProps) {
  const { profile, authenticity_score, insights, recommendations } = data;

  const getScoreClass = (score: number) => {
    if (score >= 8.5) return 'score-excellent';
    if (score >= 7.0) return 'score-good';
    if (score >= 5.0) return 'score-moderate';
    return 'score-poor';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 8.5) return 'Excellent';
    if (score >= 7.0) return 'Good';
    if (score >= 5.0) return 'Moderate';
    return 'Poor';
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatFollowerRatio = (followers: number, following: number) => {
    if (following === 0) {
      return '∞'; // Infinity symbol for 0 following
    }
    
    const ratio = followers / following;
    
    // For very high ratios, show in a more readable format
    if (ratio >= 1000000) {
      return (ratio / 1000000).toFixed(1) + 'M:1';
    } else if (ratio >= 1000) {
      return (ratio / 1000).toFixed(1) + 'K:1';
    } else if (ratio >= 100) {
      return Math.round(ratio).toString() + ':1';
    } else {
      return ratio.toFixed(1) + ':1';
    }
  };

  return (
    <section className="py-5">
      <div className="container">
        {/* Profile Header */}
        <div className="row mb-5">
          <div className="col-12">
            <div className="card metric-card">
              <div className="card-body p-4">
                <div className="row align-items-center">
                  <div className="col-md-8">
                    <div className="d-flex align-items-center mb-3">
                      <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" 
                           style={{ width: '60px', height: '60px' }}>
                        <span className="text-white fw-bold fs-4">
                          {profile.username.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div>
                        <h2 className="mb-1">
                          @{profile.username}
                          {profile.verified && (
                            <span className="badge bg-primary ms-2">✓ Verified</span>
                          )}
                        </h2>
                        <p className="text-muted mb-0 text-capitalize">
                          {profile.platform} • {formatNumber(profile.follower_count)} followers
                        </p>
                      </div>
                    </div>
                    {profile.bio && (
                      <p className="text-muted mb-0">{profile.bio}</p>
                    )}
                  </div>
                  <div className="col-md-4 text-md-end">
                    <div className="text-center">
                      <div className={`authenticity-score ${getScoreClass(authenticity_score.overall_score)}`}>
                        {authenticity_score.overall_score}/10
                      </div>
                      <div className="fw-semibold text-muted">
                        {getScoreLabel(authenticity_score.overall_score)} Authenticity
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="row mb-5">
          <div className="col-md-6 col-lg-3 mb-4">
            <div className="card metric-card h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-muted">Engagement Quality</h5>
                <div className={`h3 ${getScoreClass(authenticity_score.engagement_quality)}`}>
                  {authenticity_score.engagement_quality}/10
                </div>
                <div className="progress mt-3">
                  <div 
                    className="progress-bar" 
                    style={{ width: `${authenticity_score.engagement_quality * 10}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="col-md-6 col-lg-3 mb-4">
            <div className="card metric-card h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-muted">Content Authenticity</h5>
                <div className={`h3 ${getScoreClass(authenticity_score.content_authenticity)}`}>
                  {authenticity_score.content_authenticity}/10
                </div>
                <div className="progress mt-3">
                  <div 
                    className="progress-bar" 
                    style={{ width: `${authenticity_score.content_authenticity * 10}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="col-md-6 col-lg-3 mb-4">
            <div className="card metric-card h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-muted">Follower Authenticity</h5>
                <div className={`h3 ${getScoreClass(authenticity_score.follower_authenticity)}`}>
                  {authenticity_score.follower_authenticity}/10
                </div>
                <div className="progress mt-3">
                  <div 
                    className="progress-bar" 
                    style={{ width: `${authenticity_score.follower_authenticity * 10}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="col-md-6 col-lg-3 mb-4">
            <div className="card metric-card h-100">
              <div className="card-body text-center">
                <h5 className="card-title text-muted">Sponsored Ratio</h5>
                <div className={`h3 ${getScoreClass(authenticity_score.sponsored_ratio)}`}>
                  {authenticity_score.sponsored_ratio}/10
                </div>
                <div className="progress mt-3">
                  <div 
                    className="progress-bar" 
                    style={{ width: `${authenticity_score.sponsored_ratio * 10}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Insights and Recommendations */}
        <div className="row">
          <div className="col-lg-6 mb-4">
            <div className="card metric-card h-100">
              <div className="card-header bg-transparent">
                <h5 className="mb-0">🔍 Key Insights</h5>
              </div>
              <div className="card-body">
                {insights.length > 0 ? (
                  <ul className="list-unstyled">
                    {insights.map((insight, index) => (
                      <li key={index} className="mb-2">
                        <span className="text-primary me-2">•</span>
                        {insight}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-muted">No specific insights available.</p>
                )}
              </div>
            </div>
          </div>
          
          <div className="col-lg-6 mb-4">
            <div className="card metric-card h-100">
              <div className="card-header bg-transparent">
                <h5 className="mb-0">💡 Recommendations</h5>
              </div>
              <div className="card-body">
                {recommendations.length > 0 ? (
                  <ul className="list-unstyled">
                    {recommendations.map((recommendation, index) => (
                      <li key={index} className="mb-2">
                        <span className="text-warning me-2">•</span>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-muted">No specific recommendations available.</p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Profile Stats */}
        <div className="row mt-4">
          <div className="col-12">
            <div className="card metric-card">
              <div className="card-header bg-transparent">
                <h5 className="mb-0">📊 Profile Statistics</h5>
              </div>
              <div className="card-body">
                <div className="row text-center">
                  <div className="col-md-3">
                    <div className="h4 text-primary">{formatNumber(profile.follower_count)}</div>
                    <div className="text-muted">Followers</div>
                  </div>
                  <div className="col-md-3">
                    <div className="h4 text-primary">{formatNumber(profile.following_count)}</div>
                    <div className="text-muted">Following</div>
                  </div>
                  <div className="col-md-3">
                    <div className="h4 text-primary">{formatNumber(profile.post_count)}</div>
                    <div className="text-muted">Posts</div>
                  </div>
                  <div className="col-md-3">
                    <div className="h4 text-primary">
                      {formatFollowerRatio(profile.follower_count, profile.following_count)}
                    </div>
                    <div className="text-muted">Follower Ratio</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
