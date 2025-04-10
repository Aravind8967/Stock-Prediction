import React, { useState } from "react";
import { Form, FormControl, Button, Table, Spinner } from 'react-bootstrap';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { ChartSection } from "./Chart";
import { Row, Col, Alert } from "react-bootstrap";
import axios from "axios";
import './SearchBar.css'
import { ColorType } from "lightweight-charts";


export function SearchBar() {

    // ======================= Search Bar Variables =================================

    const [companyName, setCompanyName] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [searchResults, setSearchResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showAlert, setShowAlert] = useState(false);

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
        try {
            const response = await axios.get(`/api/${companyName}/getCompany`);
            setSearchResults(response.data);
        } catch (error) {
            console.error('Error fetching company details:', error);
            setShowAlert(true)
            setSearchResults({ status: 500, data: 'Error fetching data' });
        } finally {
            setLoading(false);
        }
    };

    // ========================= Future Range variables ===================================

    const [futureRange, setFutureRange] = useState(4)
    
    function futureBtn () {
        console.log('futureBtn pressed');
    }

    return (
        <>
            {showAlert && (
                <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
                    Company not found, Please check the Company name and try again.
                </Alert>
            )}
            <Row>
                <Col className="SearchBarSection">
                    <div>
                        <Form className="d-flex align-items-center" style={{ position: 'relative' }} id="SearchBar">
                            <FormControl
                                type="text"
                                placeholder="Enter Company Name"
                                className="mr-2"
                                value={companyName}
                                onChange={handleInputChange}
                            />
                            <Button variant="outline-success" onClick={handleSearchClick} disabled={loading} id="searchBtn">
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
                    <Button variant="primary" className="futureBtn" onClick={futureBtn}>Predict</Button>
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
                    /><span style={{fontSize: '1.7rem', margin: '0.5rem'}}>Years</span>
                </Col>
            </Row>
            {/* ============= All Chart Sections called by results ======================== */}
            <Row>
                <SearchResults
                    SearchData={searchResults}
                />
            </Row>
        </>
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