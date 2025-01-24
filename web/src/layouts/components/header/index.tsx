import React from "react";
import { Layout, Menu, Dropdown } from "antd";
import { HomeOutlined, ScanOutlined, BugOutlined, UserOutlined, LogoutOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import "./index.less";

const LayoutHeader = () => {
    const { Header } = Layout;
    const navigate = useNavigate();

    const menuItems = [
        {
            key: "home",
            icon: <HomeOutlined />,
            label: "首页",
            onClick: () => navigate("/home/index")
        },
        {
            key: "scan",
            icon: <ScanOutlined />,
            label: "扫描",
            onClick: () => navigate("/home/tasks")
        },
        {
            key: "vulns",
            icon: <BugOutlined />,
            label: "漏洞",
            onClick: () => navigate("/home/vulns")
        }
    ];

    const userMenuItems = [
        {
            key: "profile",
            icon: <UserOutlined />,
            label: "个人信息"
        },
        {
            key: "logout",
            icon: <LogoutOutlined />,
            label: "退出登录"
        }
    ];

    return (
        <Header className="layout-header" style={{ display: 'flex', alignItems: 'center' }}>
            <div className="demo-logo" />
            <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['2']}
                items={menuItems}
                style={{ flex: 1, minWidth: 0 }}
            />
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
                <span className="user-dropdown">
                    <UserOutlined />
                    <span>管理员</span>
                </span>
            </Dropdown>
        </Header>
    );
};

export default LayoutHeader;
