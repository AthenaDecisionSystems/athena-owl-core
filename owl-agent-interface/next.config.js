module.exports = {
    output: 'standalone',
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                //destination: 'http://ibu-backend:8000/api/:path*',
                destination: 'http://ibu-backend.ibu.svc.cluster.local:8000/api/:path*',
            }
        ]
    }
}