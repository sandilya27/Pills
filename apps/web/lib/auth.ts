import { betterAuth } from "better-auth";
import { organization, bearer } from "better-auth/plugins";
import { Pool } from "pg";

export const pgPool = new Pool({
  host: process.env.POSTGRES_HOST || "127.0.0.1",
  port: Number(process.env.POSTGRES_PORT || 5432),
  user: process.env.POSTGRES_USER || "pills",
  password: process.env.POSTGRES_PASSWORD || "pills",
  database: process.env.POSTGRES_DB || "pills",
});

export const auth = betterAuth({
  database: pgPool,
  secret: process.env.BETTER_AUTH_SECRET || "pills-development-secret-key-change-in-production-min-32-chars",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
    }),
    bearer(),
  ],
});
