/** @type {import('next').NextConfig} */
const nextConfig = {
  // Optimize for Docker deployments by outputting a standalone folder
  // This drastically reduces the Docker image size.
  output: 'standalone',
  // Disable x-powered-by header for security
  poweredByHeader: false,
};

module.exports = nextConfig;
