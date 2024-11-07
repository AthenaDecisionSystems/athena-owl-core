"use server";
export const getEnv = async () => ({
    backendBaseAPI: process.env.NEXT_PUBLIC_BACKEND_BASE_API,
    collectionName: process.env.NEXT_PUBLIC_COLLECTION_NAME,
    demoText: process.env.NEXT_PUBLIC_DEMO_TEXT,
    showSettingsAndDocuments: (process.env.NEXT_PUBLIC_SHOW_SETTINGS_AND_DOCUMENTS?.toLowerCase() === 'true'
        || process.env.NEXT_PUBLIC_SHOW_SETTINGS_AND_DOCUMENTS?.toLowerCase() === 'yes'),
});
