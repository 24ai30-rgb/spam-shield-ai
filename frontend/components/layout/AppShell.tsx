import { Sidebar } from "./Sidebar";

export function AppShell({ children, title, subtitle }: { children: React.ReactNode; title?: string; subtitle?: string }) {
  return (
    <div className="flex min-h-screen bg-paper dark:bg-void-900">
      <Sidebar />
      <main className="flex-1 px-6 py-8 md:px-10 md:py-10 max-w-7xl">
        {title && (
          <div className="mb-8">
            <h1 className="text-2xl md:text-3xl font-bold">{title}</h1>
            {subtitle && <p className="mt-1 text-fog-400">{subtitle}</p>}
          </div>
        )}
        {children}
      </main>
    </div>
  );
}
