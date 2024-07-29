"use server";
export const getEnv = async () => ({
    title: process.env.NEXT_PUBLIC_OWL_AGENT_TITLE,
    description: process.env.NEXT_PUBLIC_OWL_AGENT_DESCRIPTION,
    backendBaseAPI: process.env.NEXT_PUBLIC_BACKEND_BASE_API,
    demoText: process.env.NEXT_PUBLIC_DEMO_TEXT,
});

export const checkEnv = async (env) => {
    // If the user accesses some pages directly, the env is not loaded yet
    if (env.backendBaseAPI) {
        return env;
    } else {
        return getEnv();
    }
};
