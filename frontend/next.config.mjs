/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: [
    'http://192.168.1.132:3000',
    'http://localhost:3000',
  ],
  images: {
    domains: ['localhost'],
  },
}

// تصدير الإعدادات بطريقة ESM
export default nextConfig
