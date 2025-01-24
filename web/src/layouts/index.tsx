import { Layout } from "antd";
import { Outlet } from "react-router-dom";
import LayoutHeader from "./components/header";
import LayoutFooter from "./components/footer";
import "./index.less";

const LayoutIndex = () => {
    const { Content } = Layout;

    return (
        <Layout className="layout-container">
            <LayoutHeader />
            <Content className="layout-content">
                <Outlet />
            </Content>
            <LayoutFooter />
        </Layout>
    );
};

export default LayoutIndex;
