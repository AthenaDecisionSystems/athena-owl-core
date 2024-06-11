// Copyright 2024, Athena Decision Systems
// @author Joel Milgram

export const SET_ERROR = "SET_ERROR"; // Define action type

export const setError = (error) => {
    return (dispatch) => {
        // Some actions in the backend...

        // Inform the reducer
        return (dispatch({ type: SET_ERROR, payload: error }))
    }
}