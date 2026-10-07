import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'ImóvelRadar',
  description: 'Plataforma inicial de inteligência imobiliária',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
