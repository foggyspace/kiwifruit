import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { BugOutlined, AlertOutlined, SafetyOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import './index.less';

const Home: React.FC = () => {
    // 模拟数据 - 实际项目中应该从API获取
    const vulnerabilityData = [
        { date: '2024-01', count: 5 },
        { date: '2024-02', count: 8 },
        { date: '2024-03', count: 3 },
        { date: '2024-04', count: 12 },
        { date: '2024-05', count: 6 },
    ];

    const vulnerabilityTypes = [
        { type: 'SQL注入', value: 25 },
        { type: 'XSS', value: 18 },
        { type: '文件包含', value: 15 },
        { type: '命令执行', value: 10 },
        { type: '其他', value: 8 },
    ];

    const lineOption = {
        xAxis: {
            type: 'category',
            data: vulnerabilityData.map(item => item.date)
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: vulnerabilityData.map(item => item.count),
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 8
        }]
    };

    const pieOption = {
        series: [{
            type: 'pie',
            data: vulnerabilityTypes.map(item => ({
                name: item.type,
                value: item.value
            })),
            radius: '80%',
            label: {
                position: 'outside'
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };

    return (
        <div className="home-container">
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="总漏洞数"
                            value={76}
                            prefix={<BugOutlined />}
                            valueStyle={{ color: '#cf1322' }}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="高危漏洞"
                            value={23}
                            prefix={<AlertOutlined />}
                            valueStyle={{ color: '#fa8c16' }}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="已修复"
                            value={45}
                            prefix={<SafetyOutlined />}
                            valueStyle={{ color: '#52c41a' }}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
                <Col xs={24} lg={14}>
                    <Card title="漏洞趋势">
                        <ReactECharts option={lineOption} style={{ height: '300px' }} />
                    </Card>
                </Col>
                <Col xs={24} lg={10}>
                    <Card title="漏洞类型分布">
                        <ReactECharts option={pieOption} style={{ height: '300px' }} />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Home;