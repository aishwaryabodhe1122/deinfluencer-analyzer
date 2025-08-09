'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

interface PasswordResetProps {
  mode: 'request' | 'reset' | 'success' | 'error';
  token?: string;
  message?: string;
}

const PasswordReset: React.FC<PasswordResetProps> = ({ mode, token, message }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [tokenValid, setTokenValid] = useState(false);
  const router = useRouter();

  // Verify reset token when in reset mode
  useEffect(() => {
    if (mode === 'reset' && token) {
      verifyResetToken(token);
    }
  }, [mode, token]);

  const verifyResetToken = async (resetToken: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/auth/verify-reset-token?token=${resetToken}`, {
        method: 'GET',
      });

      if (response.ok) {
        setTokenValid(true);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Invalid or expired reset link.');
        setTokenValid(false);
      }
    } catch (error) {
      setError('Network error. Please try again.');
      setTokenValid(false);
    }
  };

  const handleForgotPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) {
      setError('Please enter your email address.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email.trim() }),
      });

      if (response.ok) {
        setSuccess('Password reset link sent! Please check your email.');
        setEmail('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to send reset email. Please try again.');
      }
    } catch (error) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!password.trim()) {
      setError('Please enter a new password.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          token: token,
          new_password: password 
        }),
      });

      if (response.ok) {
        setSuccess('Password reset successfully! You can now sign in with your new password.');
        setTimeout(() => {
          router.push('/landing?password_reset=success');
        }, 2000);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to reset password. Please try again.');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    switch (mode) {
      case 'request':
        return (
          <div className="text-center">
            <div className="mb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
                <i className="fas fa-key text-white text-2xl"></i>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Forgot Password?</h2>
              <p className="text-gray-300 mb-6">
                Enter your email address and we'll send you a link to reset your password.
              </p>
            </div>

            <form onSubmit={handleForgotPassword}>
              <div className="mb-4">
                <input
                  type="email"
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent"
                  disabled={isLoading}
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
              >
                {isLoading ? (
                  <>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    Sending Reset Link...
                  </>
                ) : (
                  'Send Reset Link'
                )}
              </button>
            </form>

            <button
              onClick={() => router.push('/landing')}
              className="w-full bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300"
            >
              Back to Sign In
            </button>
          </div>
        );

      case 'reset':
        if (!tokenValid && !isLoading) {
          return (
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-red-400 to-pink-500 rounded-full flex items-center justify-center">
                <i className="fas fa-exclamation-triangle text-white text-2xl"></i>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Invalid Reset Link</h2>
              <p className="text-gray-300 mb-6">
                This password reset link is invalid or has expired. Please request a new one.
              </p>
              <button
                onClick={() => router.push('/reset-password')}
                className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 mb-4"
              >
                Request New Reset Link
              </button>
              <button
                onClick={() => router.push('/landing')}
                className="w-full bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300"
              >
                Back to Sign In
              </button>
            </div>
          );
        }

        return (
          <div className="text-center">
            <div className="mb-4">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                <i className="fas fa-lock text-white text-2xl"></i>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Reset Your Password</h2>
              <p className="text-gray-300 mb-6">
                Enter your new password below.
              </p>
            </div>

            <form onSubmit={handleResetPassword}>
              <div className="mb-4">
                <input
                  type="password"
                  placeholder="New password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent"
                  disabled={isLoading}
                  required
                  minLength={6}
                />
              </div>

              <div className="mb-4">
                <input
                  type="password"
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent"
                  disabled={isLoading}
                  required
                  minLength={6}
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
              >
                {isLoading ? (
                  <>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    Resetting Password...
                  </>
                ) : (
                  'Reset Password'
                )}
              </button>
            </form>

            <button
              onClick={() => router.push('/landing')}
              className="w-full bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-gray-600 transition-all duration-300"
            >
              Back to Sign In
            </button>
          </div>
        );

      case 'success':
        return (
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
              <i className="fas fa-check text-white text-2xl"></i>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Password Reset Successful!</h2>
            <p className="text-gray-300 mb-6">
              Your password has been successfully reset. You can now sign in with your new password.
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
            <h2 className="text-2xl font-bold text-white mb-2">Reset Failed</h2>
            <p className="text-gray-300 mb-6">
              {message || 'Unable to reset password. Please try again.'}
            </p>
            <button
              onClick={() => router.push('/reset-password')}
              className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 mb-4"
            >
              Try Again
            </button>
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

export default PasswordReset;
