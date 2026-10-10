import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pills — Multi-Agent AI Teammate Platform",
  description: "Enterprise-grade multi-agent SaaS platform with capsule personas and tenant-isolated execution.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
        <div className="fixed inset-0 -z-10 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(14,165,233,0.15),rgba(255,255,255,0))]" />
        {children}
      </body>
    </html>
  );
}
