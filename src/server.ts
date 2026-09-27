import "dotenv/config";
import express, { type NextFunction, type Request, type Response } from "express";
import { Prisma } from "@prisma/client";
import { prisma } from "./prisma.js";

const app = express();
const port = Number(process.env.PORT ?? 8000);

app.use(express.json());

const numberValue = (value: Prisma.Decimal | null): number | null =>
  value === null ? null : value.toNumber();

const userId = (request: Request, response: Response): number | undefined => {
  const id = Number(request.params.userId);
  if (!Number.isInteger(id) || id < 1) {
    response.status(400).json({ detail: "user_id must be a positive integer" });
    return undefined;
  }
  return id;
};

app.get("/", (_request, response) => {
  response.json({ message: "KarmaPathAI API is running!" });
});

app.get("/users", async (_request, response) => {
  const users = await prisma.user.findMany({
    select: { id: true, name: true, email: true, role: true, department: true, designation: true },
  });
  response.json(users);
});

app.get("/competencies", async (_request, response) => {
  const profiles = await prisma.competencyProfile.findMany({ include: { skill: true } });
  response.json(profiles.map((profile) => ({
    skill: profile.skill.skillName,
    domain: profile.skill.domain,
    current_level: profile.currentLevel,
    required_level: profile.skill.requiredLevel,
    gap_score: numberValue(profile.gapScore),
  })));
});

app.get("/courses", async (_request, response) => {
  const courses = await prisma.course.findMany();
  response.json(courses.map(({ embedding: _embedding, ...course }) => course));
});

app.get("/recommendations", async (_request, response) => {
  const recommendations = await prisma.recommendation.findMany({ include: { course: true } });
  response.json(recommendations.map((recommendation) => ({
    id: recommendation.id,
    user_id: recommendation.userId,
    course: recommendation.course.title,
    match_score: numberValue(recommendation.matchScore),
    status: recommendation.status,
    reasoning: recommendation.reasoning,
  })));
});

app.get("/enrollments", async (_request, response) => {
  const enrollments = await prisma.enrollment.findMany({ include: { course: true } });
  response.json(enrollments.map((enrollment) => ({
    id: enrollment.id,
    user_id: enrollment.userId,
    course: enrollment.course.title,
    status: enrollment.status,
    progress: numberValue(enrollment.progressPct),
  })));
});

app.get("/learning-materials", async (_request, response) => {
  const materials = await prisma.learningMaterial.findMany();
  response.json(materials.map((material) => ({
    id: material.id,
    uploaded_by: material.uploadedBy,
    filename: material.filename,
    content_type: material.contentType,
    extracted_text: material.extractedText,
  })));
});

app.get("/quizzes", async (_request, response) => {
  const quizzes = await prisma.quiz.findMany();
  response.json(quizzes.map((quiz) => ({
    id: quiz.id,
    material_id: quiz.materialId,
    title: quiz.title,
    questions: quiz.questionsJson,
  })));
});

app.get("/quiz-attempts", async (_request, response) => {
  const attempts = await prisma.quizAttempt.findMany();
  response.json(attempts.map((attempt) => ({
    id: attempt.id,
    quiz_id: attempt.quizId,
    user_id: attempt.userId,
    answers: attempt.answersJson,
    score: numberValue(attempt.score),
    max_score: numberValue(attempt.maxScore),
  })));
});

app.get("/competency/user/:userId", async (request, response) => {
  const id = userId(request, response);
  if (id === undefined) return;

  const user = await prisma.user.findUnique({
    where: { id },
    include: { competencyProfiles: { include: { skill: true } } },
  });
  if (!user) return response.status(404).json({ detail: "User not found" });

  response.json({
    user_id: user.id,
    user_name: user.name,
    department: user.department,
    designation: user.designation,
    competency_gaps: user.competencyProfiles.map((profile) => ({
      skill: profile.skill.skillName,
      domain: profile.skill.domain,
      required_level: profile.skill.requiredLevel,
      current_level: profile.currentLevel,
      gap_score: Math.max(profile.skill.requiredLevel - profile.currentLevel, 0),
    })),
  });
});

app.get("/recommendations/user/:userId", async (request, response) => {
  const id = userId(request, response);
  if (id === undefined) return;

  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) return response.status(404).json({ detail: "User not found" });

  const profiles = await prisma.competencyProfile.findMany({
    where: { userId: id, gapScore: { gt: 0 } },
    include: { skill: true },
    orderBy: { gapScore: "desc" },
  });

  const recommendations = [];
  for (const profile of profiles) {
    const courses = await prisma.course.findMany({ where: { domain: profile.skill.domain } });
    for (const course of courses) {
      const existing = await prisma.recommendation.findFirst({
        where: { userId: id, courseId: course.id },
      });
      const gapScore = numberValue(profile.gapScore) ?? 0;
      const recommendation = existing ?? await prisma.recommendation.create({
        data: {
          userId: id,
          courseId: course.id,
          matchScore: Math.min(100, 70 + Math.trunc(gapScore * 10)),
          status: "recommended",
          reasoning: `Recommended because the employee has a competency gap in ${profile.skill.skillName}.`,
        },
      });
      recommendations.push({
        skill: profile.skill.skillName,
        domain: profile.skill.domain,
        gap_score: gapScore,
        course_id: course.id,
        course_title: course.title,
        provider: course.provider,
        difficulty: course.difficulty,
        match_score: numberValue(recommendation.matchScore),
        reasoning: recommendation.reasoning,
      });
    }
  }

  response.json({ user_id: user.id, user_name: user.name, recommendations });
});

app.use((error: unknown, _request: Request, response: Response, _next: NextFunction) => {
  console.error(error);
  response.status(500).json({ detail: "Internal server error" });
});

const server = app.listen(port, () => {
  console.log(`KarmaPathAI API listening on http://localhost:${port}`);
});

const shutdown = async () => {
  server.close();
  await prisma.$disconnect();
};
process.once("SIGINT", shutdown);
process.once("SIGTERM", shutdown);
