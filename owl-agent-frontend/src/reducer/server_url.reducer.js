// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import { SET_SERVER_URL } from "./server_url.action";

const localServerUrl = { serverUrl: process.env.REACT_APP_BACKEND_URL };

export default function serverUrlReducer(serverUrl = localServerUrl, action) {
    switch (action.type) {
        case SET_SERVER_URL:
            return { serverUrl: action.payload };
        default:
            return serverUrl;
    }
};  