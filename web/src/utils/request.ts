import axios from 'axios';
import { message } from 'antd';

const request = axios.create({
    baseURL: '/api',
    timeout: 10000,
});

// 请求拦截器
request.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
request.interceptors.response.use(
    (response) => {
        const { data } = response;
        if (data.error_code === 200 || data.error_code === 0) {
            return data.data || data;
        } else {
            message.error(data.msg || '请求失败');
            console.log("request...", data)
            return Promise.reject(new Error(data.msg || '请求失败'));
        }
    },
    (error) => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，清除token并跳转到登录页
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                    break;
                default:
                    message.error(error.response.data.msg || '请求失败');
            }
        } else {
            message.error('网络错误，请稍后重试');
        }
        return Promise.reject(error);
    }
);

export default request;