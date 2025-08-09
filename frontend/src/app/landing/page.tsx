'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import authService, { RegisterRequest, LoginRequest } from '../../services/auth';
import './landing.css';

export default function LandingPage() {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [userRole, setUserRole] = useState<'consumer' | 'brand' | 'admin'>('consumer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [showScrollTop, setShowScrollTop] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    username: ''
  });
  const router = useRouter();

  // Handle OAuth and social login error messages from URL params
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const errorType = urlParams.get('error');
    const socialError = urlParams.get('social_error');
    const provider = urlParams.get('provider');
    const errorMessage = urlParams.get('message');
    
    console.log('URL Params Debug:', {
      errorType,
      socialError,
      provider,
      errorMessage,
      fullURL: window.location.href
    });
    
    // Handle OAuth errors (old format - for backward compatibility)
    if (errorType === 'oauth_unavailable' && errorMessage) {
      console.log('Handling old OAuth error format');
      setError(`Social login is not available yet. ${decodeURIComponent(errorMessage)}`);
      setShowAuthModal(true);
      setAuthMode('login');
      
      // Clean up URL params
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
    
    // Handle social login errors (new format)
    if (socialError === 'oauth_unavailable' && errorMessage && provider) {
      console.log('Handling new social error format:', { socialError, provider, errorMessage });
      const providerName = provider.charAt(0).toUpperCase() + provider.slice(1);
      setError(`${providerName} login is not available yet. ${decodeURIComponent(errorMessage)}`);
      setShowAuthModal(true);
      setAuthMode('login');
      
      // Clean up URL params
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
    
    // Handle email verification success
    const verified = urlParams.get('verified');
    if (verified === 'true' && errorMessage) {
      // Show success message for email verification
      setError('');
      // You could add a success state here if needed
      
      // Clean up URL params
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
  }, []);

  // Scroll to top functionality
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 300);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  const handleGetStarted = () => {
    setAuthMode('signup');
    setShowAuthModal(true);
    setError('');
    resetForm();
  };

  const handleLogin = () => {
    setAuthMode('login');
    setShowAuthModal(true);
    setError('');
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      email: '',
      password: '',
      confirmPassword: '',
      name: '',
      username: ''
    });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (error) setError(''); // Clear error when user starts typing
  };

  const validateForm = (): string | null => {
    if (!formData.email || !formData.password) {
      return 'Email and password are required';
    }

    if (authMode === 'signup') {
      if (!formData.name || !formData.username) {
        return 'Name and username are required';
      }
      if (formData.password !== formData.confirmPassword) {
        return 'Passwords do not match';
      }
      if (formData.password.length < 6) {
        return 'Password must be at least 6 characters long';
      }
      if (formData.username.length < 3) {
        return 'Username must be at least 3 characters long';
      }
    }

    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError('');

    try {
      if (authMode === 'login') {
        const loginData: LoginRequest = {
          email: formData.email,
          password: formData.password
        };
        await authService.login(loginData);
      } else {
        const registerData: RegisterRequest = {
          email: formData.email,
          username: formData.username,
          password: formData.password,
          full_name: formData.name,
          role: userRole
        };
        await authService.register(registerData);
      }

      // Redirect to dashboard on success
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSocialLogin = async (provider: string) => {
    try {
      setLoading(true);
      setError('');
      // This will be implemented when we add social auth
      await authService.socialLogin(provider);
      router.push('/dashboard');
    } catch (err: any) {
      setError(`${provider} authentication is not yet available`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`landing-page ${showAuthModal ? 'modal-open' : ''}`}>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="row align-items-center min-vh-100">
            <div className="col-lg-6 hero-content-col">
              <div className="hero-content">
                <div className="hero-badge mb-4">
                  <span className="badge-text">🚀 Next Gen Trust Analysis</span>
                </div>
                <h1 className="hero-title mb-4">
                  Nexora
                  <span className="hero-subtitle d-block">Next Gen Trust Aura</span>
                </h1>
                <p className="hero-description mb-5">
                  Combat fake engagement and misleading promotions with our advanced authenticity analysis. 
                  Get transparent, explainable trust scores for influencers across all major social media platforms.
                </p>
                <div className="hero-buttons">
                  <button 
                    className="btn btn-primary btn-lg me-3 mb-3" 
                    onClick={handleGetStarted}
                  >
                    Get Started Free
                  </button>
                  <button 
                    className="btn btn-outline-light btn-lg mb-3" 
                    onClick={handleLogin}
                  >
                    Sign In
                  </button>
                </div>
              </div>
            </div>
            
            <div className="col-lg-6 hero-visual-col">
              <div className="hero-visual">
                <div className="ai-brain-visualization">
                  {/* Central AI Brain */}
                  <div className="ai-brain">
                    <div className="brain-core">
                      <div className="core-ring ring-1"></div>
                      <div className="core-ring ring-2"></div>
                      <div className="core-ring ring-3"></div>
                      <div className="brain-center">
                        <i className="fas fa-brain"></i>
                      </div>
                    </div>
                  </div>

                  {/* Data Streams */}
                  <div className="data-streams">
                    <div className="stream stream-1">
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                    </div>
                    <div className="stream stream-2">
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                    </div>
                    <div className="stream stream-3">
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                    </div>
                    <div className="stream stream-4">
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                      <div className="data-particle"></div>
                    </div>
                  </div>

                  {/* Social Platform Nodes */}
                  <div className="platform-nodes">
                    <div className="platform-node node-1">
                      <i className="fab fa-instagram"></i>
                      <div className="node-pulse"></div>
                    </div>
                    <div className="platform-node node-2">
                      <i className="fab fa-twitter"></i>
                      <div className="node-pulse"></div>
                    </div>
                    <div className="platform-node node-3">
                      <i className="fab fa-youtube"></i>
                      <div className="node-pulse"></div>
                    </div>
                    <div className="platform-node node-4">
                      <i className="fab fa-tiktok"></i>
                      <div className="node-pulse"></div>
                    </div>
                    <div className="platform-node node-5">
                      <i className="fab fa-meta"></i>
                      <div className="node-pulse"></div>
                    </div>
                    <div className="platform-node node-6">
                      <i className="fab fa-linkedin"></i>
                      <div className="node-pulse"></div>
                    </div>
                  </div>

                  {/* Trust Score Indicators */}
                  <div className="trust-indicators">
                    <div className="trust-badge badge-1">
                      <span className="trust-score">9.2</span>
                      <span className="trust-label">Authentic</span>
                    </div>
                    <div className="trust-badge badge-2">
                      <span className="trust-score">7.8</span>
                      <span className="trust-label">Good</span>
                    </div>
                    <div className="trust-badge badge-3">
                      <span className="trust-score">8.5</span>
                      <span className="trust-label">Verified</span>
                    </div>
                  </div>

                  {/* Background Grid */}
                  <div className="neural-grid">
                    <div className="grid-line grid-h-1"></div>
                    <div className="grid-line grid-h-2"></div>
                    <div className="grid-line grid-h-3"></div>
                    <div className="grid-line grid-v-1"></div>
                    <div className="grid-line grid-v-2"></div>
                    <div className="grid-line grid-v-3"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-12 text-center mb-5">
              <h2 className="section-title">Why Choose Nexora?</h2>
              <p className="section-subtitle">
                Advanced AI technology meets transparent authenticity analysis
              </p>
            </div>
          </div>
          
          <div className="row">
            <div className="col-lg-4 mb-4">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="fas fa-shield-alt"></i>
                </div>
                <h4>Real-Time Analysis</h4>
                <p>
                  Get instant authenticity scores with real-time data from 
                  Instagram, X (Twitter), YouTube, TikTok, and more.
                </p>
              </div>
            </div>
            
            <div className="col-lg-4 mb-4">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="fas fa-brain"></i>
                </div>
                <h4>AI-Powered Insights</h4>
                <p>
                  Advanced machine learning algorithms detect fake engagement, 
                  bot activity, and sponsored content patterns.
                </p>
              </div>
            </div>
            
            <div className="col-lg-4 mb-4">
              <div className="feature-card">
                <div className="feature-icon">
                  <i className="fas fa-chart-line"></i>
                </div>
                <h4>Transparent Scoring</h4>
                <p>
                  Understand exactly how scores are calculated with detailed 
                  breakdowns and actionable recommendations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-12 text-center">
              <h2 className="cta-title mb-4">
                Ready to Discover Authentic Influencers?
              </h2>
              <p className="cta-description mb-4">
                Join thousands of brands and agencies who trust Nexora for 
                authentic influencer partnerships.
              </p>
              <button 
                className="btn btn-primary btn-lg"
                onClick={handleGetStarted}
              >
                Start Your Free Analysis
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Authentication Modal */}
      {showAuthModal && (
        <>
          <div className="modal-backdrop fade show"></div>
          <div className="modal fade show d-block" tabIndex={-1} style={{zIndex: 1055, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: '20px'}}>
            <div className="modal-dialog" style={{margin: '0 auto', maxWidth: '500px', width: '100%', maxHeight: '90vh'}}>
              <div className="modal-content">
              <div className="modal-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <h5 className="modal-title" style={{color: 'white', margin: '0'}}>
                  {authMode === 'login' ? 'Welcome Back' : 'Get Started'}
                </h5>
                <button 
                  type="button" 
                  className="nexora-close-btn"
                  onClick={() => setShowAuthModal(false)}
                  style={{
                    background: '#f5f1e8',
                    border: '3px solid #d4af37',
                    borderRadius: '50%',
                    width: '40px',
                    height: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    visibility: 'visible' as const,
                    opacity: 1,
                    position: 'absolute' as const,
                    top: '15px',
                    right: '15px',
                    zIndex: 99999,
                    fontSize: '24px',
                    fontWeight: 900,
                    color: '#2a2d3a',
                    cursor: 'pointer',
                    boxShadow: '0 4px 12px rgba(212, 175, 55, 0.6)',
                    transition: 'all 0.2s ease',
                    outline: 'none',
                    textAlign: 'center' as const,
                    lineHeight: 1
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#d4af37';
                    e.currentTarget.style.color = '#ffffff';
                    e.currentTarget.style.transform = 'scale(1.15)';
                    e.currentTarget.style.boxShadow = '0 6px 16px rgba(212, 175, 55, 0.8)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = '#f5f1e8';
                    e.currentTarget.style.color = '#2a2d3a';
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.6)';
                  }}
                  aria-label="Close modal"
                >×</button>
              </div>
              <div className="modal-body">

                
                {error && (
                  <div className="alert alert-danger" role="alert">
                    {error}
                  </div>
                )}
                
                <form onSubmit={handleSubmit}>
                  {/* Email field - FORCED VISIBLE */}
                  <div className="mb-3" style={{
                    display: 'block', 
                    visibility: 'visible', 
                    opacity: 1,
                    marginBottom: '1rem'
                  }}>
                    <label htmlFor="email" className="form-label" style={{
                      color: 'white', 
                      display: 'block',
                      fontWeight: 'bold',
                      marginBottom: '0.5rem'
                    }}>Email</label>
                    <input 
                      type="email" 
                      className="form-control" 
                      id="email" 
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required 
                      disabled={loading}
                      style={{
                        display: 'block', 
                        visibility: 'visible', 
                        opacity: 1,
                        width: '100%',
                        padding: '0.75rem',
                        backgroundColor: '#1a1d2a',
                        color: 'white',
                        border: '2px solid #d4af37',
                        borderRadius: '0.5rem'
                      }}
                      placeholder="Enter your email address"
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input 
                      type="password" 
                      className="form-control" 
                      id="password" 
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      required 
                      disabled={loading}
                    />
                  </div>
                  {authMode === 'signup' && (
                    <>
                      <div className="mb-3">
                        <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                        <input 
                          type="password" 
                          className="form-control" 
                          id="confirmPassword" 
                          name="confirmPassword"
                          value={formData.confirmPassword}
                          onChange={handleInputChange}
                          required 
                          disabled={loading}
                        />
                      </div>
                      <div className="mb-3">
                        <label htmlFor="name" className="form-label">Full Name</label>
                        <input 
                          type="text" 
                          className="form-control" 
                          id="name" 
                          name="name"
                          value={formData.name}
                          onChange={handleInputChange}
                          required 
                          disabled={loading}
                        />
                      </div>
                      <div className="mb-3">
                        <label htmlFor="username" className="form-label">Username</label>
                        <input 
                          type="text" 
                          className="form-control" 
                          id="username" 
                          name="username"
                          value={formData.username}
                          onChange={handleInputChange}
                          required 
                          disabled={loading}
                        />
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Account Type</label>
                        <div className="role-selection">
                          <div className="form-check mb-2">
                            <input 
                              className="form-check-input" 
                              type="radio" 
                              name="role" 
                              id="consumer" 
                              value="consumer"
                              checked={userRole === 'consumer'}
                              onChange={(e) => setUserRole(e.target.value as 'consumer' | 'brand' | 'admin')}
                              disabled={loading}
                            />
                            <label className="form-check-label" htmlFor="consumer">
                              <strong>Consumer</strong> - Individual user analyzing influencers
                            </label>
                          </div>
                          <div className="form-check mb-2">
                            <input 
                              className="form-check-input" 
                              type="radio" 
                              name="role" 
                              id="brand" 
                              value="brand"
                              checked={userRole === 'brand'}
                              onChange={(e) => setUserRole(e.target.value as 'consumer' | 'brand' | 'admin')}
                              disabled={loading}
                            />
                            <label className="form-check-label" htmlFor="brand">
                              <strong>Brand/Agency</strong> - Business user for marketing campaigns
                            </label>
                          </div>
                          <small className="form-text text-muted">
                            Admin accounts are assigned manually. Contact support if you need admin access.
                          </small>
                        </div>
                      </div>
                    </>
                  )}
                  <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        {authMode === 'login' ? 'Signing In...' : 'Creating Account...'}
                      </>
                    ) : (
                      authMode === 'login' ? 'Sign In' : 'Create Account'
                    )}
                  </button>
                </form>

                {/* Social Login Section */}
                <div className="text-center my-3">
                  <div className="d-flex align-items-center mb-3">
                    <hr className="flex-grow-1" style={{ borderColor: '#444' }} />
                    <span className="px-3 text-muted small">or continue with</span>
                    <hr className="flex-grow-1" style={{ borderColor: '#444' }} />
                  </div>
                  
                  <div className="d-flex justify-content-center gap-3 flex-wrap">
                    {/* Google */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateGoogleLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with Google"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        borderColor: '#d4af37',
                        color: '#f5f1e8',
                        backgroundColor: '#4285f4',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    >
                      <i className="fab fa-google" style={{ fontSize: '20px', color: 'white' }}></i>
                    </button>
                    
                    {/* GitHub */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateGitHubLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with GitHub"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        borderColor: '#d4af37',
                        color: '#f5f1e8',
                        backgroundColor: '#333',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    >
                      <i className="fab fa-github" style={{ fontSize: '20px', color: 'white' }}></i>
                    </button>
                    
                    {/* Meta */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateFacebookLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with Meta"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        borderColor: '#d4af37',
                        color: '#f5f1e8',
                        background: 'linear-gradient(45deg, #0866ff 0%, #0653d3 50%, #0866ff 100%)',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    >
                      <i className="fab fa-meta" style={{ fontSize: '20px', color: 'white' }}></i>
                    </button>
                    
                    {/* Instagram */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateInstagramLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with Instagram"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        background: 'linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%)',
                        border: 'none',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    >
                      <i className="fab fa-instagram" style={{ fontSize: '20px', color: 'white' }}></i>
                    </button>
                    
                    {/* LinkedIn */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateLinkedInLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with LinkedIn"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        borderColor: '#d4af37',
                        color: '#f5f1e8',
                        backgroundColor: '#0077b5',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}
                    >
                      <i className="fab fa-linkedin-in" style={{ fontSize: '20px', color: 'white' }}></i>
                    </button>
                    
                    {/* X (Twitter) */}
                    <button
                      type="button"
                      className="btn btn-outline-light d-flex align-items-center justify-content-center"
                      onClick={() => {
                        import('../../services/auth').then((AuthService) => {
                          AuthService.default.initiateTwitterLogin();
                        });
                      }}
                      disabled={loading}
                      title="Continue with X (Twitter)"
                      style={{
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        borderColor: '#d4af37',
                        color: '#fff',
                        backgroundColor: '#000',
                        border: '2px solid #d4af37',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
                        e.currentTarget.style.backgroundColor = '#1a1a1a';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                        e.currentTarget.style.boxShadow = 'none';
                        e.currentTarget.style.backgroundColor = '#000';
                      }}
                    >
                      <span style={{ fontSize: '18px', color: '#fff', fontWeight: 'bold', fontFamily: 'Arial, sans-serif' }}>𝕏</span>
                    </button>
                  </div>
                </div>

                <div className="text-center mt-3">
                  <p>
                    {authMode === 'login' ? "Don't have an account? " : "Already have an account? "}
                    <button 
                      className="btn btn-link p-0"
                      onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}
                    >
                      {authMode === 'login' ? 'Sign Up' : 'Sign In'}
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </div>
          </div>
        </>
      )}
      
      {/* Scroll to Top Button */}
      <button 
        className={`scroll-to-top ${showScrollTop ? 'visible' : ''}`}
        onClick={scrollToTop}
        aria-label="Scroll to top"
      >
        <i className="fas fa-chevron-up"></i>
      </button>
    </div>
  );
}
