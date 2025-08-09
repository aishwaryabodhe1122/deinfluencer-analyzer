// Use Next.js API routes instead of direct backend calls to avoid CORS - no axios needed
const API_BASE_URL = 'http://localhost:8000';

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

class AuthService {
  private static tokenKey = 'nexora_token';
  private static userKey = 'nexora_user';

  // Register new user
  static async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }
      
      // Store token and user data
      localStorage.setItem(AuthService.tokenKey, data.access_token);
      localStorage.setItem(AuthService.userKey, JSON.stringify(data.user));
      
      return data;
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed. Please try again.');
    }
  }

  // Login user
  static async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }
      
      // Store token and user data
      localStorage.setItem(AuthService.tokenKey, data.access_token);
      localStorage.setItem(AuthService.userKey, JSON.stringify(data.user));
      
      return data;
    } catch (error: any) {
      throw new Error(error.message || 'Login failed. Please check your credentials.');
    }
  }

  // Logout user
  static logout(): void {
    localStorage.removeItem(AuthService.tokenKey);
    localStorage.removeItem(AuthService.userKey);
  }

  // Get stored token
  static getToken(): string | null {
    return localStorage.getItem(AuthService.tokenKey);
  }

  // Get stored user
  static getUser(): User | null {
    const userStr = localStorage.getItem(AuthService.userKey);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    const token = this.getToken();
    const user = this.getUser();
    return !!(token && user);
  }

  // Get user role
  static getUserRole(): string | null {
    const user = this.getUser();
    return user?.role || null;
  }

  // Check if user has specific role or higher
  static hasRole(requiredRole: string): boolean {
    const userRole = this.getUserRole();
    if (!userRole) return false;

    const roleHierarchy: { [key: string]: number } = {
      consumer: 1,
      brand: 2,
      admin: 3
    };

    const userLevel = roleHierarchy[userRole] || 0;
    const requiredLevel = roleHierarchy[requiredRole] || 0;

    return userLevel >= requiredLevel;
  }

  // Get authorization header
  static getAuthHeader(): { Authorization: string } | {} {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  // Profile Management
  static async updateProfile(profileData: {
    full_name?: string;
    email?: string;
    avatar_url?: string;
  }): Promise<User> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/profile`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });

    if (!response.ok) {
      throw new Error('Failed to update profile');
    }

    const updatedUser = await response.json();
    localStorage.setItem('nexora_user', JSON.stringify(updatedUser));
    return updatedUser;
  }

  static async changePassword(passwordData: {
    current_password: string;
    new_password: string;
  }): Promise<void> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/profile/password`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(passwordData)
    });

    if (!response.ok) {
      throw new Error('Failed to change password');
    }
  }

  static async updateNotificationPreferences(preferences: {
    analysis_updates: boolean;
    weekly_reports: boolean;
    security_alerts: boolean;
  }): Promise<void> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/profile/notifications`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferences)
    });

    if (!response.ok) {
      throw new Error('Failed to update notification preferences');
    }
  }

  // Admin Functions
  static async getSystemStats(): Promise<{
    total_users: number;
    consumer_users: number;
    brand_users: number;
    admin_users: number;
    total_analyses: number;
    analyses_today: number;
  }> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/admin/stats`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch system stats');
    }

    return response.json();
  }

  static async getAllUsers(): Promise<any[]> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/admin/users`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }

    return response.json();
  }

  static async updateUserRole(userId: number, newRole: string): Promise<void> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/admin/users/${userId}/role`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ role: newRole })
    });

    if (!response.ok) {
      throw new Error('Failed to update user role');
    }
  }

  static async updateUserStatus(userId: number, isActive: boolean): Promise<void> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/admin/users/${userId}/status`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_active: isActive })
    });

    if (!response.ok) {
      throw new Error('Failed to update user status');
    }
  }

  // Analysis History
  static async getAnalysisHistory(filters?: {
    platform?: string;
    search?: string;
    sort_by?: string;
    limit?: number;
    offset?: number;
  }): Promise<any[]> {
    const token = localStorage.getItem('nexora_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const params = new URLSearchParams();
    if (filters?.platform) params.append('platform', filters.platform);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.sort_by) params.append('sort_by', filters.sort_by);
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.offset) params.append('offset', filters.offset.toString());

    const response = await fetch(`${API_BASE_URL}/api/history?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch analysis history');
    }

    return await response.json();
  }

  // Social Authentication Methods
  static initiateGoogleLogin(): void {
    const googleAuthUrl = `${API_BASE_URL}/api/auth/google/login`;
    window.location.href = googleAuthUrl;
  }

  static initiateGitHubLogin(): void {
    const githubAuthUrl = `${API_BASE_URL}/api/auth/github/login`;
    window.location.href = githubAuthUrl;
  }

  static initiateFacebookLogin(): void {
    const facebookAuthUrl = `${API_BASE_URL}/api/auth/facebook/login`;
    window.location.href = facebookAuthUrl;
  }

  static initiateInstagramLogin(): void {
    const instagramAuthUrl = `${API_BASE_URL}/api/auth/instagram/login`;
    window.location.href = instagramAuthUrl;
  }

  static initiateLinkedInLogin(): void {
    const linkedinAuthUrl = `${API_BASE_URL}/api/auth/linkedin/login`;
    window.location.href = linkedinAuthUrl;
  }

  static initiateTwitterLogin(): void {
    const twitterAuthUrl = `${API_BASE_URL}/api/auth/twitter/login`;
    window.location.href = twitterAuthUrl;
  }

  static async handleSocialCallback(token: string, userId: string): Promise<AuthResponse> {
    try {
      // Store the token and fetch user data
      localStorage.setItem(AuthService.tokenKey, token);
      
      // Fetch user data using the token
      const response = await fetch(`${API_BASE_URL}/api/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }
      
      const user = await response.json();
      localStorage.setItem(AuthService.userKey, JSON.stringify(user));
      
      return {
        access_token: token,
        token_type: 'bearer',
        user: user
      };
    } catch (error: any) {
      // Clear any stored data on error
      localStorage.removeItem(AuthService.tokenKey);
      localStorage.removeItem(AuthService.userKey);
      throw new Error('Social authentication failed');
    }
  }

  static async verifySocialToken(provider: string, accessToken: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/social/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          provider: provider,
          access_token: accessToken
        })
      });
      
      if (!response.ok) {
        throw new Error('Social token verification failed');
      }
      
      const authData = await response.json();
      
      // Store token and user data
      localStorage.setItem(AuthService.tokenKey, authData.access_token);
      localStorage.setItem(AuthService.userKey, JSON.stringify(authData.user));
      
      return authData;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Social authentication verification failed');
    }
  }
}

// Export both the class and an instance for backward compatibility
export const authService = new AuthService();
export default AuthService;
export { AuthService };
