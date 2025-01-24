import React, { useState, useEffect } from 'react';
import { Table, Space, Button, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';

interface VulnerabilityItem {
  id: number;
  name: string;
  vul_type: string;
  cve_id: string;
  cvss_score: number;
  severity: number;
}

const VulnerabilityList: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<VulnerabilityItem[]>([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  });

  const getSeverityTag = (severity: number) => {
    const levels = {
      1: { color: 'blue', text: '低危' },
      2: { color: 'orange', text: '中危' },
      3: { color: 'red', text: '高危' },
      4: { color: 'purple', text: '严重' }
    };
    const level = levels[severity] || { color: 'default', text: '未知' };
    return <Tag color={level.color}>{level.text}</Tag>;
  };

  const columns: ColumnsType<VulnerabilityItem> = [
    {
      title: '漏洞名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '漏洞类型',
      dataIndex: 'vul_type',
      key: 'vul_type',
    },
    {
      title: 'CVE编号',
      dataIndex: 'cve_id',
      key: 'cve_id',
    },
    {
      title: 'CVSS评分',
      dataIndex: 'cvss_score',
      key: 'cvss_score',
    },
    {
      title: '危险等级',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: number) => getSeverityTag(severity),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" onClick={() => handleViewDetails(record.id)}>
            查看详情
          </Button>
        </Space>
      ),
    },
  ];

  const fetchData = async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/vulnerabilities?page=${page}&page_size=${pageSize}`);
      const result = await response.json();
      
      setData(result.items);
      setPagination({
        ...pagination,
        current: page,
        total: result.total
      });
    } catch (error) {
      console.error('获取漏洞数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (id: number) => {
    window.location.href = `/vulnerabilities/${id}`;
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTableChange = (newPagination: any) => {
    fetchData(newPagination.current, newPagination.pageSize);
  };

  return (
    <div className="vulnerability-list">
      <h2>漏洞库</h2>
      <Table
        columns={columns}
        dataSource={data}
        rowKey="id"
        pagination={pagination}
        loading={loading}
        onChange={handleTableChange}
      />
    </div>
  );
};

export default VulnerabilityList;