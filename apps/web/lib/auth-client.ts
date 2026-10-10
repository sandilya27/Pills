import { createAuthClient } from "better-auth/client";
import { organizationClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: typeof window !== "undefined" ? window.location.origin : (process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000"),
  plugins: [
    organizationClient(),
  ],
});

export const {
  signIn,
  signOut,
  signUp,
  useSession,
  organization: orgApi,
} = authClient;
