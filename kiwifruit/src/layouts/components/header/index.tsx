import React from "react";
import { Layout, Menu } from "antd";


const LayoutHeader = () => {
    const { Header } = Layout;

    return (
        <Header style={{ display: "flex", alignItems: "center"}}>
            <div className="header-logo" />
        </Header>
    );
};

export default LayoutHeader;
