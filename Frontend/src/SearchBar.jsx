import React, { useState } from "react";
import { Form, FormControl, Button, Table, Spinner } from 'react-bootstrap';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

const host = 'http://localhost:83'

export function SearchBar() {
    const [companyName, setCompanyName] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [searchResults, setSearchResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleInputChange = async (event) => {
        const newCompanyName = event.target.value;
        setCompanyName(newCompanyName);

        if (newCompanyName.length > 0) {
            try {
                const response = await axios.get(`${host}/suggestions?query=${newCompanyName}`);
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
            const response = await axios.get(`${host}/${companyName}/getCompany`);
            setSearchResults(response.data);
        } catch (error) {
            console.error('Error fetching company details:', error);
            setSearchResults({ status: 500, data: 'Error fetching data' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <Form className="d-flex align-items-center">
                <FormControl
                    type="text"
                    placeholder="Enter Company Name"
                    className="mr-2"
                    value={companyName}
                    onChange={handleInputChange}
                />
                <Button variant="outline-success" onClick={handleSearchClick} disabled={loading}>
                    {loading ? <Spinner animation="border" size="sm" /> : <FontAwesomeIcon icon={faSearch} />}
                </Button>
            </Form>

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

            {searchResults && (
                <div className="mt-3">
                    <h3>Search Results:</h3>
                    {searchResults.status === 200 ? (
                        searchResults.data.map((company, index) => (
                            <div key={index}>
                                <p><strong>Name:</strong> {company.c_name}</p>
                                <p><strong>Symbol:</strong> {company.c_symbol}</p>
                            </div>
                        ))
                    ) : (
                        <p>{searchResults.data}</p>
                    )}
                </div>
            )}
        </div>
    );
}