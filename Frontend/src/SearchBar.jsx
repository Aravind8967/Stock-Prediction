import React, { useState } from "react";
import { Form, FormControl, Button, Table, Spinner } from 'react-bootstrap';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { ChartSection } from "./Chart";
import { Row, Col, Alert } from "react-bootstrap";
import axios from "axios";
import './SearchBar.css'
import { FutureChartSection } from "./futureChart";


async function getFutureFundamentals(c_name, futureRange) {
    try {
        console.log('calling getFutureFundamentals function')
        var c_symbol = await getSymbol(c_name)
        var response = await axios.get(`/api/${c_symbol}/getFutureFundamentals/${futureRange}`);
        console.log(response);
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        }
    }
    catch (error) {
        console.error("Api fetchin error : ", error)
    }
}

async function getFutureShareprice(c_name, futureRange) {
    try {
        console.log('calling getFutureShareprice function')
        var c_symbol = await getSymbol(c_name)
        var response = await axios.get(`/api/${c_symbol}/getFutureSharePrice/${futureRange}`);
        if (response.status === 200) {
            console.log(response.data)
            return response.data
        }
    }
    catch (error) {
        console.error("Api fetchin error : ", error)
    }
}

async function getSymbol(c_name) {
    try {
        var response = await axios.get(`/api/${c_name}/getCompany`)
        if (response.status === 200) {
            var c_symbol = await response['data']['data'][0]['c_symbol']
            console.log({ 'getSymbol': c_symbol })
            return c_symbol
        }
    }
    catch (error) {
        console.error('API fetching error : ', error)
    }
}

export function SearchBar() {

    // ======================= Search Bar Variables =================================

    const [companyName, setCompanyName] = useState('');
    const [companySymbol, setCompanySymbol] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [searchResults, setSearchResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showAlert, setShowAlert] = useState(null);
    const [futureValues, setFutureValues] = useState(null); // Store future values
    const [showFutureChart, setShowFutureChart] = useState(false); // Toggle between charts
    const [futureRange, setFutureRange] = useState(4);

    const handleInputChange = async (event) => {
        const newCompanyName = event.target.value;
        setCompanyName(newCompanyName);

        if (newCompanyName.length > 0) {
            try {
                const response = await axios.get(`/api/suggestions?query=${newCompanyName}`);
                setSuggestions(response.data.data || []);
            } catch (error) {
                console.error("Error fetching suggestions:", error);
                setSuggestions([]);
            }
        } else {
            setSuggestions([]);
        }
    };

    const handleSuggestionClick = (suggestion) => {
        setCompanyName(suggestion);
        setSuggestions([]);
    };

    const handleSearchClick = async () => {
        setLoading(true);
        setShowFutureChart(false);
        try {
            const response = await axios.get(`/api/${companyName}/getCompany`);
            const c_symbol = response.data.data[0].c_symbol;
            setSearchResults(response.data);
            setCompanySymbol(c_symbol);
            console.log({ 'c_symbol': c_symbol });

        } catch (error) {
            console.error('Error fetching company details:', error);
            setShowAlert({ massage: 'Company not found, Please check the Company name and try again.', type: 'danger' })
            setSearchResults({ status: 500, data: 'Error fetching data' });
        } finally {
            setLoading(false);
        }
    };

    // ========================= Future Range variables ===================================

    const [futureFundamentals, setFutureFundamental] = useState(null);
    const [futureSharePrice, setFutureSharePrice] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState('');

    const futureBtn = async () => {
        const companySymbol = await getSymbol(companyName);
        setCompanySymbol(companySymbol)
        console.log("futureBtn pressed", { 'company symbol': companySymbol });
        if (companyName === "" || companySymbol === "") {
            setShowAlert({
                massage: "Please Give the Company name and try again.",
                type: "warning",
            });
            return;
        }
        setIsLoading(true);
        setLoadingMessage('Predicting Future values...');

        try {
            const futureSharePriceVal = await axios.get(`/api/${companySymbol}/getFutureSharePrice/${futureRange}`);
            const futureFundamentalsVal = await axios.get(`/api/${companySymbol}/getFutureFundamentals/${futureRange}`);
            const futureData = {
                futureSharePrice: futureSharePriceVal.data,
                futureFundamentals: futureFundamentalsVal.data,
            };
            setFutureValues(futureData);
            setShowFutureChart(true); // Show the future chart
        } catch (error) {
            console.error("Error fetching future data:", error);
            setShowAlert({
                massage: "Error fetching future data. Please try again.",
                type: "danger",
            });
        }
        finally {
            setIsLoading(false);
            setLoadingMessage('');
        }
    };

    return (
        <div className={`app-container ${isLoading ? 'loading' : ''}`}>
            {isLoading && (
                <div className="loading-overlay">
                    <Spinner animation="border" role="status" className="loading-spinner" />
                    <p className="loading-message">{loadingMessage}</p>
                </div>
            )}
            {showAlert && (
                <Alert variant={showAlert.type} onClose={() => setShowAlert(null)} dismissible>
                    {showAlert.massage}
                </Alert>
            )}
            <Row>
                <Col className="SearchBarSection">
                    <div>
                        <Form className="d-flex align-items-center" style={{ position: "relative" }} id="SearchBar">
                            <FormControl
                                type="text"
                                placeholder="Enter Company Name"
                                className="mr-2"
                                value={companyName}
                                onChange={handleInputChange}
                            />
                            <Button
                                variant="outline-success"
                                onClick={handleSearchClick}
                                disabled={loading}
                                id="searchBtn"
                            >
                                {loading ? <Spinner animation="border" size="sm" /> : <FontAwesomeIcon icon={faSearch} />}
                            </Button>

                            {suggestions.length > 0 && (
                                <Table className="table-suggestion">
                                    <tbody>
                                        {suggestions.map((suggestion, index) => (
                                            <tr key={index} onMouseDown={() => handleSuggestionClick(suggestion)}>
                                                <td>{suggestion}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </Table>
                            )}
                        </Form>
                    </div>
                </Col>
                <Col className="futureSection">
                    <Button variant="primary" className="futureBtn" onClick={futureBtn}>
                        Predict
                    </Button>
                    <input type="range"
                        className="futureRange"
                        min={2}
                        max={10}
                        step={2}
                        value={futureRange}
                        onChange={(e) => setFutureRange(e.target.value)}
                    />
                    <input type="number"
                        className="futureRangeVal"
                        readOnly
                        value={futureRange}
                    /><span style={{ fontSize: '1.7rem', margin: '0.5rem' }}>Years</span>
                </Col>
            </Row>
            <Row>
                {/* Conditionally render ChartSection or FutureChartSection */}
                {!showFutureChart && searchResults && (
                    <ChartSection companySymbol={searchResults.data[0].c_symbol} />
                )}
                {showFutureChart && futureValues && <FutureChartSection c_symbol={companySymbol} futureValues={futureValues} />}
            </Row>
        </div>
    );
}

function SearchResults({ SearchData }) {
    if (SearchData === null) {
        return
    }
    else {
        var c_symbol = SearchData['data'][0].c_symbol
        return (
            <ChartSection
                companySymbol={c_symbol}
            />
        );
    }
}