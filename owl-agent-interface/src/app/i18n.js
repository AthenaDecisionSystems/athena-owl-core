// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from "./locales/en/global.json";
import es from "./locales/es/global.json";
import fr from "./locales/fr/global.json";
import nl from "./locales/nl/global.json";

const fallbackLng = ['en'];

i18n
    .use(initReactI18next) // pass the i18n instance to react-i18next.
    .init({
        fallbackLng, // fallback language is english.
        resources: { en: { translation: en }, es: { translation: es }, fr: { translation: fr }, nl: { translation: nl } },
        whitelist: ['en', 'es', 'fr', 'nl'],
        debug: false,
        interpolation: {
            escapeValue: false, // no need for react. it escapes by default
        },
        initImmediate: false,
    });

// fetch locale from settings

export default i18n;