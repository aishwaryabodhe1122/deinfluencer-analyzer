'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export const useOnboarding = () => {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [isNewUser, setIsNewUser] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      // Check if user has completed onboarding
      const onboardingCompleted = localStorage.getItem('nexora_onboarding_completed');
      const userOnboardingKey = `nexora_onboarding_${user.id}`;
      const userOnboardingCompleted = localStorage.getItem(userOnboardingKey);

      // Show onboarding if:
      // 1. User hasn't completed global onboarding AND
      // 2. User hasn't completed their specific onboarding AND
      // 3. User account is less than 24 hours old (new user)
      const accountAge = user.created_at ? 
        (Date.now() - new Date(user.created_at).getTime()) / (1000 * 60 * 60) : 0;
      
      const shouldShowOnboarding = 
        !onboardingCompleted && 
        !userOnboardingCompleted && 
        accountAge < 24; // Less than 24 hours old

      setIsNewUser(accountAge < 24);
      setShowOnboarding(shouldShowOnboarding);
    }
  }, [user]);

  const completeOnboarding = () => {
    if (user) {
      localStorage.setItem('nexora_onboarding_completed', 'true');
      localStorage.setItem(`nexora_onboarding_${user.id}`, 'true');
    }
    setShowOnboarding(false);
  };

  const skipOnboarding = () => {
    if (user) {
      localStorage.setItem('nexora_onboarding_completed', 'true');
      localStorage.setItem(`nexora_onboarding_${user.id}`, 'true');
    }
    setShowOnboarding(false);
  };

  const resetOnboarding = () => {
    localStorage.removeItem('nexora_onboarding_completed');
    if (user) {
      localStorage.removeItem(`nexora_onboarding_${user.id}`);
    }
    setShowOnboarding(true);
  };

  return {
    showOnboarding,
    isNewUser,
    completeOnboarding,
    skipOnboarding,
    resetOnboarding
  };
};
