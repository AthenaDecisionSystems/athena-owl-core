// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

export const SET_LANGUAGE = "SET_LANGUAGE"; // Define action type

export const setLanguage = (language) => {
    return (dispatch) => {
        // Some actions in the backend...

        // Inform the reducer
        return (dispatch({ type: SET_LANGUAGE, payload: language }))
    }
}