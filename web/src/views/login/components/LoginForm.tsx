import { useState } from "react";
import { Button, Form, Input, message, Checkbox } from "antd";
import { useNavigate } from "react-router-dom";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { useDispatch } from "react-redux";
import { setUserInfo } from "../../../store/modules/users";
import "./LoginForm.less";

interface LoginFormState {
    username: string;
    password: string;
    remember: boolean;
}

const LoginFormComponent = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const navigate = useNavigate();

    const dispatch = useDispatch();

    const onFinish = async (values: LoginFormState) => {
        try {
            setLoading(true);
            const response = await fetch('/api/v1/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: values.username,
                    password: values.password
                })
            });

            if (!response.ok) {
                throw new Error('登录失败');
            }

            const data = await response.json();
            if (data.code === 0) {
                dispatch(setUserInfo(data.data));
                if (values.remember) {
                    localStorage.setItem('username', values.username);
                } else {
                    localStorage.removeItem('username');
                }
                message.success("登录成功！");
                navigate("/home");
            } else {
                throw new Error(data.msg || '登录失败');
            }
        } catch (error) {
            message.error(error instanceof Error ? error.message : "登录失败，请检查用户名和密码！");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <Form
                name="login-form"
                className="login-form"
                initialValues={{
                    remember: true,
                    username: localStorage.getItem('username') || ''
                }}
                onFinish={onFinish}
            >
                <h2 className="login-title">系统登录</h2>
                <Form.Item
                    name="username"
                    rules={[{ required: true, message: "请输入用户名！" }]}
                >
                    <Input
                        prefix={<UserOutlined />}
                        placeholder="用户名"
                        size="large"
                    />
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{ required: true, message: "请输入密码！" }]}
                >
                    <Input.Password
                        prefix={<LockOutlined />}
                        placeholder="密码"
                        size="large"
                    />
                </Form.Item>
                <Form.Item>
                    <Form.Item name="remember" valuePropName="checked" noStyle>
                        <Checkbox>记住用户名</Checkbox>
                    </Form.Item>
                </Form.Item>
                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                        className="login-form-button"
                        loading={loading}
                        block
                        size="large"
                    >
                        登录
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default LoginFormComponent;

