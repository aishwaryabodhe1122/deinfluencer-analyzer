'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import AuthService from '@/services/auth';

export default function AuthCallback() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Processing authentication...');
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const token = searchParams.get('token');
        const userId = searchParams.get('user');
        const error = searchParams.get('error');

        if (error) {
          setStatus('error');
          setMessage('Authentication failed. Please try again.');
          setTimeout(() => {
            router.push('/landing');
          }, 3000);
          return;
        }

        if (token && userId) {
          // Handle successful OAuth callback
          await AuthService.handleSocialCallback(token, userId);
          setStatus('success');
          setMessage('Authentication successful! Redirecting to dashboard...');
          
          // Redirect to dashboard after successful authentication
          setTimeout(() => {
            router.push('/dashboard');
          }, 2000);
        } else {
          setStatus('error');
          setMessage('Invalid authentication response. Please try again.');
          setTimeout(() => {
            router.push('/landing');
          }, 3000);
        }
      } catch (error) {
        console.error('OAuth callback error:', error);
        setStatus('error');
        setMessage('Authentication failed. Please try again.');
        setTimeout(() => {
          router.push('/landing');
        }, 3000);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: '#0a0e1a' }}>
      <div className="text-center">
        <div className="card" style={{ 
          backgroundColor: '#1a1d2a', 
          border: '1px solid #d4af37',
          minWidth: '400px'
        }}>
          <div className="card-body p-5">
            {status === 'loading' && (
              <>
                <div className="spinner-border text-warning mb-3" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
                <h4 className="text-light mb-3">Authenticating...</h4>
                <p className="text-muted">{message}</p>
              </>
            )}
            
            {status === 'success' && (
              <>
                <div className="text-success mb-3">
                  <i className="fas fa-check-circle" style={{ fontSize: '3rem' }}></i>
                </div>
                <h4 className="text-light mb-3">Success!</h4>
                <p className="text-muted">{message}</p>
              </>
            )}
            
            {status === 'error' && (
              <>
                <div className="text-danger mb-3">
                  <i className="fas fa-exclamation-circle" style={{ fontSize: '3rem' }}></i>
                </div>
                <h4 className="text-light mb-3">Authentication Failed</h4>
                <p className="text-muted">{message}</p>
                <button 
                  className="btn btn-outline-warning mt-3"
                  onClick={() => router.push('/landing')}
                >
                  Return to Login
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
