import React, { useState, useEffect } from 'react';
import { Table, Button, Input, Space, Tag, message, Form } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import axios from 'axios';
import DrawerForm from '@/components/DrawerForm';

const TasksList = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [drawerVisible, setDrawerVisible] = useState(false);
    const [form] = Form.useForm();
    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 10,
        total: 0
    });
    const [searchText, setSearchText] = useState('');

    const fetchTasks = async (page = 1, size = 10) => {
        setLoading(true);
        try {
            const response = await axios.get(`/api/v1/tasks?page=${page}&size=${size}`);
            if (response.data.code === 0) {
                setTasks(response.data.data.items);
                setPagination({
                    ...pagination,
                    current: page,
                    total: response.data.data.total
                });
            }
        } catch (error) {
            message.error('获取任务列表失败');
        }
        setLoading(false);
    };

    const handleTableChange = (pagination) => {
        fetchTasks(pagination.current, pagination.pageSize);
    };

    const startTask = async (taskId) => {
        try {
            const response = await axios.post(`/api/v1/tasks/${taskId}/start`);
            if (response.data.code === 0) {
                message.success('任务启动成功');
                fetchTasks(pagination.current, pagination.pageSize);
            }
        } catch (error) {
            message.error('启动任务失败');
        }
    };

    const handleCreateTask = async (values) => {
        try {
            const response = await axios.post('/api/v1/tasks', values);
            if (response.data.code === 0) {
                message.success('创建任务成功');
                setDrawerVisible(false);
                form.resetFields();
                fetchTasks();
            }
        } catch (error) {
            message.error('创建任务失败');
        }
    };

    const columns = [
        {
            title: '任务名称',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: '目标URL',
            dataIndex: 'target_url',
            key: 'target_url',
        },
        {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            render: (status) => {
                let color = 'default';
                let text = '未知';
                switch (status) {
                    case 0:
                        color = 'default';
                        text = '待执行';
                        break;
                    case 1:
                        color = 'processing';
                        text = '运行中';
                        break;
                    case 2:
                        color = 'success';
                        text = '已完成';
                        break;
                    case 3:
                        color = 'error';
                        text = '失败';
                        break;
                }
                return <Tag color={color}>{text}</Tag>;
            }
        },
        {
            title: '创建时间',
            dataIndex: 'create_time',
            key: 'create_time',
        },
        {
            title: '操作',
            key: 'action',
            render: (_, record) => (
                <Space size="middle">
                    {record.status === 0 && (
                        <Button type="link" onClick={() => startTask(record.id)}>启动扫描</Button>
                    )}
                    <Button type="link">查看详情</Button>
                </Space>
            ),
        },
    ];

    useEffect(() => {
        fetchTasks();
    }, []);

    const formContent = (
        <>
            <Form.Item
                name="name"
                label="任务名称"
                rules={[{ required: true, message: '请输入任务名称' }]}
            >
                <Input placeholder="请输入任务名称" />
            </Form.Item>
            <Form.Item
                name="target_url"
                label="目标URL"
                rules={[{ required: true, message: '请输入目标URL' }]}
            >
                <Input placeholder="请输入目标URL" />
            </Form.Item>
            <Form.Item
                name="scan_policy"
                label="扫描策略"
                rules={[{ required: true, message: '请选择扫描策略' }]}
                initialValue="default"
            >
                <Input placeholder="请选择扫描策略" />
            </Form.Item>
        </>
    );

    return (
        <div style={{ padding: '24px' }}>
            <div style={{ marginBottom: '16px' }}>
                <Space>
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => setDrawerVisible(true)}>新建任务</Button>
                    <Input
                        placeholder="搜索任务"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 200 }}
                    />
                </Space>
            </div>
            <Table
                columns={columns}
                dataSource={tasks}
                rowKey="id"
                pagination={pagination}
                loading={loading}
                onChange={handleTableChange}
            />
            <DrawerForm
                title="新建扫描任务"
                visible={drawerVisible}
                onClose={() => setDrawerVisible(false)}
                onFinish={handleCreateTask}
                form={form}
            >
                {formContent}
            </DrawerForm>
        </div>
    );
};

export default TasksList;
