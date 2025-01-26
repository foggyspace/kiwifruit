import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice({
    name: "user",
    initialState: {
        name: "",
        email: "",
        password: "",
        token: ""
    },
    reducers: {
        setToken: (state, {payload}) => {
            state.token = payload
            sessionStorage.setItem("access_token", state.token)
        },
        removeToken: (state) => {
            state.token = ""
            sessionStorage.removeItem("access_token")
        }
    }
})

export const {setToken, removeToken} = userSlice.actions

export default userSlice.reducer