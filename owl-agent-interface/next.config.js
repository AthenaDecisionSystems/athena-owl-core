module.exports = {
    output: 'standalone',
    trailingSlash: true,
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://ibu-backend:8000/api/:path*',
            }
        ]
    }
}