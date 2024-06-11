// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

import { combineReducers } from "redux"
import errorReducer from "./error.reducer";
import serverUrlReducer from "./server_url.reducer";
import languageReducer from "./language.reducer";

export default combineReducers({
    // Add reducers here
    errorReducer,
    serverUrlReducer,
    languageReducer,
})