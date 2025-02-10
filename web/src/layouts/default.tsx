import { Navbar } from "@/components/navbar.tsx";

export default function DefaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex flex-col h-screen">
      <Navbar />
      <main className="max-w-full flex-grow pt-16">{children}</main>
      <footer className="w-full flex items-center justify-center py-3">
      </footer>
    </div>
  );
}
