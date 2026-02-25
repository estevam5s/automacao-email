'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { Loader2 } from 'lucide-react';

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, checkAuth, loading } = useAppStore();
  const [initializing, setInitializing] = useState(true);

  useEffect(() => {
    const init = async () => {
      await checkAuth();
      setInitializing(false);
    };
    init();
  }, [checkAuth]);

  useEffect(() => {
    if (!initializing) {
      const isAuthPage = pathname?.startsWith('/login');
      
      if (!user && !isAuthPage) {
        router.push('/login');
      } else if (user && isAuthPage) {
        router.push('/');
      }
    }
  }, [user, pathname, initializing, router]);

  if (initializing || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-cyan-400 mx-auto" />
          <p className="mt-4 text-slate-400">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!user && !pathname?.startsWith('/login')) {
    return null;
  }

  return <>{children}</>;
}
