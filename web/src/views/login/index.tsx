import React from "react";
import LoginForm from "./components/LoginForm";
import "./index.less";
import loginBg from "../../assets/long-bg.png";

const Login: React.FC = () => {
    return (
        <div className="login-page">
            <div className="login-content">
                <div className="login-left">
                    <img src={loginBg} alt="Security" className="login-image" />
                </div>
                <div className="login-right">
                    <LoginForm />
                </div>
            </div>
        </div>
    );
};

export default Login;
