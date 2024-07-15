import { Button, Result } from "antd";
import { useNavigate } from "react-router-dom";
import "./index.less";

const NotNetwork = () => {
	const navigate = useNavigate();
	const goHome = () => {
		navigate('/home');
	};
	return (
		<Result
			status="500"
			title="500"
			subTitle="抱歉,服务出错了!"
			extra={
				<Button type="primary" onClick={goHome}>
					返回首页
				</Button>
			}
		/>
	);
};

export default NotNetwork;
