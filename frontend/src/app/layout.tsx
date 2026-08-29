import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Liam Traders - Earn & Learn Platform",
  description: "A comprehensive platform for earning through legitimate work and learning skills",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
