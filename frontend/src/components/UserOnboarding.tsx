'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  component: React.ReactNode;
  completed: boolean;
}

interface OnboardingProps {
  show: boolean;
  onComplete: () => void;
  onSkip: () => void;
}

const UserOnboarding: React.FC<OnboardingProps> = ({ show, onComplete, onSkip }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const { user } = useAuth();
  const router = useRouter();

  const steps: OnboardingStep[] = [
    {
      id: 'welcome',
      title: 'Welcome to Nexora!',
      description: 'Your journey to authentic influencer analysis starts here.',
      component: (
        <div className="text-center">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
            <i className="fas fa-star text-white text-3xl"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-4">Welcome to Nexora!</h3>
          <p className="text-gray-300 mb-6">
            We're excited to help you discover authentic influencers and analyze their content with our AI-powered platform.
          </p>
          <div className="bg-gray-800 rounded-lg p-4 mb-6">
            <h4 className="text-yellow-400 font-semibold mb-2">What you can do with Nexora:</h4>
            <ul className="text-left text-gray-300 space-y-2">
              <li><i className="fas fa-check text-green-400 mr-2"></i>Analyze influencer authenticity across multiple platforms</li>
              <li><i className="fas fa-check text-green-400 mr-2"></i>Get detailed engagement and content quality scores</li>
              <li><i className="fas fa-check text-green-400 mr-2"></i>Track analysis history and compare influencers</li>
              <li><i className="fas fa-check text-green-400 mr-2"></i>Access real-time data from Instagram, YouTube, TikTok, and more</li>
            </ul>
          </div>
        </div>
      ),
      completed: false
    },
    {
      id: 'profile_setup',
      title: 'Complete Your Profile',
      description: 'Set up your profile to get personalized recommendations.',
      component: (
        <div className="text-center">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
            <i className="fas fa-user text-white text-3xl"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-4">Complete Your Profile</h3>
          <p className="text-gray-300 mb-6">
            Help us personalize your experience by completing your profile information.
          </p>
          <div className="bg-gray-800 rounded-lg p-4 mb-6">
            <div className="text-left space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Profile Name</span>
                <span className="text-green-400">
                  <i className="fas fa-check mr-1"></i>
                  {user?.full_name ? 'Complete' : 'Pending'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Email Verification</span>
                <span className="text-green-400">
                  <i className="fas fa-check mr-1"></i>
                  {user?.is_verified ? 'Verified' : 'Pending'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Account Type</span>
                <span className="text-green-400">
                  <i className="fas fa-check mr-1"></i>
                  {user?.role ? user.role.charAt(0).toUpperCase() + user.role.slice(1) : 'Set'}
                </span>
              </div>
            </div>
          </div>
          <button
            onClick={() => router.push('/profile')}
            className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 mb-3"
          >
            Complete Profile Setup
          </button>
        </div>
      ),
      completed: false
    },
    {
      id: 'first_analysis',
      title: 'Try Your First Analysis',
      description: 'Learn how to analyze an influencer with our powerful tools.',
      component: (
        <div className="text-center">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
            <i className="fas fa-chart-line text-white text-3xl"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-4">Try Your First Analysis</h3>
          <p className="text-gray-300 mb-6">
            Ready to analyze your first influencer? Let's walk through the process together.
          </p>
          <div className="bg-gray-800 rounded-lg p-4 mb-6">
            <h4 className="text-yellow-400 font-semibold mb-3">How to analyze an influencer:</h4>
            <div className="text-left space-y-3">
              <div className="flex items-start">
                <div className="w-6 h-6 bg-yellow-400 text-black rounded-full flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</div>
                <div>
                  <p className="text-white font-medium">Choose a Platform</p>
                  <p className="text-gray-400 text-sm">Select from Instagram, YouTube, TikTok, Facebook, or LinkedIn</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="w-6 h-6 bg-yellow-400 text-black rounded-full flex items-center justify-center text-sm font-bold mr-3 mt-0.5">2</div>
                <div>
                  <p className="text-white font-medium">Enter Username</p>
                  <p className="text-gray-400 text-sm">Type the influencer's username (without @ symbol)</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="w-6 h-6 bg-yellow-400 text-black rounded-full flex items-center justify-center text-sm font-bold mr-3 mt-0.5">3</div>
                <div>
                  <p className="text-white font-medium">Get Results</p>
                  <p className="text-gray-400 text-sm">View authenticity score, engagement analysis, and detailed insights</p>
                </div>
              </div>
            </div>
          </div>
          <button
            onClick={() => router.push('/dashboard')}
            className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300 mb-3"
          >
            Start Your First Analysis
          </button>
        </div>
      ),
      completed: false
    },
    {
      id: 'features_overview',
      title: 'Explore Key Features',
      description: 'Discover all the powerful features available to you.',
      component: (
        <div className="text-center">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full flex items-center justify-center">
            <i className="fas fa-rocket text-white text-3xl"></i>
          </div>
          <h3 className="text-2xl font-bold text-white mb-4">Explore Key Features</h3>
          <p className="text-gray-300 mb-6">
            Get the most out of Nexora by exploring these powerful features.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="bg-gray-800 rounded-lg p-4">
              <i className="fas fa-history text-yellow-400 text-2xl mb-2"></i>
              <h4 className="text-white font-semibold mb-1">Analysis History</h4>
              <p className="text-gray-400 text-sm">Track and compare all your previous analyses</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <i className="fas fa-user-cog text-yellow-400 text-2xl mb-2"></i>
              <h4 className="text-white font-semibold mb-1">Profile Settings</h4>
              <p className="text-gray-400 text-sm">Customize your account and preferences</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <i className="fas fa-download text-yellow-400 text-2xl mb-2"></i>
              <h4 className="text-white font-semibold mb-1">Export Reports</h4>
              <p className="text-gray-400 text-sm">Download detailed analysis reports</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <i className="fas fa-bell text-yellow-400 text-2xl mb-2"></i>
              <h4 className="text-white font-semibold mb-1">Notifications</h4>
              <p className="text-gray-400 text-sm">Stay updated with analysis results</p>
            </div>
          </div>
        </div>
      ),
      completed: false
    }
  ];

  const handleNext = () => {
    const currentStepId = steps[currentStep].id;
    if (!completedSteps.includes(currentStepId)) {
      setCompletedSteps(prev => [...prev, currentStepId]);
    }

    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    // Mark onboarding as completed in localStorage
    localStorage.setItem('nexora_onboarding_completed', 'true');
    onComplete();
  };

  const handleSkipAll = () => {
    localStorage.setItem('nexora_onboarding_completed', 'true');
    onSkip();
  };

  const progressPercentage = ((currentStep + 1) / steps.length) * 100;

  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-900 rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-700">
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
                Getting Started
              </h2>
              <p className="text-gray-400">Step {currentStep + 1} of {steps.length}</p>
            </div>
            <button
              onClick={handleSkipAll}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <i className="fas fa-times text-xl"></i>
            </button>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {steps[currentStep].component}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex items-center justify-between">
          <button
            onClick={handleSkipAll}
            className="text-gray-400 hover:text-white transition-colors"
          >
            Skip Tour
          </button>
          
          <div className="flex items-center space-x-3">
            {currentStep > 0 && (
              <button
                onClick={handlePrevious}
                className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Previous
              </button>
            )}
            <button
              onClick={handleNext}
              className="px-6 py-2 bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold rounded-lg hover:from-yellow-500 hover:to-orange-600 transition-all duration-300"
            >
              {currentStep === steps.length - 1 ? 'Get Started' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserOnboarding;
