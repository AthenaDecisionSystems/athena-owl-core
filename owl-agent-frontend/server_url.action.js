// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

export const SET_SERVER_URL = "SET_SERVER_URL"; // Define action type

export const setServerUrl = (serverUrl) => {
    return (dispatch) => {
        // Some actions in the backend...

        // Inform the reducer
        return (dispatch({ type: SET_SERVER_URL, payload: serverUrl }))
    }
}