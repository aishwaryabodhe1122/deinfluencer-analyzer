'use client';

import React, { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import PasswordReset from '../../components/PasswordReset';

function PasswordResetContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const success = searchParams.get('success');
  const error = searchParams.get('error');

  // Determine the mode based on URL parameters
  let mode: 'request' | 'reset' | 'success' | 'error' = 'request';
  let message = '';

  if (token) {
    mode = 'reset';
  } else if (success === 'true') {
    mode = 'success';
  } else if (error) {
    mode = 'error';
    message = decodeURIComponent(error);
  }

  return (
    <PasswordReset 
      mode={mode}
      token={token || undefined}
      message={message}
    />
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">
          <i className="fas fa-spinner fa-spin text-2xl mr-3"></i>
          Loading...
        </div>
      </div>
    }>
      <PasswordResetContent />
    </Suspense>
  );
}
