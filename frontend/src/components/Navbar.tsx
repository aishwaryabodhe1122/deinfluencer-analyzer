'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import AuthService, { User } from '../services/auth';
import './navbar.css';

export default function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [isNavCollapsed, setIsNavCollapsed] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated on component mount
    const currentUser = AuthService.getUser();
    setUser(currentUser);
  }, []);

  const handleLogout = () => {
    AuthService.logout();
    setUser(null);
    setShowUserDropdown(false);
    setIsNavCollapsed(true);
    router.push('/landing');
  };

  const handleNavToggle = () => {
    setIsNavCollapsed(!isNavCollapsed);
  };

  const handleNavLinkClick = () => {
    setIsNavCollapsed(true);
    setShowUserDropdown(false);
  };

  return (
    <nav className="nexora-navbar navbar navbar-expand-lg">
      <div className="container">
        <Link href="/dashboard" className="nexora-brand">
          <div>
            <div className="nexora-brand-name">NEXORA</div>
            <div className="nexora-brand-tagline">Next-Gen Trust Aura</div>
          </div>
        </Link>
        
        <button 
          className="nexora-navbar-toggler navbar-toggler" 
          type="button" 
          onClick={handleNavToggle}
          aria-expanded={!isNavCollapsed}
          aria-label="Toggle navigation"
        >
          <span className="nexora-navbar-toggler-icon"></span>
        </button>
        
        <div className={`collapse navbar-collapse ${!isNavCollapsed ? 'show' : ''}`} id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link href="/dashboard" className="nexora-nav-link" onClick={handleNavLinkClick}>
                <i className="fas fa-tachometer-alt"></i>
                Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link href="/history" className="nexora-nav-link" onClick={handleNavLinkClick}>
                <i className="fas fa-history"></i>
                Analysis History
              </Link>
            </li>
            {user?.role === 'admin' && (
              <li className="nav-item">
                <Link href="/admin" className="nexora-nav-link" onClick={handleNavLinkClick}>
                  <i className="fas fa-cog"></i>
                  Admin Panel
                </Link>
              </li>
            )}
            
            {user ? (
              <li className="nav-item nexora-user-dropdown">
                <button 
                  className="nexora-user-btn"
                  onClick={() => setShowUserDropdown(!showUserDropdown)}
                >
                  <div 
                    className="rounded-circle d-flex align-items-center justify-content-center"
                    style={{ width: '32px', height: '32px', fontSize: '14px', backgroundColor: 'var(--nexora-dark)', color: 'white' }}
                  >
                    {user.full_name ? user.full_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
                  </div>
                  <span>{user.full_name || user.username}</span>
                  <i className="fas fa-chevron-down"></i>
                </button>
                {showUserDropdown && (
                  <div className="nexora-dropdown-menu dropdown-menu dropdown-menu-end show">
                    <div className="dropdown-header">
                      <small className="text-muted">{user.email}</small>
                    </div>
                    <div className="nexora-dropdown-divider"></div>
                    <Link href="/profile" className="nexora-dropdown-item" onClick={handleNavLinkClick}>
                      <i className="fas fa-user"></i>
                      Profile Settings
                    </Link>
                    <Link href="/history" className="nexora-dropdown-item" onClick={handleNavLinkClick}>
                      <i className="fas fa-history"></i>
                      Analysis History
                    </Link>
                    {user.role === 'admin' && (
                      <>
                        <div className="nexora-dropdown-divider"></div>
                        <Link href="/admin" className="nexora-dropdown-item" onClick={handleNavLinkClick}>
                          <i className="fas fa-cog"></i>
                          Admin Panel
                        </Link>
                      </>
                    )}
                    <div className="nexora-dropdown-divider"></div>
                    <span className="nexora-dropdown-item" style={{cursor: 'default'}}>
                      <i className="fas fa-info-circle"></i>
                      Role: <span className="badge bg-secondary">{user.role}</span>
                    </span>
                    <div className="nexora-dropdown-divider"></div>
                    <button className="nexora-dropdown-item danger" onClick={handleLogout}>
                      <i className="fas fa-sign-out-alt"></i>
                      Sign Out
                    </button>
                  </div>
                )}
              </li>
            ) : (
              <li className="nav-item">
                <button 
                  className="btn btn-outline-primary"
                  onClick={() => router.push('/landing')}
                >
                  Sign In
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}
