import { Button, Result } from 'antd';
import { useNavigate } from 'react-router-dom';
import './index.less';


const NOTAuth = () => {
    const navigate = useNavigate();
    const goHome = () => {
        navigate('/home');
    };

    return (
        <Result
            status='403'
            title='403'
            subTitle='抱歉,你无权访问这个页面.'
            extra={
                <Button type='primary' onClick={goHome}>返回首页</Button>
            }
        />
    );
};

export default NOTAuth;

