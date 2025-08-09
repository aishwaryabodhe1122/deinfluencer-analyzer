'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import AuthService, { User } from '../../services/auth';

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'notifications'>('profile');
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    username: '',
    current_password: '',
    new_password: '',
    confirm_password: '',
    notifications: {
      analysis_updates: true,
      weekly_reports: false,
      security_alerts: true
    }
  });
  const router = useRouter();

  useEffect(() => {
    const currentUser = AuthService.getUser();
    if (!currentUser) {
      router.push('/landing');
      return;
    }
    
    setUser(currentUser);
    setFormData(prev => ({
      ...prev,
      full_name: currentUser.full_name || '',
      email: currentUser.email,
      username: currentUser.username
    }));
    setLoading(false);
  }, [router]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('notifications.')) {
      const notificationKey = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        notifications: {
          ...prev.notifications,
          [notificationKey]: checked
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
    
    if (error) setError('');
    if (success) setSuccess('');
  };

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      const updatedUser = await AuthService.updateProfile({
        full_name: formData.full_name,
        email: formData.email
      });
      
      setSuccess('Profile updated successfully!');
      setUser(updatedUser);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.new_password !== formData.confirm_password) {
      setError('New passwords do not match');
      return;
    }
    
    if (formData.new_password.length < 6) {
      setError('New password must be at least 6 characters long');
      return;
    }

    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await AuthService.changePassword({
        current_password: formData.current_password,
        new_password: formData.new_password
      });
      
      setSuccess('Password changed successfully!');
      setFormData(prev => ({
        ...prev,
        current_password: '',
        new_password: '',
        confirm_password: ''
      }));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to change password');
    } finally {
      setSaving(false);
    }
  };

  const handleNotificationUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await AuthService.updateNotificationPreferences(formData.notifications);
      
      setSuccess('Notification preferences updated successfully!');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to update notification preferences');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100 d-flex flex-column">
      <Navbar />
      
      <main className="flex-grow-1 bg-light">
        <div className="container py-5">
          <div className="row">
            <div className="col-12">
              <div className="d-flex align-items-center mb-4">
                <div 
                  className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3"
                  style={{ width: '60px', height: '60px', fontSize: '24px' }}
                >
                  {user?.full_name ? user.full_name.charAt(0).toUpperCase() : user?.username.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h1 className="h3 mb-1">{user?.full_name || user?.username}</h1>
                  <p className="text-muted mb-0">
                    {user?.email} • <span className="badge bg-secondary">{user?.role}</span>
                  </p>
                </div>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              {success && (
                <div className="alert alert-success" role="alert">
                  {success}
                </div>
              )}

              <div className="card">
                <div className="card-header">
                  <ul className="nav nav-tabs card-header-tabs">
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'profile' ? 'active' : ''}`}
                        onClick={() => setActiveTab('profile')}
                      >
                        <i className="fas fa-user me-2"></i>
                        Profile Information
                      </button>
                    </li>
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'security' ? 'active' : ''}`}
                        onClick={() => setActiveTab('security')}
                      >
                        <i className="fas fa-lock me-2"></i>
                        Security
                      </button>
                    </li>
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'notifications' ? 'active' : ''}`}
                        onClick={() => setActiveTab('notifications')}
                      >
                        <i className="fas fa-bell me-2"></i>
                        Notifications
                      </button>
                    </li>
                  </ul>
                </div>

                <div className="card-body">
                  {activeTab === 'profile' && (
                    <form onSubmit={handleProfileUpdate}>
                      <div className="row">
                        <div className="col-md-6">
                          <div className="mb-3">
                            <label htmlFor="full_name" className="form-label">Full Name</label>
                            <input
                              type="text"
                              className="form-control"
                              id="full_name"
                              name="full_name"
                              value={formData.full_name}
                              onChange={handleInputChange}
                              disabled={saving}
                            />
                          </div>
                        </div>
                        <div className="col-md-6">
                          <div className="mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input
                              type="text"
                              className="form-control"
                              id="username"
                              name="username"
                              value={formData.username}
                              disabled
                              title="Username cannot be changed"
                            />
                          </div>
                        </div>
                      </div>
                      
                      <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email Address</label>
                        <input
                          type="email"
                          className="form-control"
                          id="email"
                          name="email"
                          value={formData.email}
                          onChange={handleInputChange}
                          disabled={saving}
                        />
                      </div>

                      <div className="mb-3">
                        <label className="form-label">Account Role</label>
                        <div className="form-control-plaintext">
                          <span className="badge bg-secondary fs-6">{user?.role}</span>
                          <small className="text-muted ms-2">
                            Contact admin to change your role
                          </small>
                        </div>
                      </div>

                      <button type="submit" className="btn btn-primary" disabled={saving}>
                        {saving ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Updating...
                          </>
                        ) : (
                          'Update Profile'
                        )}
                      </button>
                    </form>
                  )}

                  {activeTab === 'security' && (
                    <form onSubmit={handlePasswordChange}>
                      <div className="mb-3">
                        <label htmlFor="current_password" className="form-label">Current Password</label>
                        <input
                          type="password"
                          className="form-control"
                          id="current_password"
                          name="current_password"
                          value={formData.current_password}
                          onChange={handleInputChange}
                          disabled={saving}
                          required
                        />
                      </div>

                      <div className="mb-3">
                        <label htmlFor="new_password" className="form-label">New Password</label>
                        <input
                          type="password"
                          className="form-control"
                          id="new_password"
                          name="new_password"
                          value={formData.new_password}
                          onChange={handleInputChange}
                          disabled={saving}
                          required
                        />
                        <div className="form-text">Password must be at least 6 characters long</div>
                      </div>

                      <div className="mb-3">
                        <label htmlFor="confirm_password" className="form-label">Confirm New Password</label>
                        <input
                          type="password"
                          className="form-control"
                          id="confirm_password"
                          name="confirm_password"
                          value={formData.confirm_password}
                          onChange={handleInputChange}
                          disabled={saving}
                          required
                        />
                      </div>

                      <button type="submit" className="btn btn-primary" disabled={saving}>
                        {saving ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Changing...
                          </>
                        ) : (
                          'Change Password'
                        )}
                      </button>
                    </form>
                  )}

                  {activeTab === 'notifications' && (
                    <form onSubmit={handleNotificationUpdate}>
                      <div className="mb-4">
                        <h5>Email Notifications</h5>
                        <p className="text-muted">Choose what notifications you'd like to receive via email.</p>
                      </div>

                      <div className="mb-3">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id="analysis_updates"
                            name="notifications.analysis_updates"
                            checked={formData.notifications.analysis_updates}
                            onChange={handleInputChange}
                            disabled={saving}
                          />
                          <label className="form-check-label" htmlFor="analysis_updates">
                            <strong>Analysis Updates</strong>
                            <div className="text-muted small">Get notified when your influencer analyses are complete</div>
                          </label>
                        </div>
                      </div>

                      <div className="mb-3">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id="weekly_reports"
                            name="notifications.weekly_reports"
                            checked={formData.notifications.weekly_reports}
                            onChange={handleInputChange}
                            disabled={saving}
                          />
                          <label className="form-check-label" htmlFor="weekly_reports">
                            <strong>Weekly Reports</strong>
                            <div className="text-muted small">Receive weekly summaries of your analysis activity</div>
                          </label>
                        </div>
                      </div>

                      <div className="mb-3">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id="security_alerts"
                            name="notifications.security_alerts"
                            checked={formData.notifications.security_alerts}
                            onChange={handleInputChange}
                            disabled={saving}
                          />
                          <label className="form-check-label" htmlFor="security_alerts">
                            <strong>Security Alerts</strong>
                            <div className="text-muted small">Important security notifications about your account</div>
                          </label>
                        </div>
                      </div>

                      <button type="submit" className="btn btn-primary" disabled={saving}>
                        {saving ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                            Updating...
                          </>
                        ) : (
                          'Update Preferences'
                        )}
                      </button>
                    </form>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
}
