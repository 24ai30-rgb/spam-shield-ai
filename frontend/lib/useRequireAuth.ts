"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api";
import { useAuthStore } from "@/lib/store";

/**
 * Call at the top of any protected page. Hydrates the auth store from the
 * stored JWT on first mount and redirects to /login if there is no valid
 * session. Returns `ready` so pages can avoid a flash of unauthenticated
 * content while the check is in flight.
 */
export function useRequireAuth() {
  const router = useRouter();
  const { user, setUser } = useAuthStore();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (user) {
      setReady(true);
      return;
    }
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }
    authApi
      .me()
      .then((res) => {
        setUser(res.data);
        setReady(true);
      })
      .catch(() => router.replace("/login"));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { ready, user };
}
