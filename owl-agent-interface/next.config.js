module.exports = {
    output: 'standalone',
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://ibu-backend:8002/api/:path*',
            }
        ]
    }
}