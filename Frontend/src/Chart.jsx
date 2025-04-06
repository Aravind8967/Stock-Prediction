import React, { useEffect, useState, useRef } from "react";
import { Row, Col } from "react-bootstrap";
import { Chart } from "react-google-charts";
import './Chart.css';
import axios from "axios";
import { createChart, ColorType, AreaSeries } from 'lightweight-charts';

const host = 'http://localhost:83';

const ChartComponent = props => {
    const {
        data,
        colors: {
            backgroundColor = 'black',
            lineColor = '#2962FF',
            textColor = 'white',
            areaTopColor = '#2962FF',
            areaBottomColor = 'rgba(41, 98, 255, 0.28)',
        } = {},
    } = props;

    const chartContainerRef = useRef();
    const chart = useRef(null);

    useEffect(() => {
        const container = chartContainerRef.current;
        if (!container || !Array.isArray(data) || data.length === 0) {
            return;
        }

        const handleResize = () => {
            if (chart.current) {
                chart.current.applyOptions({ width: container.clientWidth });
            }
        };

        chart.current = createChart(container, {
            layout: {
                background: { type: ColorType.Solid, color: backgroundColor },
                textColor,
            },
            width: container.clientWidth,
            height: 300,
        });
        chart.current.timeScale().fitContent();

        const newSeries = chart.current.addSeries(AreaSeries, { lineColor, topColor: areaTopColor, bottomColor: areaBottomColor });
        newSeries.setData(data);

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            if (chart.current) {
                chart.current.remove();
                chart.current = null;
            }
        };
    }, [data, backgroundColor, lineColor, textColor, areaTopColor, areaBottomColor]);

    return (
        <div
            ref={chartContainerRef}
            style={{ width: '100%', height: '300px' }}
        />
    );
};

function RevenueChart({ years, revenue }) {
    const data = [["Year", "Revenue"]];
    if (years && revenue && revenue.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), revenue[i]]);
        }
        const options = {
            title: "Revenue Over Years",
            subtitle: "Company's Revenue Trend",
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };
        return (
            <Chart
                chartType="Line"
                width="100%"
                height="300px"
                data={data}
                options={options}
            />
        );
    }
    return <p>No Revenue data available.</p>;
}

function IncomeChart({ years, income }) {
    const data = [["Year", "Income"]];
    if (years && income && income.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), income[i]]);
        }
        const options = {
            title: "Income Over Years",
            subtitle: "Company's Income Trend",
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };
        return (
            <Chart
                chartType="Line"
                width="100%"
                height="300px"
                data={data}
                options={options}
            />
        );
    }
    return <p>No Income data available.</p>;
}

function EPSChart({ years, eps }) {
    const data = [["Year", "EPS"]];
    if (years && eps && eps.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), eps[i]]);
        }
        const options = {
            title: "EPS Over Years",
            subtitle: "Company's EPS Trend",
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };
        return (
            <Chart
                chartType="Line"
                width="100%"
                height="300px"
                data={data}
                options={options}
            />
        );
    }
    return <p>No EPS data available.</p>;
}

function ROEChart({ years, roe }) {
    const data = [["Year", "ROE"]];
    if (years && roe && roe.length === years.length) {
        for (let i = 0; i < years.length; i++) {
            data.push([String(years[i]), roe[i]]);
        }
        const options = {
            title: "ROE Over Years",
            subtitle: "Company's ROE Trend",
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };
        return (
            <Chart
                chartType="Line"
                width="100%"
                height="300px"
                data={data}
                options={options}
            />
        );
    }
    return <p>No ROE data available.</p>;
}

export function ChartSection() {
    const [fundamentalData, setFundamentalData] = useState(null);
    const [sharePriceData, setSharePriceData] = useState(null);
    const [isSharePriceLoading, setIsSharePriceLoading] = useState(false);
    const [sharePriceError, setSharePriceError] = useState(null);
    const companySymbol = 'ITC';

    useEffect(() => {
        const fetchFundamentals = async () => {
            try {
                const resFundamentals = await axios.get(`${host}/${companySymbol}/getFundamentals`);
                setFundamentalData(resFundamentals.data);
            } catch (error) {
                console.error('Error fetching fundamentals:', error);
                setFundamentalData(null);
            }
        };

        fetchFundamentals();
    }, [companySymbol]);

    useEffect(() => {
        const fetchSharePrice = async () => {
            setIsSharePriceLoading(true);
            setSharePriceError(null); // Reset error on new fetch
            const range = 4;
            try {
                const sharePriceUrl = `${host}/${companySymbol}/getSharePrice/${range}`;
                const respSharePrice = await axios.get(sharePriceUrl);
                // Format the data to match what Lightweight Charts expects
                const formattedData = respSharePrice.data.map(item => ({
                    time: item.Date,
                    value: item.Close,
                }));
                setSharePriceData(formattedData);
            } catch (error) {
                console.error('Error fetching Share price data:', error);
                setSharePriceError(error.message || 'Failed to fetch share price data');
                setSharePriceData(null);
            } finally {
                setIsSharePriceLoading(false);
            }
        };
        fetchSharePrice();
    }, [companySymbol]);

    return (
        <>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        <h2>Revenue</h2>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <RevenueChart
                                years={fundamentalData.years}
                                revenue={fundamentalData.revenue}
                            />
                        ) : (
                            <p>Loading Revenue data...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        <h2>Income</h2>
                        {fundamentalData && fundamentalData.years && fundamentalData.income ? (
                            <IncomeChart
                                years={fundamentalData.years}
                                income={fundamentalData.income}
                            />
                        ) : (
                            <p>Loading Income data...</p>
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        <h2>EPS</h2>
                        {fundamentalData && fundamentalData.years && fundamentalData.eps ? (
                            <EPSChart
                                years={fundamentalData.years}
                                eps={fundamentalData.eps}
                            />
                        ) : (
                            <p>Loading EPS data...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        <h2>ROE</h2>
                        {fundamentalData && fundamentalData.years && fundamentalData.roe ? (
                            <ROEChart
                                years={fundamentalData.years}
                                roe={fundamentalData.roe}
                            />
                        ) : (
                            <p>Loading ROE data...</p>
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="SharePriceChart">
                    <h2>Share Price</h2>
                    {isSharePriceLoading ? (
                        <p>Loading Share Price data...</p>
                    ) : sharePriceError ? (
                        <p>Error loading Share Price data: {sharePriceError}</p>
                    ) : sharePriceData ? (
                        <ChartComponent data={sharePriceData} />
                    ) : (
                        <p>No Share Price data available.</p>
                    )}
                </Col>
            </Row>
        </>
    );
}