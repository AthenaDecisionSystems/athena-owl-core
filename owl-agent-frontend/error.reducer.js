// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import { SET_ERROR } from "./error.action";

const emptyError = { error: "" };

export default function errorReducer(error = emptyError, action) {
    switch (action.type) {
        case SET_ERROR:
            return { error: action.payload };
        default:
            return error;
    }
};  