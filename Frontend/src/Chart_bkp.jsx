import React, { useEffect, useState, useRef } from "react";
import { Row, Col, Container } from "react-bootstrap";
import { Chart } from "react-google-charts";
import './Chart.css'
import axios from "axios";

const host = 'http://localhost:83'

export function ChartSection() {

    const [fundamentalData, setFundamentalData] = useState('');
    const companySymbol = 'TATAMOTORS';

    useEffect(() => {
        const fetchFundamentals = async () => {
            try {
                const resFundamentals = await axios.get(`${host}/${companySymbol}/getFundamentals`);
                setFundamentalData(resFundamentals.data);
            }
            catch (error) {
                console.log('Error fetching data', error);
                setFundamentalData(null);
            }
        };

        fetchFundamentals();

    }, [companySymbol]);

    return (
        <>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <RevenueChart
                                years={fundamentalData.years}
                                revenue={fundamentalData.revenue}
                            />
                        ) : (
                            <p>Loading the Revenue data ...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <IncomeChart
                                years={fundamentalData.years}
                                income={fundamentalData.income}
                            />
                        ) : (
                            <p>Loading the Income data ...</p>
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <EPSChart
                                years={fundamentalData.years}
                                eps={fundamentalData.eps}
                            />
                        ) : (
                            <p>Loading the Income data ...</p>
                        )}
                    </div>
                </Col>
                <Col className="ChartCol">
                    <div>
                        {fundamentalData && fundamentalData.years && fundamentalData.revenue ? (
                            <ROEChart
                                years={fundamentalData.years}
                                roe={fundamentalData.roe}
                            />
                        ) : (
                            <p>Loading the Income data ...</p>
                        )}
                    </div>
                </Col>
            </Row>
            <Row className="ChartRow">
                <Col className="SharePriceChart">
                    <div className="trading-view-container">
                        <TradingViewChart />
                    </div>
                </Col>
            </Row>
        </>
    )
}

function RevenueChart({ years, revenue }) {
    const data = [
        ["Year", "Revenue"]
    ];

    if (years && revenue && revenue.length == years.length) {
        for (var i = 0; i < years.length; i++) {
            data.push([String(years[i]), revenue[i]])
        }
        const options = {
            chart: {
                title: "Revenue Over Years",
                subtitle: "Company's Revenue Trend",
            },
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };

        return (
            <Chart
                chartType="Line"
                width="100%"
                height="400px"
                data={data}
                options={options}
            />
        );
    }
    else {
        return
    }

}

function IncomeChart({ years, income }) {
    const data = [
        ["Year", "Income"]
    ];

    if (years && income && income.length == years.length) {
        for (var i = 0; i < years.length; i++) {
            data.push([String(years[i]), income[i]])
        }
        const options = {
            chart: {
                title: "Income Over Years",
                subtitle: "Company's Income Trend",
            },
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };

        return (
            <Chart
                chartType="Line"
                width="100%"
                height="400px"
                data={data}
                options={options}
            />
        );
    }
    else {
        return
    }

}

function EPSChart({ years, eps }) {
    const data = [
        ["Year", "EPS"]
    ];

    if (years && eps && eps.length == years.length) {
        for (var i = 0; i < years.length; i++) {
            data.push([String(years[i]), eps[i]])
        }
        const options = {
            chart: {
                title: "EPS Over Years",
                subtitle: "Company's EPS Trend",
            },
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };

        return (
            <Chart
                chartType="Line"
                width="100%"
                height="400px"
                data={data}
                options={options}
            />
        );
    }
    else {
        return
    }

}

function ROEChart({ years, roe }) {
    const data = [
        ["Year", "ROE"]
    ];

    if (years && roe && roe.length == years.length) {
        for (var i = 0; i < years.length; i++) {
            data.push([String(years[i]), roe[i]])
        }
        const options = {
            chart: {
                title: "ROE Over Years",
                subtitle: "Company's ROE Trend",
            },
            backgroundColor: 'transparent',
            chartArea: { backgroundColor: 'transparent' },
        };

        return (
            <Chart
                chartType="Line"
                width="100%"
                height="400px"
                data={data}
                options={options}
            />
        );
    }
    else {
        return
    }

}

function TradingViewChart({ companySymbol = 'OIL' }) {
    const chartContainerRef = useRef();
    const chart = useRef(null);
    const lineSeries = useRef(null);
    const ema100Series = useRef(null);
    const ema200Series = useRef(null);
    const [sharePriceData, setSharePriceData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSharePrice = async () => {
            setLoading(true);
            setError(null);
            try {
                const respSharePrice = await axios.get(`${host}/${companySymbol}/getSharePrice/4`);
                setSharePriceData(respSharePrice.data);
                setLoading(false);
            } catch (err) {
                setError(err.message || 'Failed to fetch share price data');
                setLoading(false);
            }
        };

        fetchSharePrice();
    }, [companySymbol]);

    useEffect(() => {
        if (!chartContainerRef.current) return;

        chart.current = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.offsetWidth,
            height: 400,
            layout: {
                textColor: 'white', // You can adjust colors
                background: { type: 'solid', color: 'white' },
            },
            crosshair: { mode: 0 }, // snap to data points
        });

        lineSeries.current = chart.current.addLineSeries({ color: 'blue', lineWidth: 2 });
        ema100Series.current = chart.current.addLineSeries({ color: 'orange', lineWidth: 1 });
        ema200Series.current = chart.current.addLineSeries({ color: 'purple', lineWidth: 1 });

        return () => chart.current.remove(); // Cleanup on unmount
    }, []);

    useEffect(() => {
        if (chart.current && sharePriceData.length > 0) {
            const formattedData = sharePriceData.map(item => ({
                time: item.Date, // Assuming 'Date' is in 'YYYY-MM-DD' format
                value: item.Close,
            }));
            lineSeries.current.setData(formattedData);

            const formattedEma100 = sharePriceData.map(item => ({
                time: item.Date,
                value: item.ema100,
            }));
            ema100Series.current.setData(formattedEma100);

            const formattedEma200 = sharePriceData.map(item => ({
                time: item.Date,
                value: item.ema200,
            }));
            ema200Series.current.setData(formattedEma200);

            chart.current.timeScale().fitContent();
        }
    }, [sharePriceData]);

    if (loading) {
        return <p>Loading Share Price Data...</p>;
    }

    if (error) {
        return <p>Error loading Share Price Data: {error}</p>;
    }

    return (
        <div ref={chartContainerRef} className="trading-view-chart" style={{ width: '100%', height: '400px' }}></div>
    );
}

