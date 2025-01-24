import React from 'react';
import { Drawer, Form, Button } from 'antd';

interface DrawerFormProps {
    title: string;
    visible: boolean;
    onClose: () => void;
    onFinish: (values: any) => void;
    children: React.ReactNode;
    width?: number;
    form?: any;
}

const DrawerForm: React.FC<DrawerFormProps> = ({
    title,
    visible,
    onClose,
    onFinish,
    children,
    width = 400,
    form,
}) => {
    const [formInstance] = Form.useForm();
    const currentForm = form || formInstance;

    const handleSubmit = async (values: any) => {
        await onFinish(values);
        currentForm.resetFields();
    };

    const handleClose = () => {
        currentForm.resetFields();
        onClose();
    };

    return (
        <Drawer
            title={title}
            width={width}
            onClose={handleClose}
            open={visible}
            bodyStyle={{ paddingBottom: 80 }}
        >
            <Form
                form={currentForm}
                layout="vertical"
                onFinish={handleSubmit}
            >
                {children}
                <Form.Item>
                    <Button type="primary" htmlType="submit" block>
                        提交
                    </Button>
                </Form.Item>
            </Form>
        </Drawer>
    );
};

export default DrawerForm;