'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

interface EmailVerificationProps {
  mode: 'pending' | 'verify' | 'success' | 'error';
  email?: string;
  token?: string;
  message?: string;
}

const EmailVerification: React.FC<EmailVerificationProps> = ({ 
  mode, 
  email, 
  token, 
  message 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [resendCooldown, setResendCooldown] = useState(0);
  const router = useRouter();

  // Handle email verification from URL token
  useEffect(() => {
    if (mode === 'verify' && token) {
      verifyEmailToken(token);
    }
  }, [mode, token]);

  // Resend cooldown timer
  useEffect(() => {
    if (resendCooldown > 0) {
      const timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [resendCooldown]);

  const verifyEmailToken = async (verificationToken: string) => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch(`http://localhost:8000/api/auth/verify-email?token=${verificationToken}`, {
        method: 'GET',
      });

      if (response.ok) {
        setSuccess('Email verified successfully! You can now sign in.');
        setTimeout(() => {
          router.push('/landing?verified=true');
        }, 2000);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Email verification failed. The link may be expired or invalid.');
      }
    } catch (error) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const resendVerificationEmail = async () => {
    if (!email || resendCooldown > 0) return;
    
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/send-verification-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setSuccess('Verification email sent! Please check your inbox.');
        setResendCooldown(60); // 60 second cooldown
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to send verification email.');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    switch (mode) {
      case 'pending':
        return (
          <div className="text-center">
            <div className="mb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
                <i className="fas fa-envelope text-white text-2xl"></i>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Check Your Email</h2>
              <p className="text-gray-300 mb-6">
                We've sent a verification link to <span className="text-yellow-400 font-semibold">{email}</span>
              </p>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-4 mb-6">
              <p className="text-gray-300 text-sm mb-4">
                <i className="fas fa-info-circle text-blue-400 mr-2"></i>
                Click the verification link in your email to activate your account.
              </p>
              <p className="text-gray-400 text-xs">
                Can't find the email? Check your spam folder or request a new one.
              </p>
            </div>

            <button
              onClick={resendVerificationEmail}
              disabled={isLoading || resendCooldown > 0}
              className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
            >
              {isLoading ? (
                <i className="fas fa-spinner fa-spin mr-2"></i>
              ) : resendCooldown > 0 ? (
                `Resend in ${resendCooldown}s`
              ) : (
                'Resend Verification Email'
              )}
            </button>

            <button
              onClick={() => router.push('/landing')}
              className="w-full bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300"
            >
              Back to Sign In
            </button>
          </div>
        );

      case 'verify':
        return (
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
              <i className="fas fa-spinner fa-spin text-white text-2xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Verifying Your Email</h2>
            <p className="text-gray-300">Please wait while we verify your email address...</p>
          </div>
        );

      case 'success':
        return (
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
              <i className="fas fa-check text-white text-2xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Email Verified!</h2>
            <p className="text-gray-300 mb-6">
              Your email has been successfully verified. You can now sign in to your account.
            </p>
            <button
              onClick={() => router.push('/landing')}
              className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300"
            >
              Continue to Sign In
            </button>
          </div>
        );

      case 'error':
        return (
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-red-400 to-pink-500 rounded-full flex items-center justify-center">
              <i className="fas fa-exclamation-triangle text-white text-2xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Verification Failed</h2>
            <p className="text-gray-300 mb-6">
              {message || 'The verification link is invalid or has expired.'}
            </p>
            
            {email && (
              <button
                onClick={resendVerificationEmail}
                disabled={isLoading || resendCooldown > 0}
                className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
              >
                {isLoading ? (
                  <i className="fas fa-spinner fa-spin mr-2"></i>
                ) : resendCooldown > 0 ? (
                  `Resend in ${resendCooldown}s`
                ) : (
                  'Request New Verification Email'
                )}
              </button>
            )}

            <button
              onClick={() => router.push('/landing')}
              className="w-full bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300"
            >
              Back to Sign In
            </button>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700">
          {/* Nexora Logo/Branding */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
              Nexora
            </h1>
            <p className="text-gray-400 text-sm">Next Gen Trust Aura</p>
          </div>

          {/* Error/Success Messages */}
          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-4">
              <i className="fas fa-exclamation-circle mr-2"></i>
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-900/50 border border-green-500 text-green-200 px-4 py-3 rounded-lg mb-4">
              <i className="fas fa-check-circle mr-2"></i>
              {success}
            </div>
          )}

          {/* Main Content */}
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default EmailVerification;
