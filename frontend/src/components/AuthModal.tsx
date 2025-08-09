'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import AuthService from '@/services/auth';

interface AuthModalProps {
  show: boolean;
  onHide: () => void;
  initialMode?: 'login' | 'register';
}

export default function AuthModal({ show, onHide, initialMode = 'login' }: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'register'>(initialMode);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    fullName: '',
    confirmPassword: ''
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const { login, register, isLoading, error } = useAuth();
  const router = useRouter();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const errors: Record<string, string> = {};

    if (!formData.email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email is invalid';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters';
    }

    if (mode === 'register') {
      if (!formData.username) {
        errors.username = 'Username is required';
      } else if (formData.username.length < 3) {
        errors.username = 'Username must be at least 3 characters';
      }

      if (formData.password !== formData.confirmPassword) {
        errors.confirmPassword = 'Passwords do not match';
      }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      if (mode === 'login') {
        await login(formData.email, formData.password);
        // Reset form and close modal on successful login
        setFormData({
          email: '',
          username: '',
          password: '',
          fullName: '',
          confirmPassword: ''
        });
        onHide();
      } else {
        await register(formData.email, formData.username, formData.password, formData.fullName);
        // Redirect to email verification page after successful registration
        onHide();
        router.push(`/verify-email?email=${encodeURIComponent(formData.email)}`);
      }
    } catch (err) {
      // Error is handled by the auth context
    }
  };

  const switchMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
    setFormErrors({});
  };

  if (!show) return null;

  return (
    <div className="modal show d-block" tabIndex={-1} style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              {mode === 'login' ? 'Sign In' : 'Create Account'}
            </h5>
            <button
              type="button"
              className="btn-close"
              onClick={onHide}
              disabled={isLoading}
            ></button>
          </div>
          
          <div className="modal-body">
            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email address</label>
                <input
                  type="email"
                  className={`form-control ${formErrors.email ? 'is-invalid' : ''}`}
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  disabled={isLoading}
                  required
                />
                {formErrors.email && (
                  <div className="invalid-feedback">{formErrors.email}</div>
                )}
              </div>

              {mode === 'register' && (
                <>
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                      type="text"
                      className={`form-control ${formErrors.username ? 'is-invalid' : ''}`}
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleInputChange}
                      disabled={isLoading}
                      required
                    />
                    {formErrors.username && (
                      <div className="invalid-feedback">{formErrors.username}</div>
                    )}
                  </div>

                  <div className="mb-3">
                    <label htmlFor="fullName" className="form-label">Full Name (Optional)</label>
                    <input
                      type="text"
                      className="form-control"
                      id="fullName"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleInputChange}
                      disabled={isLoading}
                    />
                  </div>
                </>
              )}

              <div className="mb-3">
                <label htmlFor="password" className="form-label">Password</label>
                <input
                  type="password"
                  className={`form-control ${formErrors.password ? 'is-invalid' : ''}`}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  disabled={isLoading}
                  required
                />
                {formErrors.password && (
                  <div className="invalid-feedback">{formErrors.password}</div>
                )}
                {mode === 'login' && (
                  <div className="text-end">
                    <button
                      type="button"
                      className="btn btn-link p-0 text-decoration-none small"
                      onClick={() => {
                        onHide();
                        router.push('/reset-password');
                      }}
                      disabled={isLoading}
                      style={{ color: '#fbbf24' }}
                    >
                      Forgot Password?
                    </button>
                  </div>
                )}
              </div>

              {mode === 'register' && (
                <div className="mb-3">
                  <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                  <input
                    type="password"
                    className={`form-control ${formErrors.confirmPassword ? 'is-invalid' : ''}`}
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    disabled={isLoading}
                    required
                  />
                  {formErrors.confirmPassword && (
                    <div className="invalid-feedback">{formErrors.confirmPassword}</div>
                  )}
                </div>
              )}

              <div className="d-grid gap-2">
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </span>
                      {mode === 'login' ? 'Signing In...' : 'Creating Account...'}
                    </>
                  ) : (
                    mode === 'login' ? 'Sign In' : 'Create Account'
                  )}
                </button>
              </div>
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
                  onClick={() => AuthService.initiateGoogleLogin()}
                  disabled={isLoading}
                  title="Continue with Google"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    color: '#f5f1e8',
                    backgroundColor: '#4285f4'
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
                  onClick={() => AuthService.initiateGitHubLogin()}
                  disabled={isLoading}
                  title="Continue with GitHub"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    color: '#f5f1e8',
                    backgroundColor: '#333'
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
                  onClick={() => AuthService.initiateFacebookLogin()}
                  disabled={isLoading}
                  title="Continue with Meta"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    color: '#f5f1e8',
                    background: 'linear-gradient(45deg, #0866ff 0%, #0653d3 50%, #0866ff 100%)'
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
                  onClick={() => AuthService.initiateInstagramLogin()}
                  disabled={isLoading}
                  title="Continue with Instagram"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    background: 'linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%)',
                    border: 'none'
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
                  onClick={() => AuthService.initiateLinkedInLogin()}
                  disabled={isLoading}
                  title="Continue with LinkedIn"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    color: '#f5f1e8',
                    backgroundColor: '#0077b5'
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
                  onClick={() => AuthService.initiateTwitterLogin()}
                  disabled={isLoading}
                  title="Continue with X (Twitter)"
                  style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '12px',
                    borderColor: '#d4af37',
                    color: '#fff',
                    backgroundColor: '#000',
                    border: '2px solid #d4af37'
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
          </div>
          
          <div className="modal-footer">
            <p className="text-muted mb-0">
              {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                className="btn btn-link p-0"
                onClick={switchMode}
                disabled={isLoading}
              >
                {mode === 'login' ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
