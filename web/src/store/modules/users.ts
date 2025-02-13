import { createSlice } from "@reduxjs/toolkit";

interface UserState {
    token: string;
    uuid: number;
    email: string;
    nickname: string;
    role: string;
    isAdmin: boolean;
    isAuditor: boolean;
}

const initialState: UserState = {
    token: sessionStorage.getItem('access_token') || '',
    uuid: 0,
    email: '',
    nickname: '',
    role: '',
    isAdmin: false,
    isAuditor: false
};

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setUserInfo: (state, { payload }) => {
            const { token, uuid, permission, is_admin, is_auditor } = payload;
            state.token = token;
            state.uuid = uuid;
            state.role = permission;
            state.isAdmin = is_admin;
            state.isAuditor = is_auditor;
            sessionStorage.setItem('access_token', token);
            sessionStorage.setItem('user_info', JSON.stringify(payload));
        },
        clearUserInfo: (state) => {
            Object.assign(state, initialState);
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('user_info');
        }
    }
})

export const {setUserInfo, clearUserInfo} = userSlice.actions

export default userSlice.reducer