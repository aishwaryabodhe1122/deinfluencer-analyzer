'use client';

import React, { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import EmailVerification from '../../components/EmailVerification';

function EmailVerificationContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const email = searchParams.get('email');
  const verified = searchParams.get('verified');
  const error = searchParams.get('error');

  // Determine the mode based on URL parameters
  let mode: 'pending' | 'verify' | 'success' | 'error' = 'pending';
  let message = '';

  if (token) {
    mode = 'verify';
  } else if (verified === 'true') {
    mode = 'success';
  } else if (error) {
    mode = 'error';
    message = decodeURIComponent(error);
  } else if (email) {
    mode = 'pending';
  }

  return (
    <EmailVerification 
      mode={mode}
      email={email || undefined}
      token={token || undefined}
      message={message}
    />
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">
          <i className="fas fa-spinner fa-spin text-2xl mr-3"></i>
          Loading...
        </div>
      </div>
    }>
      <EmailVerificationContent />
    </Suspense>
  );
}
