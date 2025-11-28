// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Deshabilitar optimizaciones para desarrollo rápido
  experimental: {
    optimizeCss: false,
  },
}

module.exports = nextConfig