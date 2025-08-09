'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import RoleProtectedRoute from '../../components/RoleProtectedRoute';
import AuthService, { User } from '../../services/auth';

interface UserStats {
  total_users: number;
  consumer_users: number;
  brand_users: number;
  admin_users: number;
  total_analyses: number;
  analyses_today: number;
}

interface SystemUser {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export default function AdminPanel() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'analytics' | 'settings'>('overview');
  const [stats, setStats] = useState<UserStats>({
    total_users: 0,
    consumer_users: 0,
    brand_users: 0,
    admin_users: 0,
    total_analyses: 0,
    analyses_today: 0
  });
  const [users, setUsers] = useState<SystemUser[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<SystemUser[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedUsers, setSelectedUsers] = useState<number[]>([]);
  const [error, setError] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    const currentUser = AuthService.getUser();
    if (!currentUser) {
      router.push('/landing');
      return;
    }
    
    if (currentUser.role !== 'admin') {
      router.push('/dashboard');
      return;
    }
    
    setUser(currentUser);
    loadAdminData();
    setLoading(false);
  }, [router]);

  const loadAdminData = async () => {
    try {
      // Load real system statistics
      const statsData = await AuthService.getSystemStats();
      setStats(statsData);

      // Load real user data
      const usersData = await AuthService.getAllUsers();
      setUsers(usersData);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load admin data');
    }
  };

  // Filter users based on search query, role, and status
  useEffect(() => {
    let filtered = users;

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(user => 
        user.username.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query) ||
        (user.full_name && user.full_name.toLowerCase().includes(query))
      );
    }

    // Apply role filter
    if (roleFilter !== 'all') {
      filtered = filtered.filter(user => user.role === roleFilter);
    }

    // Apply status filter
    if (statusFilter !== 'all') {
      const isActive = statusFilter === 'active';
      filtered = filtered.filter(user => user.is_active === isActive);
    }

    setFilteredUsers(filtered);
  }, [users, searchQuery, roleFilter, statusFilter]);

  // Bulk operations
  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedUsers(filteredUsers.map(user => user.id));
    } else {
      setSelectedUsers([]);
    }
  };

  const handleSelectUser = (userId: number, checked: boolean) => {
    if (checked) {
      setSelectedUsers(prev => [...prev, userId]);
    } else {
      setSelectedUsers(prev => prev.filter(id => id !== userId));
    }
  };

  const handleBulkStatusChange = async (isActive: boolean) => {
    try {
      for (const userId of selectedUsers) {
        await AuthService.updateUserStatus(userId, isActive);
      }
      // Refresh users list
      const usersData = await AuthService.getAllUsers();
      setUsers(usersData);
      setSelectedUsers([]);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to update user status');
    }
  };

  // Note: Bulk delete functionality would require backend deleteUser endpoint
  // For now, we'll focus on bulk status changes which are available

  const handleUserRoleChange = async (userId: number, newRole: string) => {
    try {
      await AuthService.updateUserRole(userId, newRole);
      
      // Update local state
      setUsers(prev => prev.map(u => 
        u.id === userId ? { ...u, role: newRole } : u
      ));
      
      // Reload stats to reflect changes
      const statsData = await AuthService.getSystemStats();
      setStats(statsData);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to update user role');
    }
  };

  const handleUserStatusToggle = async (userId: number) => {
    try {
      const user = users.find(u => u.id === userId);
      if (!user) return;
      
      const newStatus = !user.is_active;
      await AuthService.updateUserStatus(userId, newStatus);
      
      // Update local state
      setUsers(prev => prev.map(u => 
        u.id === userId ? { ...u, is_active: newStatus } : u
      ));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to update user status');
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading admin panel...</p>
        </div>
      </div>
    );
  }

  return (
    <RoleProtectedRoute allowedRoles={['admin']} fallbackRoute="/dashboard">
      <div className="min-vh-100 d-flex flex-column">
        <Navbar />
      
      <main className="flex-grow-1 bg-light">
        <div className="container py-5">
          <div className="row">
            <div className="col-12">
              <div className="d-flex align-items-center justify-content-between mb-4">
                <div>
                  <h1 className="h3 mb-1">
                    <i className="fas fa-cog me-2" style={{color: '#d4af37'}}></i>
                    Admin Panel
                  </h1>
                  <p className="text-muted mb-0">Manage Nexora system and users</p>
                </div>
                <div className="badge bg-danger fs-6">Admin Access</div>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <div className="card">
                <div className="card-header">
                  <ul className="nav nav-tabs card-header-tabs">
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                      >
                        <i className="fas fa-chart-pie me-2"></i>
                        Overview
                      </button>
                    </li>
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
                        onClick={() => setActiveTab('users')}
                      >
                        <i className="fas fa-users me-2"></i>
                        User Management
                      </button>
                    </li>
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'analytics' ? 'active' : ''}`}
                        onClick={() => setActiveTab('analytics')}
                      >
                        <i className="fas fa-chart-line me-2"></i>
                        Analytics
                      </button>
                    </li>
                    <li className="nav-item">
                      <button 
                        className={`nav-link ${activeTab === 'settings' ? 'active' : ''}`}
                        onClick={() => setActiveTab('settings')}
                      >
                        <i className="fas fa-cogs me-2"></i>
                        System Settings
                      </button>
                    </li>
                  </ul>
                </div>

                <div className="card-body">
                  {activeTab === 'overview' && (
                    <div>
                      <div className="row mb-4">
                        <div className="col-md-3 mb-3">
                          <div className="card bg-primary text-white">
                            <div className="card-body">
                              <div className="d-flex align-items-center">
                                <i className="fas fa-users fa-2x me-3"></i>
                                <div>
                                  <div className="h4 mb-0">{stats.total_users}</div>
                                  <div className="small">Total Users</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-3 mb-3">
                          <div className="card bg-success text-white">
                            <div className="card-body">
                              <div className="d-flex align-items-center">
                                <i className="fas fa-user fa-2x me-3"></i>
                                <div>
                                  <div className="h4 mb-0">{stats.consumer_users}</div>
                                  <div className="small">Consumers</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-3 mb-3">
                          <div className="card bg-warning text-white">
                            <div className="card-body">
                              <div className="d-flex align-items-center">
                                <i className="fas fa-building fa-2x me-3"></i>
                                <div>
                                  <div className="h4 mb-0">{stats.brand_users}</div>
                                  <div className="small">Brands/Agencies</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-3 mb-3">
                          <div className="card bg-info text-white">
                            <div className="card-body">
                              <div className="d-flex align-items-center">
                                <i className="fas fa-chart-bar fa-2x me-3"></i>
                                <div>
                                  <div className="h4 mb-0">{stats.total_analyses}</div>
                                  <div className="small">Total Analyses</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="row">
                        <div className="col-md-6">
                          <div className="card">
                            <div className="card-header">
                              <h5 className="card-title mb-0">Recent Activity</h5>
                            </div>
                            <div className="card-body">
                              <div className="d-flex align-items-center mb-2">
                                <i className="fas fa-chart-line text-success me-2"></i>
                                <span>{stats.analyses_today} analyses completed today</span>
                              </div>
                              <div className="d-flex align-items-center mb-2">
                                <i className="fas fa-user-plus text-primary me-2"></i>
                                <span>3 new users registered this week</span>
                              </div>
                              <div className="d-flex align-items-center">
                                <i className="fas fa-server text-info me-2"></i>
                                <span>System running smoothly</span>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-6">
                          <div className="card">
                            <div className="card-header">
                              <h5 className="card-title mb-0">Quick Actions</h5>
                            </div>
                            <div className="card-body">
                              <button className="btn btn-outline-primary btn-sm me-2 mb-2">
                                <i className="fas fa-download me-1"></i>
                                Export User Data
                              </button>
                              <button className="btn btn-outline-success btn-sm me-2 mb-2">
                                <i className="fas fa-chart-bar me-1"></i>
                                Generate Report
                              </button>
                              <button className="btn btn-outline-warning btn-sm mb-2">
                                <i className="fas fa-cog me-1"></i>
                                System Maintenance
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'users' && (
                    <div>
                      <div className="d-flex justify-content-between align-items-center mb-3">
                        <h5>User Management ({filteredUsers.length} users)</h5>
                        <button className="btn btn-primary btn-sm">
                          <i className="fas fa-user-plus me-1"></i>
                          Add User
                        </button>
                      </div>

                      {/* Search and Filters */}
                      <div className="row mb-3">
                        <div className="col-md-4">
                          <div className="input-group">
                            <span className="input-group-text">
                              <i className="fas fa-search"></i>
                            </span>
                            <input
                              type="text"
                              className="form-control"
                              placeholder="Search users..."
                              value={searchQuery}
                              onChange={(e) => setSearchQuery(e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="col-md-3">
                          <select
                            className="form-select"
                            value={roleFilter}
                            onChange={(e) => setRoleFilter(e.target.value)}
                          >
                            <option value="all">All Roles</option>
                            <option value="consumer">Consumer</option>
                            <option value="brand">Brand/Agency</option>
                            <option value="admin">Admin</option>
                          </select>
                        </div>
                        <div className="col-md-3">
                          <select
                            className="form-select"
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                          >
                            <option value="all">All Status</option>
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                          </select>
                        </div>
                        <div className="col-md-2">
                          <button
                            className="btn btn-outline-secondary w-100"
                            onClick={() => {
                              setSearchQuery('');
                              setRoleFilter('all');
                              setStatusFilter('all');
                            }}
                          >
                            <i className="fas fa-times me-1"></i>
                            Clear
                          </button>
                        </div>
                      </div>

                      {/* Bulk Actions */}
                      {selectedUsers.length > 0 && (
                        <div className="alert alert-info d-flex justify-content-between align-items-center mb-3">
                          <span>
                            <i className="fas fa-check-square me-2"></i>
                            {selectedUsers.length} user(s) selected
                          </span>
                          <div>
                            <button
                              className="btn btn-success btn-sm me-2"
                              onClick={() => handleBulkStatusChange(true)}
                            >
                              <i className="fas fa-check me-1"></i>
                              Activate
                            </button>
                            <button
                              className="btn btn-warning btn-sm me-2"
                              onClick={() => handleBulkStatusChange(false)}
                            >
                              <i className="fas fa-pause me-1"></i>
                              Deactivate
                            </button>
                            <button
                              className="btn btn-outline-secondary btn-sm"
                              onClick={() => setSelectedUsers([])}
                            >
                              <i className="fas fa-times me-1"></i>
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}

                      <div className="table-responsive">
                        <table className="table table-hover">
                          <thead>
                            <tr>
                              <th style={{ width: '40px' }}>
                                <input
                                  type="checkbox"
                                  className="form-check-input"
                                  checked={selectedUsers.length === filteredUsers.length && filteredUsers.length > 0}
                                  onChange={(e) => handleSelectAll(e.target.checked)}
                                />
                              </th>
                              <th>User</th>
                              <th>Email</th>
                              <th>Role</th>
                              <th>Status</th>
                              <th>Created</th>
                              <th>Last Login</th>
                              <th>Actions</th>
                            </tr>
                          </thead>
                          <tbody>
                            {filteredUsers.map(user => (
                              <tr key={user.id}>
                                <td>
                                  <input
                                    type="checkbox"
                                    className="form-check-input"
                                    checked={selectedUsers.includes(user.id)}
                                    onChange={(e) => handleSelectUser(user.id, e.target.checked)}
                                  />
                                </td>
                                <td>
                                  <div className="d-flex align-items-center">
                                    <div 
                                      className="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2"
                                      style={{ width: '32px', height: '32px', fontSize: '12px' }}
                                    >
                                      {user.full_name ? user.full_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
                                    </div>
                                    <div>
                                      <div className="fw-medium">{user.full_name || user.username}</div>
                                      <small className="text-muted">@{user.username}</small>
                                    </div>
                                  </div>
                                </td>
                                <td>{user.email}</td>
                                <td>
                                  <select 
                                    className="form-select form-select-sm"
                                    value={user.role}
                                    onChange={(e) => handleUserRoleChange(user.id, e.target.value)}
                                  >
                                    <option value="consumer">Consumer</option>
                                    <option value="brand">Brand/Agency</option>
                                    <option value="admin">Admin</option>
                                  </select>
                                </td>
                                <td>
                                  <span className={`badge ${user.is_active ? 'bg-success' : 'bg-danger'}`}>
                                    {user.is_active ? 'Active' : 'Inactive'}
                                  </span>
                                </td>
                                <td>
                                  <small>{new Date(user.created_at).toLocaleDateString()}</small>
                                </td>
                                <td>
                                  <small>
                                    {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                                  </small>
                                </td>
                                <td>
                                  <div className="btn-group btn-group-sm">
                                    <button 
                                      className={`btn ${user.is_active ? 'btn-outline-warning' : 'btn-outline-success'}`}
                                      onClick={() => handleUserStatusToggle(user.id)}
                                      title={user.is_active ? 'Deactivate' : 'Activate'}
                                    >
                                      <i className={`fas ${user.is_active ? 'fa-ban' : 'fa-check'}`}></i>
                                    </button>
                                    <button className="btn btn-outline-danger" title="Delete">
                                      <i className="fas fa-trash"></i>
                                    </button>
                                  </div>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {activeTab === 'analytics' && (
                    <div>
                      <h5 className="mb-3">System Analytics</h5>
                      <div className="alert alert-info">
                        <i className="fas fa-chart-line me-2"></i>
                        Advanced analytics dashboard coming soon. This will include user engagement metrics, 
                        analysis trends, and system performance data.
                      </div>
                    </div>
                  )}

                  {activeTab === 'settings' && (
                    <div>
                      <h5 className="mb-3">System Settings</h5>
                      <div className="alert alert-warning">
                        <i className="fas fa-cogs me-2"></i>
                        System configuration panel coming soon. This will include API settings, 
                        notification preferences, and security configurations.
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
        <Footer />
      </div>
    </RoleProtectedRoute>
  );
}
