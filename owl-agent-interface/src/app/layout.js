import './globals.scss';

import { Providers } from './providers';

export const metadata = {
  title: 'OWL Agent',
  description:
    'This is the OWL Agent frontend from Athena Decision Systems.  You can leverage this framework for Hybrid AI based applications.  Visit http://www.athenadecisions.com',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <title>{metadata.title}</title>
        <meta name="description" content={metadata.description} />
        <link
          rel="icon"
          href="//img1.wsimg.com/isteam/ip/597ca088-d8e8-4dfb-a521-a0653722a82c/favicon/91d06154-a6a9-4e42-81ca-140770bfcbf1.png/:/rs=w:16,h:16,m"
          sizes="16x16"
        />
        <link
          rel="icon"
          href="//img1.wsimg.com/isteam/ip/597ca088-d8e8-4dfb-a521-a0653722a82c/favicon/91d06154-a6a9-4e42-81ca-140770bfcbf1.png/:/rs=w:24,h:24,m"
          sizes="24x24"
        />
        <link
          rel="icon"
          href="//img1.wsimg.com/isteam/ip/597ca088-d8e8-4dfb-a521-a0653722a82c/favicon/91d06154-a6a9-4e42-81ca-140770bfcbf1.png/:/rs=w:32,h:32,m"
          sizes="32x32"
        />
        <link
          rel="icon"
          href="//img1.wsimg.com/isteam/ip/597ca088-d8e8-4dfb-a521-a0653722a82c/favicon/91d06154-a6a9-4e42-81ca-140770bfcbf1.png/:/rs=w:48,h:48,m"
          sizes="48x48"
        />
        <link
          rel="icon"
          href="//img1.wsimg.com/isteam/ip/597ca088-d8e8-4dfb-a521-a0653722a82c/favicon/91d06154-a6a9-4e42-81ca-140770bfcbf1.png/:/rs=w:64,h:64,m"
          sizes="64x64"
        />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
