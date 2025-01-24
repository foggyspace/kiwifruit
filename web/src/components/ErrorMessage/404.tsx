import { Button, Result } from "antd";
import { useNavigate } from "react-router-dom";
import "./index.less";

const NotFound = () => {
	const navigate = useNavigate();
	const goHome = () => {
		navigate('/home/index');
	};
	return (
		<Result
			status="404"
			title="404"
			subTitle="抱歉你访问的页面不存在!"
			extra={
				<Button type="primary" onClick={goHome}>
					返回首页
				</Button>
			}
		/>
	);
};

export default NotFound;
