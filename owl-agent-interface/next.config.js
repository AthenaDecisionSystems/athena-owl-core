module.exports = {
    output: 'standalone',
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8002/api/:path*',
            }
        ]
    }
}