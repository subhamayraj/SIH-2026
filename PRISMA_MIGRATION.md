# Prisma migration

The Prisma schema in `prisma/schema.prisma` is a one-to-one mapping of the current PostgreSQL schema. It keeps the existing snake_case table and column names with Prisma `@map`/`@@map` annotations, so using Prisma does not require renaming or rebuilding the current database.

## First-time setup

1. Keep the existing `DATABASE_URL` in `.env`.
2. Install the Node dependencies: `npm install`.
3. Generate the client: `npm run prisma:generate`.
4. Start the Prisma-based API: `npm run dev`.

For the existing database, do **not** run `prisma migrate dev` as the first Prisma command: it would attempt to create tables that already exist. The schema already describes the current database. If the live database has drifted from the SQLAlchemy models, run `npx prisma db pull` first and review the resulting schema before generating the client.

For a new empty database, run `npm run prisma:migrate -- --name init` and commit the generated migration before deploying with `npm run prisma:deploy`.

## Cutover

The Prisma API entry point is `src/server.ts`; it maintains the existing HTTP endpoints, including `/competency/user/:userId` and `/recommendations/user/:userId`. Once it has been tested against the current database, use it in place of `main.py`. Leave the SQLAlchemy files in place only until the cutover is confirmed, then remove the unused Python ORM and Alembic dependencies together.
