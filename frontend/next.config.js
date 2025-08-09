/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Handle hydration issues with browser extensions
  compiler: {
    // Remove console.logs in production
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  // Custom webpack config
  webpack: (config, { dev }) => {
    if (dev) {
      // Suppress specific hydration warnings for browser extensions
      config.infrastructureLogging = {
        level: 'error',
      };
    }
    return config;
  },
}

module.exports = nextConfig
