'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import SearchSection from '../../components/SearchSection';
import AnalysisResults from '../../components/AnalysisResults';
import TrendingInfluencers from '../../components/TrendingInfluencers';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import AuthService, { User } from '../../services/auth';
// Removed axios import - using native fetch instead
import './dashboard.css';

interface AnalysisData {
  profile: {
    username: string;
    platform: string;
    followers_count: number;
    following_count: number;
    posts_count: number;
    engagement_rate: number;
    is_verified: boolean;
    bio: string;
    profile_image_url: string;
  };
  authenticity_score: {
    overall_score: number;
    engagement_quality: number;
    content_authenticity: number;
    sponsored_ratio: number;
    follower_authenticity: number;
    consistency_score: number;
  };
  insights: string[];
  recommendations: string[];
}

export default function DashboardPage() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      router.push('/landing');
      return;
    }
    
    // Get user information
    const currentUser = AuthService.getUser();
    if (currentUser) {
      setUser(currentUser);
      setIsAuthenticated(true);
    } else {
      router.push('/landing');
    }
  }, [router]);

  const getRoleBasedWelcomeMessage = (role?: string) => {
    switch (role) {
      case 'admin':
        return 'Manage users, monitor system performance, and oversee platform operations.';
      case 'brand':
        return 'Discover authentic influencers for your campaigns with advanced analytics and reporting.';
      case 'consumer':
        return 'Analyze influencer authenticity and discover trustworthy content creators.';
      default:
        return 'Next-Gen Trust Aura - Discover authentic influencers with AI-powered analysis';
    }
  };

  const handleAnalysis = async (username: string, platform: string) => {
    setLoading(true);
    setError('');
    setAnalysisData(null);

    try {
      const token = localStorage.getItem('nexora_token');
      const headers: any = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          username,
          platform
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      const analysisResult = await response.json();
      setAnalysisData(analysisResult);
    } catch (err: any) {
      console.error('Analysis error:', err);
      
      // Handle different types of errors
      if (err.message) {
        setError(err.message);
      } else {
        setError('Username is invalid or the account does not exist.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Checking authentication...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page min-vh-100 d-flex flex-column">
      <Navbar />
      
      <main className="flex-grow-1">
        {/* Welcome Section */}
        <section className="welcome-section">
          <div className="container">
            <div className="row">
              <div className="col-12 text-center">
                <h1 className="welcome-title display-4 fw-bold mb-3">
                  Welcome back, {user?.full_name || user?.username}!
                </h1>
                <p className="welcome-description lead mb-3">
                  {getRoleBasedWelcomeMessage(user?.role)}
                </p>
                <span className="role-badge">
                  <i className="fas fa-user-tag me-2"></i>
                  {user?.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : 'User'} Account
                </span>
              </div>
            </div>
          </div>
        </section>
        
        <div className="container py-4">
          <div className="row">
            <div className="col-12">
              
              {/* Role-based Quick Actions */}
              {user?.role === 'admin' && (
                <div className="row mb-4">
                  <div className="col-12">
                    <div className="card quick-actions-card admin-card">
                      <div className="card-body">
                        <h5 className="card-title">
                          <i className="fas fa-shield-alt me-2"></i>
                          Admin Control Panel
                        </h5>
                        <p className="card-text">
                          Manage users, monitor system performance, and access administrative tools.
                        </p>
                        <div className="d-flex gap-2">
                          <button 
                            className="btn btn-outline-danger btn-sm"
                            onClick={() => router.push('/admin')}
                          >
                            <i className="fas fa-users-cog me-1"></i>
                            User Management
                          </button>
                          <button className="btn btn-outline-danger btn-sm">
                            <i className="fas fa-chart-line me-1"></i>
                            System Analytics
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {user?.role === 'brand' && (
                <div className="row mb-4">
                  <div className="col-12">
                    <div className="card quick-actions-card brand-card">
                      <div className="card-body">
                        <h5 className="card-title">
                          <i className="fas fa-briefcase me-2"></i>
                          Brand/Agency Features
                        </h5>
                        <p className="card-text">
                          Access advanced analytics, bulk analysis tools, and campaign management features.
                        </p>
                        <div className="d-flex gap-2">
                          <button className="btn btn-outline-primary btn-sm">
                            <i className="fas fa-chart-bar me-1"></i>
                            Campaign Analytics
                          </button>
                          <button className="btn btn-outline-primary btn-sm">
                            <i className="fas fa-download me-1"></i>
                            Export Reports
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {user?.role === 'consumer' && (
                <div className="row mb-4">
                  <div className="col-12">
                    <div className="card quick-actions-card consumer-card">
                      <div className="card-body">
                        <h5 className="card-title">
                          <i className="fas fa-search me-2"></i>
                          Consumer Tools
                        </h5>
                        <p className="card-text">
                          Discover authentic influencers and analyze content quality with our AI-powered tools.
                        </p>
                        <div className="d-flex gap-2">
                          <button 
                            className="btn btn-outline-success btn-sm"
                            onClick={() => router.push('/history')}
                          >
                            <i className="fas fa-history me-1"></i>
                            Analysis History
                          </button>
                          <button className="btn btn-outline-success btn-sm">
                            <i className="fas fa-bookmark me-1"></i>
                            Saved Influencers
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <SearchSection 
                onAnalyze={handleAnalysis} 
                isLoading={loading}
                error={error}
              />
              
              {analysisData && (
                <AnalysisResults data={analysisData} />
              )}
              
              <TrendingInfluencers />
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
