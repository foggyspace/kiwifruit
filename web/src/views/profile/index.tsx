import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message, Row, Col, Descriptions } from 'antd';
import { LockOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import './index.less';

const Profile: React.FC = () => {
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(false);

    const userInfo = useSelector((state: any) => state.user.userInfo);

    const handlePasswordChange = async (values: any) => {
        try {
            setLoading(true);
            const response = await fetch('/api/v1/users/change-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    old_password: values.oldPassword,
                    new_password: values.newPassword,
                    confirm_password: values.confirmPassword
                })
            });

            if (!response.ok) {
                throw new Error('修改密码失败');
            }

            const data = await response.json();
            if (data.code === 0) {
                message.success('密码修改成功');
                form.resetFields();
            } else {
                throw new Error(data.msg || '修改密码失败');
            }
        } catch (error) {
            message.error(error instanceof Error ? error.message : '修改密码失败');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="profile-container">
            <Row gutter={[16, 16]}>
                <Col span={24}>
                    <Card title="基本信息" bordered={false}>
                        <Descriptions column={1}>
                            <Descriptions.Item label="用户名">{userInfo?.username || '-'}</Descriptions.Item>
                            <Descriptions.Item label="邮箱">{userInfo?.email || '-'}</Descriptions.Item>
                            <Descriptions.Item label="角色">{userInfo?.role || '-'}</Descriptions.Item>
                        </Descriptions>
                    </Card>
                </Col>
                <Col span={24}>
                    <Card title="修改密码" bordered={false}>
                        <Form
                            form={form}
                            onFinish={handlePasswordChange}
                            layout="vertical"
                            className="password-form"
                        >
                            <Form.Item
                                name="oldPassword"
                                label="原密码"
                                rules={[
                                    { required: true, message: '请输入原密码' },
                                    { min: 6, max: 22, message: '密码长度必须在6-22位之间' }
                                ]}
                            >
                                <Input.Password
                                    prefix={<LockOutlined />}
                                    placeholder="请输入原密码"
                                />
                            </Form.Item>
                            <Form.Item
                                name="newPassword"
                                label="新密码"
                                rules={[
                                    { required: true, message: '请输入新密码' },
                                    { min: 6, max: 22, message: '密码长度必须在6-22位之间' },
                                    { pattern: /^[A-Za-z0-9_*$@]+$/, message: '密码只能包含字母、数字和特殊字符(_*$@)' }
                                ]}
                            >
                                <Input.Password
                                    prefix={<LockOutlined />}
                                    placeholder="请输入新密码"
                                />
                            </Form.Item>
                            <Form.Item
                                name="confirmPassword"
                                label="确认新密码"
                                dependencies={['newPassword']}
                                rules={[
                                    { required: true, message: '请确认新密码' },
                                    ({ getFieldValue }) => ({
                                        validator(_, value) {
                                            if (!value || getFieldValue('newPassword') === value) {
                                                return Promise.resolve();
                                            }
                                            return Promise.reject(new Error('两次输入的密码不一致'));
                                        },
                                    }),
                                ]}
                            >
                                <Input.Password
                                    prefix={<LockOutlined />}
                                    placeholder="请确认新密码"
                                />
                            </Form.Item>
                            <Form.Item>
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    loading={loading}
                                    className="submit-button"
                                >
                                    确认修改
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Profile;