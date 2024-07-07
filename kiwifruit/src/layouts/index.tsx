import { Layout } from "antd";

import LayoutHeader from "./components/footer";
import LayoutFooter from "./components/header";

import "./index.less";


const LayoutIndex = () => {
    const { Content } = Layout;

    return (
        <section className="container">
            <Layout>
                <LayoutHeader></LayoutHeader>
                <Content>
                    <Outlet></Outlet>
                </Content>
                <LayoutFooter></LayoutFooter>
            </Layout>
        </section>
    );
};

export default LayoutIndex;
