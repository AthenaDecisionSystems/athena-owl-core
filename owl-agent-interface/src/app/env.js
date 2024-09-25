"use server";
export const getEnv = async () => ({
    backendBaseAPI: process.env.NEXT_PUBLIC_BACKEND_BASE_API,
    demoText: process.env.NEXT_PUBLIC_DEMO_TEXT,
});
