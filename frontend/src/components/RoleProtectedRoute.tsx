'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AuthService, { User } from '../services/auth';

interface RoleProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: string[];
  fallbackRoute?: string;
}

export default function RoleProtectedRoute({ 
  children, 
  allowedRoles, 
  fallbackRoute = '/landing' 
}: RoleProtectedRouteProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasAccess, setHasAccess] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkAccess = () => {
      const currentUser = AuthService.getUser();
      
      if (!currentUser) {
        // User not authenticated, redirect to landing
        router.push('/landing');
        return;
      }

      setUser(currentUser);
      
      // Check if user's role is in allowed roles
      const userHasAccess = allowedRoles.includes(currentUser.role);
      setHasAccess(userHasAccess);
      
      if (!userHasAccess) {
        // User doesn't have required role, redirect to fallback
        router.push(fallbackRoute);
        return;
      }
      
      setLoading(false);
    };

    checkAccess();
  }, [allowedRoles, fallbackRoute, router]);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Checking permissions...</p>
        </div>
      </div>
    );
  }

  if (!hasAccess) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="alert alert-warning" role="alert">
            <h4 className="alert-heading">Access Denied</h4>
            <p>You don't have permission to access this page.</p>
            <hr />
            <p className="mb-0">
              Required roles: {allowedRoles.join(', ')}
              <br />
              Your role: {user?.role}
            </p>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => router.push('/dashboard')}
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
