// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import { SET_LANGUAGE } from "./language.action";

const emptyLanguage = { language: "" };

export default function languageReducer(language = emptyLanguage, action) {
    switch (action.type) {
        case SET_LANGUAGE:
            return { language: action.payload };
        default:
            return language;
    }
};