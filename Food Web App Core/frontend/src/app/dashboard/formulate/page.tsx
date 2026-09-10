'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function FormulateIndexRedirect() {
  const router = useRouter();
  useEffect(() => {
    router.replace('/dashboard/formulate/guided');
  }, [router]);

  return null;
}
