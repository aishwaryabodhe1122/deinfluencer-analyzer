'use client';

import { useState, useEffect, useRef } from 'react';

interface SearchSectionProps {
  onAnalyze: (username: string, platform: string) => void;
  isLoading: boolean;
  error?: string | null;
}

export default function SearchSection({ onAnalyze, isLoading, error }: SearchSectionProps) {
  const [username, setUsername] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [validationError, setValidationError] = useState('');
  const [showPlatformDropdown, setShowPlatformDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowPlatformDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const validateUsername = (username: string): string | null => {
    if (!username || username.trim().length === 0) {
      return 'Username is required';
    }

    const trimmedUsername = username.trim();

    // Check length
    if (trimmedUsername.length < 2) {
      return 'Username must be at least 2 characters long';
    }
    if (trimmedUsername.length > 30) {
      return 'Username must be less than 30 characters';
    }

    // Check for valid characters
    if (!/^[a-zA-Z0-9._]+$/.test(trimmedUsername)) {
      return 'Username can only contain letters, numbers, dots, and underscores';
    }

    // Check for obvious gibberish patterns
    const gibberishPatterns = [
      /^[a-z]{1,2}$/i,  // Single or double letters
      /^\d+$/,  // Only numbers
      /^[._]+$/,  // Only dots/underscores
      /^(test|user|admin)\d*$/i,  // test, user, admin variations
      /^[qwerty]+$/i,  // keyboard mashing
      /^[asdf]+$/i,  // keyboard mashing
    ];

    for (const pattern of gibberishPatterns) {
      if (pattern.test(trimmedUsername)) {
        return 'Please enter a valid influencer username';
      }
    }

    // Check for common gibberish sequences
    const commonGibberish = ['asdfgh', 'qwerty', 'zxcvbn', '123456'];
    const lowerUsername = trimmedUsername.toLowerCase();
    for (const gibberish of commonGibberish) {
      if (lowerUsername.includes(gibberish)) {
        return 'Please enter a valid influencer username';
      }
    }

    // Must have at least one letter
    if (!/[a-zA-Z]/.test(trimmedUsername)) {
      return 'Username must contain at least one letter';
    }

    // Must not be all the same character
    if (new Set(trimmedUsername.toLowerCase()).size === 1) {
      return 'Please enter a valid influencer username';
    }

    return null;
  };

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newUsername = e.target.value;
    setUsername(newUsername);
    
    // Clear validation error when user starts typing
    if (validationError && newUsername.trim()) {
      setValidationError('');
    }
    
    // Also clear API errors when user starts typing (passed from parent)
    // This will be handled by the parent component when it detects input changes
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const error = validateUsername(username);
    if (error) {
      setValidationError(error);
      return;
    }
    
    setValidationError('');
    onAnalyze(username.trim(), platform);
  };

  return (
    <section className="search-container" style={{
      background: 'linear-gradient(135deg, #2a2d3a 0%, #1a1d2a 100%)',
      color: '#ffffff',
      padding: '4rem 0',
      minHeight: '60vh',
      display: 'flex',
      alignItems: 'center'
    }}>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-8 text-center">
            <h1 className="display-4 fw-bold mb-4" style={{
              background: 'linear-gradient(45deg, #d4af37, #f4e4a6)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>
              Discover Authentic Influencers
            </h1>
            <p className="lead mb-5" style={{
              color: '#f5f1e8',
              opacity: 0.9
            }}>
              Get AI-powered authenticity scores for influencers across social media platforms. 
              Make informed decisions about who to trust and follow.
            </p>
            
            <form onSubmit={handleSubmit} className="row g-3 justify-content-center">
              <div className="col-md-6">
                <div className="input-group input-group-lg">
                  <span className="input-group-text" style={{
                    backgroundColor: '#1a1d2a',
                    borderColor: '#d4af37',
                    color: '#d4af37',
                    border: '2px solid #d4af37'
                  }}>@</span>
                  <input
                    type="text"
                    className={`form-control white-placeholder ${validationError ? 'is-invalid' : ''}`}
                    placeholder="Enter username"
                    value={username}
                    onChange={handleUsernameChange}
                    disabled={isLoading}
                    required
                    style={{
                      backgroundColor: '#1a1d2a',
                      borderColor: '#d4af37',
                      color: '#ffffff',
                      border: '2px solid #d4af37'
                    }}
                  />
                </div>
                {validationError && (
                  <div className="invalid-feedback d-block" style={{
                    color: '#ff6b6b'
                  }}>
                    {validationError}
                  </div>
                )}
              </div>
              <div className="col-md-3">
                <div className="custom-dropdown" style={{ position: 'relative' }} ref={dropdownRef}>
                  <button 
                    type="button"
                    className="btn"
                    style={{
                      backgroundColor: '#1a1d2a',
                      borderColor: '#d4af37',
                      color: '#ffffff',
                      border: '2px solid #d4af37',
                      fontSize: '16px',
                      fontWeight: '500',
                      padding: '12px 15px',
                      borderRadius: '8px',
                      cursor: isLoading ? 'not-allowed' : 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      minHeight: '48px',
                      width: '100%'
                    }}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      if (!isLoading) {
                        console.log('Dropdown clicked, current state:', showPlatformDropdown);
                        setShowPlatformDropdown(prev => !prev);
                      }
                    }}
                    disabled={isLoading}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <i 
                        className={`fab ${
                          platform === 'instagram' ? 'fa-instagram' :
                          platform === 'twitter' ? 'fa-twitter' :
                          platform === 'tiktok' ? 'fa-tiktok' :
                          platform === 'youtube' ? 'fa-youtube' :
                          platform === 'facebook' ? 'fa-meta' :
                          platform === 'linkedin' ? 'fa-linkedin' : 'fa-instagram'
                        }`}
                        style={{ color: '#d4af37', fontSize: '18px' }}
                      ></i>
                      <span>
                        {platform === 'instagram' ? 'Instagram' :
                         platform === 'twitter' ? 'X (Twitter)' :
                         platform === 'tiktok' ? 'TikTok' :
                         platform === 'youtube' ? 'YouTube' :
                         platform === 'facebook' ? 'Meta' :
                         platform === 'linkedin' ? 'LinkedIn' : 'Instagram'}
                      </span>
                    </div>
                    <i 
                      className={`fas fa-chevron-${showPlatformDropdown ? 'up' : 'down'}`} 
                      style={{ color: '#d4af37', fontSize: '12px' }}
                    ></i>
                  </button>
                  
                  {showPlatformDropdown && (
                    <div 
                      className="dropdown-menu show"
                      style={{
                        position: 'absolute',
                        top: '100%',
                        left: 0,
                        right: 0,
                        backgroundColor: '#1a1d2a',
                        border: '2px solid #d4af37',
                        borderTop: 'none',
                        borderRadius: '0 0 8px 8px',
                        zIndex: 1000,
                        maxHeight: '200px',
                        overflowY: 'auto',
                        display: 'block'
                      }}
                    >
                      {[
                        { value: 'instagram', label: 'Instagram', icon: 'fa-instagram' },
                        { value: 'twitter', label: 'X (Twitter)', icon: 'fa-twitter' },
                        { value: 'tiktok', label: 'TikTok', icon: 'fa-tiktok' },
                        { value: 'youtube', label: 'YouTube', icon: 'fa-youtube' },
                        { value: 'facebook', label: 'Meta', icon: 'fa-meta' },
                        { value: 'linkedin', label: 'LinkedIn', icon: 'fa-linkedin' }
                      ].map((option) => (
                        <button
                          key={option.value}
                          type="button"
                          className="dropdown-item"
                          style={{
                            padding: '12px 15px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '10px',
                            color: '#ffffff',
                            backgroundColor: platform === option.value ? '#2a2d3a' : 'transparent',
                            borderBottom: '1px solid #333',
                            border: 'none',
                            width: '100%',
                            textAlign: 'left'
                          }}
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('Option clicked:', option.value);
                            setPlatform(option.value);
                            setShowPlatformDropdown(false);
                          }}
                          onMouseEnter={(e) => {
                            if (platform !== option.value) {
                              e.currentTarget.style.backgroundColor = '#2a2d3a';
                            }
                          }}
                          onMouseLeave={(e) => {
                            if (platform !== option.value) {
                              e.currentTarget.style.backgroundColor = 'transparent';
                            }
                          }}
                        >
                          <i className={`fab ${option.icon}`} style={{ color: '#d4af37', fontSize: '16px' }}></i>
                          <span>{option.label}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
              <div className="col-md-3">
                <button
                  type="submit"
                  className="btn btn-lg w-100"
                  disabled={isLoading || !username.trim() || !!validationError}
                  style={{
                    background: 'linear-gradient(45deg, #d4af37, #f4e4a6)',
                    border: '2px solid #d4af37',
                    color: '#2a2d3a',
                    fontWeight: 'bold',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 8px 25px rgba(212, 175, 55, 0.4)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  {isLoading ? (
                    <>
                      <div className="spinner-border spinner-border-sm me-2" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                      Analyzing...
                    </>
                  ) : (
                    'Analyze'
                  )}
                </button>
              </div>
            </form>
            
            {/* Validation and API Error Display */}
            {(validationError || error) && (
              <div className="mt-3">
                <div className="alert alert-danger" role="alert">
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  {validationError || error}
                </div>
              </div>
            )}
            
            <div className="mt-4">
              <small className="text-light opacity-75">
                Try verified influencers: elonmusk, justinbieber, taylorswift, therock, mkbhd, mrbeast
              </small>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
